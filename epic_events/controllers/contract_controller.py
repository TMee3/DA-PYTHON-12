import click
import sentry_sdk
from sqlalchemy import select

from epic_events.controllers.auth_controller import check_auth
from epic_events.models import Client, Contract
from epic_events.permissions import has_permission
from epic_events.views.client_view import display_unknown_client
from epic_events.views.contract_view import (display_contract_created,
                                             display_contract_data,
                                             display_contract_deleted,
                                             display_contract_updated,
                                             display_contracts_list,
                                             display_error_amount,
                                             display_unknown_contract)
from epic_events.views.generic_view import (display_exception,
                                            display_no_data_to_update)
from epic_events.views.permissions_view import display_not_authorized


@click.group()
@click.pass_context
@check_auth
def contract(ctx):
    ctx.ensure_object(dict)


def check_amount(amount, left_to_pay):
    """Check that the remaining amount to be paid is not greater than the total amount

    Args:
        amount (int): total amount of the contract
        left_to_pay (int): the remaining amount to pay

    Returns:
        True if the condition is valid else display an error
    """
    return (
        True if amount >= left_to_pay >= 0 and amount >= 0 else display_error_amount()
    )


@contract.command(name="list")
@click.option("-client", "--client_id", required=False, type=int)
@click.option("-u", "--unpaid", required=False, is_flag=True)
@click.option(
    "-s",
    "--status",
    required=False,
    type=click.Choice(["SIGNED", "UNSIGNED"], case_sensitive=False),
)
@click.pass_context
@has_permission(["management", "commercial", "support"])
def list_contracts(session, ctx, client_id, unpaid, status):
    try:
        query = select(Contract)
        if client_id:
            query = query.where(Contract.client_id == client_id)
        if unpaid:
            query = query.where(Contract.left_to_pay > 0)
        if status:
            query = query.where(Contract.status == status)
        contracts = session.scalars(query)
        return display_contracts_list(contracts)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)


@contract.command(name="create")
@click.option("-client", "--client_id", required=True, type=int)
@click.option("-a", "--amount", required=True, type=int)
@click.option("-ltp", "--left_to_pay", required=False, type=int)
@click.option(
    "-s",
    "--status",
    required=False,
    default="UNSIGNED",
    type=click.Choice(["SIGNED", "UNSIGNED"], case_sensitive=False),
)
@click.pass_context
@has_permission(["management"])
def create_contract(session, ctx, client_id, amount, left_to_pay, status):
    client = session.scalar(select(Client).where(Client.id == client_id))
    if not client:
        return display_unknown_client()

    try:
        current_left_to_pay = left_to_pay if left_to_pay else amount
        check_amount(amount, current_left_to_pay)
        new_contract = Contract(
            client_id=client_id,
            total_amount=amount,
            left_to_pay=current_left_to_pay,
            status=status,
        )
        session.add(new_contract)
        session.commit()

        # Send a message via sentry to notify that a contract has been signed
        if new_contract.status == "SIGNED":
            with sentry_sdk.push_scope() as scope:
                scope.set_tag("contracts-info", "signed")
                sentry_sdk.capture_message(
                    f"Contract {new_contract.id} has been signed."
                )

        return display_contract_created(new_contract)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)


@contract.command(name="update")
@click.option("-id", "--contract_id", required=True, type=int)
@click.option("-a", "--amount", required=False, type=int)
@click.option("-ltp", "--left_to_pay", required=False, type=int)
@click.option(
    "-s",
    "--status",
    required=False,
    type=click.Choice(["SIGNED", "UNSIGNED"], case_sensitive=False),
)
@click.pass_context
@has_permission(["management", "commercial"])
def update_contract(session, ctx, contract_id, amount, left_to_pay, status):
    if not (amount or left_to_pay or status):
        return display_no_data_to_update()

    requester = ctx.obj["current_user"]
    selected_contract = session.scalar(
        select(Contract).where(Contract.id == contract_id)
    )
    if not selected_contract:
        return display_unknown_contract()
    client = session.scalar(
        select(Client).where(Client.id == selected_contract.client_id)
    )
    if requester.role == 1 and client.commercial_contact_id != requester.id:
        return display_not_authorized()

    try:
        selected_contract.total_amount = (
            amount if amount else selected_contract.total_amount
        )
        selected_contract.left_to_pay = (
            left_to_pay if left_to_pay else selected_contract.left_to_pay
        )
        check_amount(selected_contract.total_amount, selected_contract.left_to_pay)
        selected_contract.status = status if status else selected_contract.status
        session.commit()

        # Send a message via sentry to notify that a contract has been signed
        if status == "SIGNED":
            with sentry_sdk.push_scope() as scope:
                scope.set_tag("contracts-info", "signed")
                sentry_sdk.capture_message(
                    f"Contract {selected_contract.id} has been signed."
                )

        return display_contract_updated(selected_contract)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)


@contract.command(name="get")
@click.option("-id", "--contract_id", required=True, type=int)
@click.pass_context
@has_permission(["management", "commercial", "support"])
def get_contract(session, ctx, contract_id):
    selected_contract = session.scalar(
        select(Contract).where(Contract.id == contract_id)
    )
    if not selected_contract:
        return display_unknown_contract()
    return display_contract_data(selected_contract)


@contract.command(name="delete")
@click.option("-id", "--contract_id", required=True, type=int)
@click.confirmation_option(prompt="Are you sure you want to delete this contract?")
@click.pass_context
@has_permission(roles=["management"])
def delete_contract(session, ctx, contract_id):
    selected_contract = session.scalar(
        select(Contract).where(Contract.id == contract_id)
    )

    if not selected_contract:
        return display_unknown_contract()

    try:
        session.delete(selected_contract)
        session.commit()
        return display_contract_deleted()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return display_exception(e)
