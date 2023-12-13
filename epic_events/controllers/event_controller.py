from datetime import datetime

import click
from sqlalchemy import and_, select

from epic_events.controllers.auth_controller import check_auth
from epic_events.models import Client, Contract, Event, User
from epic_events.permissions import has_permission
from epic_events.views.contract_view import display_unknown_contract
from epic_events.views.event_view import (display_cant_create_event,
                                          display_error_event_date,
                                          display_event_contact_updated,
                                          display_event_created,
                                          display_event_data,
                                          display_event_deleted,
                                          display_event_updated,
                                          display_events_list,
                                          display_unknown_event)
from epic_events.views.generic_view import (display_exception,
                                            display_no_data_to_update)
from epic_events.views.permissions_view import display_not_authorized
from epic_events.views.user_view import display_unknown_user


@click.group()
@click.pass_context
@check_auth
def event(ctx):
    ctx.ensure_object(dict)


def check_date(start, end):
    """Checks that the dates are in the future and that the end date is not before the start date

    Args:
        start (datetime): event start date
        end (datetime): event end date

    Returns:
        error if conditions are not valid
    """
    datetime_now = datetime.now()
    if start < datetime_now or end < datetime_now:
        return display_error_event_date(start, end, has_passed=True)
    if start > end:
        return display_error_event_date(start, end, has_passed=False)


@event.command(name="list")
@click.option("-c", "--contract_id", required=False, type=int)
@click.option("-s", "--support_id", required=False, type=int)
@click.option("-noc", "--no_contact", required=False, is_flag=True)
@click.pass_context
@has_permission(["management", "commercial", "support"])
def list_events(session, ctx, contract_id, support_id, no_contact):
    try:
        query = select(Event)
        if contract_id:
            query = query.where(Event.contract_id == contract_id)
        if support_id:
            query = query.where(Event.support_contact_id == support_id)
        if no_contact:
            query = query.where(Event.support_contact_id.is_(None))
        events = session.scalars(query)
        return display_events_list(events)
    except Exception as e:
        raise


@event.command(name="create")
@click.option("-c", "--contract_id", required=True, type=int)
@click.option(
    "-sd",
    "--start_date",
    required=False,
    help="Start date (ex:14-08-2024 13:00)",
    type=click.DateTime(formats=["%d-%m-%Y %H:%M"]),
    default=None,
)
@click.option(
    "-ed",
    "--end_date",
    required=False,
    help="End date (ex:14-08-2024 13:00)",
    type=click.DateTime(formats=["%d-%m-%Y %H:%M"]),
    default=None,
)
@click.option("-l", "--location", required=False, type=str, default=None)
@click.option("-a", "--attendees", required=False, type=int, default=None)
@click.option("-n", "--notes", required=False, type=str, default=None)
@click.pass_context
@has_permission(["commercial"])
def create_event(
    session, ctx, contract_id, start_date, end_date, location, attendees, notes
):
    contract = session.scalar(select(Contract).where(Contract.id == contract_id))
    if not contract:
        return display_unknown_contract()

    client = session.scalar(select(Client).where(Client.id == contract.client_id))
    requester = ctx.obj["current_user"]
    if requester.id != client.commercial_contact_id:
        return display_not_authorized()

    # Checks that the contract is signed before creating the event
    if contract.status != "SIGNED":
        return display_cant_create_event(contract)

    if start_date and end_date:
        check_date(start_date, end_date)

    try:
        new_event = Event(
            contract_id=contract_id,
            start_date=start_date,
            end_date=end_date,
            location=location,
            attendees=attendees,
            notes=notes,
        )
        session.add(new_event)
        session.commit()
        return display_event_created(new_event)
    except Exception as e:
        raise


@event.command(name="contact")
@click.option("-id", "--event_id", required=True, type=int)
@click.option("-s", "--support_id", required=True, type=int)
@click.pass_context
@has_permission(["management"])
def update_event_support_contact(session, ctx, event_id, support_id):
    selected_event = session.scalar(select(Event).where(Event.id == event_id))
    if not selected_event:
        return display_unknown_event()

    selected_contact = session.scalar(
        select(User).where(and_(User.id == support_id, User.role == 2))
    )
    if not selected_contact:
        return display_unknown_user()

    try:
        selected_event.support_contact_id = selected_contact.id
        session.commit()
        return display_event_contact_updated(selected_event, selected_contact)
    except Exception as e:
        raise


@event.command(name="update")
@click.option("-id", "--event_id", required=True, type=int)
@click.option(
    "-sd",
    "--start_date",
    required=False,
    help="Start date (ex:14-08-2024 13:00)",
    type=click.DateTime(formats=["%d-%m-%Y %H:%M"]),
    default=None,
)
@click.option(
    "-ed",
    "--end_date",
    required=False,
    help="End date (ex:14-08-2024 13:00)",
    type=click.DateTime(formats=["%d-%m-%Y %H:%M"]),
    default=None,
)
@click.option("-l", "--location", required=False, type=str, default=None)
@click.option("-a", "--attendees", required=False, type=int, default=None)
@click.option("-n", "--notes", required=False, type=str, default=None)
@click.pass_context
@has_permission(["support"])
def update_event(
    session, ctx, event_id, start_date, end_date, location, attendees, notes
):
    if not (start_date or end_date or location or attendees or notes):
        return display_no_data_to_update()

    selected_event = session.scalar(select(Event).where(Event.id == event_id))
    if not selected_event:
        return display_unknown_event()

    requester = ctx.obj["current_user"]
    if requester.id != selected_event.support_contact_id:
        return display_not_authorized()

    try:
        selected_event.start_date = (
            start_date if start_date else selected_event.start_date
        )
        selected_event.end_date = end_date if end_date else selected_event.end_date
        if selected_event.start_date and selected_event.end_date:
            check_date(selected_event.start_date, selected_event.end_date)
        selected_event.location = location if location else selected_event.location
        selected_event.attendees = attendees if attendees else selected_event.attendees
        selected_event.notes = notes if notes else selected_event.notes
        session.commit()
        return display_event_updated(selected_event)
    except Exception as e:
        raise


@event.command(name="get")
@click.option("-id", "--event_id", required=True, type=int)
@click.pass_context
@has_permission(["management", "commercial", "support"])
def get_event(session, ctx, event_id):
    selected_event = session.scalar(select(Event).where(Event.id == event_id))
    if not selected_event:
        return display_unknown_event()
    return display_event_data(selected_event)


@event.command(name="delete")
@click.option("-id", "--event_id", required=True, type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this event?")
@click.pass_context
@has_permission(roles=["support"])
def delete_event(session, ctx, event_id):
    selected_event = session.scalar(select(Event).where(Event.id == event_id))
    if not selected_event:
        return display_unknown_event()

    requester = ctx.obj["current_user"]
    if requester.id != selected_event.support_contact_id:
        return display_not_authorized()

    try:
        session.delete(selected_event)
        session.commit()
        return display_event_deleted()
    except Exception as e:
        raise
