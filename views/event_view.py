from click import ClickException


def display_events_list(events):
    for event in events:
        print(f"Id: {event.id}, contract: {event.contract_id}, support: {event.support_contact_id}")


def display_unknown_event():
    raise ClickException("Sorry, this event does not exist.")


def display_event_data(event):
    print(f"Id: {event.id}, contract: {event.contract_id}, start at: {event.start_date}, end at: {event.end_date}, "
          f"support: {event.support_contact_id}, location: {event.location}, attendees: {event.attendees},"
          f" notes: {event.notes}")


def display_cant_create_event(contract):
    raise ClickException(f"Sorry, the contract (id:{contract.id}) is not signed, we can't create an event.")


def display_event_created(event):
    print(f"Event {event.id} is successfully created.")


def display_error_event_date(start_date, end_date, has_passed):
    if has_passed:
        raise ClickException("Start date and end date cannot be in the past")
    else:
        raise ClickException(f"End date {end_date} can't be before start date {start_date}.")


def display_event_deleted():
    print("This event is successfully deleted.")


def display_event_contact_updated(event, contact):
    print(f"{contact.name} is now responsible for the event {event.id}")


def display_event_updated(event):
    print(f"Id: {event.id}, contract: {event.contract_id}, start at: {event.start_date}, end at: {event.end_date}, "
          f"support: {event.support_contact_id}, location: {event.location}, attendees: {event.attendees},"
          f" notes: {event.notes}")
