from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.client_controller import list_clients, get_client, create_client, update_client, \
    update_client_contact, delete_client
from epic_events.models import User, Client


class TestListClientController:
    runner = CliRunner()

    def test_list_client(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(list_clients, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert 1 == result.output.count("Id")

    def test_list_client_with_filter(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-c", 3]
        result = self.runner.invoke(list_clients, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 0
        assert 1 == result.output.count("Id")


class TestGetClientController:
    runner = CliRunner()

    def test_get_client_without_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(get_client, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 2
        assert "Missing option" in result.output

    def test_get_client_with_unknown_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "777"]
        result = self.runner.invoke(get_client, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this client does not exist." in result.output

    def test_get_client_with_existing_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "1"]
        result = self.runner.invoke(get_client, options, obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert "Client(id=1" in result.output


class TestCreateClientController:
    runner = CliRunner()

    def test_create_client_with_existing_email(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        email = "client@test.com"
        options = ["-e", email]
        result = self.runner.invoke(create_client, options, obj={"session": mocked_session,
                                                                 "current_user": current_user})
        assert result.exit_code == 1
        assert f"Client ({email}) already exists." in result.output

    def test_create_client_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        email = "sophia@test.com"
        name = "sophia"
        options = ["-e", email, "-n", name, "-ph", 123456789, "-c", "chess tournament"]
        result = self.runner.invoke(create_client, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert f"Client {email} is successfully created." in result.output
        created_client = mocked_session.scalar(select(Client).where(Client.email == email))
        assert created_client is not None
        assert created_client.name == name


class TestUpdateClientController:
    runner = CliRunner()

    def test_update_client_without_optional_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        options = ["-id", 1]
        result = self.runner.invoke(update_client, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Can't update without data in the command." in result.output

    def test_update_client_with_unknown_client(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        email = "sophia@test.com"
        options = ["-id", 777, "-e", email]
        result = self.runner.invoke(update_client, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this client does not exist." in result.output

    def test_update_client_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 4))
        email = "sophia@test.com"
        options = ["-id", 1, "-e", email]
        result = self.runner.invoke(update_client, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output

    def test_update_client_with_existing_email(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        email = "client@test.com"
        options = ["-id", 1, "-e", email]
        result = self.runner.invoke(update_client, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert f"Client ({email}) already exists." in result.output

    def test_update_client_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        email = "alpha@test.com"
        options = ["-id", 1, "-e", email, "-n", "beta", "-ph", 1122334455, "-com", "gamma"]
        result = self.runner.invoke(update_client, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert f"Client {email} is successfully updated." in result.output


class TestUpdateClientContactController:
    runner = CliRunner()

    def test_update_client_contact_with_unknown_client(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        contact_id = 4
        options = ["-id", 777, "-c", contact_id]
        result = self.runner.invoke(update_client_contact, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this client does not exist." in result.output

    def test_update_client_contact_with_unknown_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        contact_id = 777
        options = ["-id", 1, "-c", contact_id]
        result = self.runner.invoke(update_client_contact, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this user does not exist." in result.output

    def test_update_client_contact_with_a_non_commercial_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        contact_id = 1
        options = ["-id", 1, "-c", contact_id]
        result = self.runner.invoke(update_client_contact, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this user does not exist." in result.output

    def test_update_client_contact_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        client_id = 1
        options = ["-id", client_id, "-c", 4]
        result = self.runner.invoke(update_client_contact, options,
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert f"marion is now responsible for the client {client_id}" in result.output


class TestDeleteClientController:
    runner = CliRunner()

    def test_delete_client_with_unknown_client(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        options = ["-id", 777]
        result = self.runner.invoke(delete_client, options, input="y",
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this client does not exist." in result.output

    def test_delete_client_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 4))
        options = ["-id", 1]
        result = self.runner.invoke(delete_client, options, input="y",
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output

    def test_delete_client_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        options = ["-id", 1]
        result = self.runner.invoke(delete_client, options, input="y",
                                    obj={"session": mocked_session, "current_user": current_user})
        assert result.exit_code == 0
        assert "This client is successfully deleted." in result.output
