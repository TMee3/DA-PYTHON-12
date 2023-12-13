from datetime import datetime, timedelta

import pytest
from click import ClickException
from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.event_controller import (
    check_date, create_event, delete_event, get_event, list_events,
    update_event, update_event_support_contact)
from epic_events.models import Event, User


class TestListEventController:
    runner = CliRunner()

    @pytest.mark.parametrize("options, expected_count", [([], 1), (["-noc"], 0)])
    def test_list_events(self, mocked_session, options, expected_count):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(
            list_events,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 0
        assert expected_count == result.output.count("Id")


class TestCreateEventController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "contract_id, current_user_id, expected_exit_code, expected_output",
        [
            (777, 3, 1, "Sorry, this contract does not exist."),
            (1, 4, 1, "Sorry, you're not authorized."),
            (
                2,
                3,
                1,
                "Sorry, the contract (id:2) is not signed, we can't create an event.",
            ),
            (1, 3, 0, "Event 2 is successfully created."),
        ],
    )
    def test_create_event(
        self,
        mocked_session,
        contract_id,
        current_user_id,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(
            select(User).where(User.id == current_user_id)
        )
        options = ["-c", str(contract_id)]
        result = self.runner.invoke(
            create_event,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output


class TestUpdateEventSupportContactController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "event_id, support_contact_id, current_user_id, expected_exit_code, expected_output",
        [
            (777, 2, 1, 1, "Sorry, this event does not exist."),
            (1, 777, 1, 1, "Sorry, this user does not exist."),
            (1, 5, 1, 0, "william is now responsible for the event 1"),
        ],
    )
    def test_update_event_support_contact(
        self,
        mocked_session,
        event_id,
        support_contact_id,
        current_user_id,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(
            select(User).where(User.id == current_user_id)
        )
        options = ["-id", str(event_id), "-s", str(support_contact_id)]
        result = self.runner.invoke(
            update_event_support_contact,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output


class TestUpdateEventController:
    runner = CliRunner()

    def test_update_event_without_optional_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        options = ["-id", 1]
        result = self.runner.invoke(
            update_event,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 1
        assert "Can't update without data in the command." in result.output

    def test_update_event_with_unknown_event(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        options = ["-id", 777, "-a", 50]
        result = self.runner.invoke(
            update_event,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 1
        assert "Sorry, this event does not exist." in result.output

    def test_update_event_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 5))
        options = ["-id", 1, "-a", 50]
        result = self.runner.invoke(
            update_event,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output

    def test_update_event_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 2))
        event_id = 1
        attendees = 50
        options = ["-id", event_id, "-a", attendees]
        result = self.runner.invoke(
            update_event,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 0
        assert all(arg in result.output for arg in [str(event_id), str(attendees)])


class TestGetEventController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "event_id, current_user_id, expected_exit_code, expected_output",
        [
            (777, 2, 1, "Sorry, this event does not exist."),
            (1, 2, 0, "Id: 1"),  # Ajoutez d'autres cas de test si nécessaire
        ],
    )
    def test_get_event(
        self,
        mocked_session,
        event_id,
        current_user_id,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(
            select(User).where(User.id == current_user_id)
        )
        options = ["-id", str(event_id)]
        result = self.runner.invoke(
            get_event,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output


class TestDeleteEventController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "event_id, current_user_id, input_response, expected_exit_code, expected_output",
        [
            (777, 2, "y", 1, "Sorry, this event does not exist."),
            (1, 5, "y", 1, "Sorry, you're not authorized."),
            (1, 2, "y", 0, "This event is successfully deleted."),
        ],
    )
    def test_delete_event(
        self,
        mocked_session,
        event_id,
        current_user_id,
        input_response,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(
            select(User).where(User.id == current_user_id)
        )
        options = ["-id", str(event_id)]
        result = self.runner.invoke(
            delete_event,
            options,
            input=input_response,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output
        if expected_exit_code == 0:
            deleted_event = mocked_session.scalar(
                select(Event).where(Event.id == event_id)
            )
            assert deleted_event is None


class TestCheckDate:
    @pytest.mark.parametrize(
        "start_date, end_date, expected_exception_message",
        [
            (
                datetime.now() + timedelta(days=1),
                datetime.now() + timedelta(days=2),
                None,
            ),
            (
                datetime.now() + timedelta(days=2),
                datetime.now() + timedelta(days=1),
                "End date .* can't be before start date .*.",
            ),
            (
                datetime.now() - timedelta(days=2),
                datetime.now() - timedelta(days=1),
                "Start date and end date cannot be in the past",
            ),
        ],
    )
    def test_check_date(self, start_date, end_date, expected_exception_message):
        if expected_exception_message:
            with pytest.raises(ClickException, match=expected_exception_message):
                check_date(start_date, end_date)
        else:
            result = check_date(start_date, end_date)
            assert result is None
