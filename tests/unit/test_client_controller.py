import pytest
from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.client_controller import (create_client,
                                                       delete_client,
                                                       get_client,
                                                       list_clients,
                                                       update_client,
                                                       update_client_contact)
from epic_events.models import Client, User


class TestListClientController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "options, expected_exit_code, expected_output_count",
        [
            ([], 0, 1),
            (["-c", 3], 0, 1),
        ],
    )
    def test_list_client(
        self, mocked_session, options, expected_exit_code, expected_output_count
    ):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(
            list_clients,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output_count == result.output.count("Id")


class TestGetClientController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "options, exit_code, output",
        [
            ([], 2, "Missing option"),
            (["-id", "777"], 1, "Sorry, this client does not exist."),
            (["-id", "1"], 0, "Client(id=1"),
        ],
    )
    def test_get_client(self, mocked_session, options, exit_code, output):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(
            get_client,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == exit_code
        assert output in result.output


class TestCreateClientController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "email, name, phone, company, expected_exit_code, expected_output",
        [
            (
                "client@test.com",
                None,
                None,
                None,
                1,
                "Client (client@test.com) already exists.",
            ),
            (
                "sophia@test.com",
                "sophia",
                123456789,
                "chess tournament",
                0,
                "Client sophia@test.com is successfully created.",
            ),
        ],
    )
    def test_create_client(
        self,
        mocked_session,
        email,
        name,
        phone,
        company,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        options = []
        if email:
            options.extend(["-e", email])
        if name:
            options.extend(["-n", name])
        if phone:
            options.extend(["-ph", phone])
        if company:
            options.extend(["-c", company])

        result = self.runner.invoke(
            create_client,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output
        if expected_exit_code == 0:
            created_client = mocked_session.scalar(
                select(Client).where(Client.email == email)
            )
            assert created_client is not None
            assert created_client.name == name


class TestUpdateClientController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "id, email, name, phone, company, current_user_id, expected_exit_code, expected_output",
        [
            (
                1,
                None,
                None,
                None,
                None,
                3,
                1,
                "Can't update without data in the command.",
            ),
            (
                777,
                "sophia@test.com",
                None,
                None,
                None,
                3,
                1,
                "Sorry, this client does not exist.",
            ),
            (
                1,
                "client@test.com",
                None,
                None,
                None,
                3,
                1,
                "Client (client@test.com) already exists.",
            ),
            (
                1,
                "alpha@test.com",
                "beta",
                1122334455,
                "gamma",
                3,
                0,
                "Client alpha@test.com is successfully updated.",
            ),
            (
                1,
                "alpha@test.com",
                None,
                None,
                None,
                4,
                1,
                "Sorry, you're not authorized.",
            ),
        ],
    )
    def test_update_client(
        self,
        mocked_session,
        id,
        email,
        name,
        phone,
        company,
        current_user_id,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(
            select(User).where(User.id == current_user_id)
        )
        options = ["-id", str(id)]
        if email:
            options.extend(["-e", email])
        if name:
            options.extend(["-n", name])
        if phone:
            options.extend(["-ph", str(phone)])
        if company:
            options.extend(["-com", company])

        result = self.runner.invoke(
            update_client,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output


class TestUpdateClientContactController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "client_id, contact_id, current_user_id, expected_exit_code, expected_output",
        [
            (777, 4, 1, 1, "Sorry, this client does not exist."),
            (1, 777, 1, 1, "Sorry, this user does not exist."),
            (1, 1, 1, 1, "Sorry, this user does not exist."),
            (1, 4, 1, 0, "marion is now responsible for the client 1"),
        ],
    )
    def test_update_client_contact(
        self,
        mocked_session,
        client_id,
        contact_id,
        current_user_id,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(
            select(User).where(User.id == current_user_id)
        )
        options = ["-id", str(client_id), "-c", str(contact_id)]

        result = self.runner.invoke(
            update_client_contact,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output


class TestDeleteClientController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "client_id, current_user_id, input_response, expected_exit_code, expected_output",
        [
            (777, 3, "y", 1, "Sorry, this client does not exist."),
            (1, 4, "y", 1, "Sorry, you're not authorized."),
            (1, 3, "y", 0, "This client is successfully deleted."),
        ],
    )
    def test_delete_client(
        self,
        mocked_session,
        client_id,
        current_user_id,
        input_response,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(
            select(User).where(User.id == current_user_id)
        )
        options = ["-id", str(client_id)]
        result = self.runner.invoke(
            delete_client,
            options,
            input=input_response,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output
