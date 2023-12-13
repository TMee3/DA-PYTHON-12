import pytest
from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.user_controller import (create_user, delete_user,
                                                     get_user, list_users,
                                                     update_user)
from epic_events.models import User


class TestCreateUserController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "role, expected_exit_code, expected_output",
        [
            ("777", 1, "777 is not a correct role."),
            ("1", 0, "User leo@test.com is successfully created"),
        ],
    )
    def test_create_user_with_unknown_role(
        self, mocked_session, role, expected_exit_code, expected_output
    ):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        email = "leo@test.com"
        name = "leo"
        options = ["-n", name, "-e", email, "-r", role, "--password", "1234"]
        result = self.runner.invoke(
            create_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output

    @pytest.mark.parametrize(
        "name, email, role, expected_exit_code, expected_output",
        [
            (
                "lucas",
                "manager_lucas@test.com",
                "3",
                1,
                "User (manager_lucas@test.com) already exists.",
            ),
            (
                "leo",
                "leo@test.com",
                "1",
                0,
                "User leo@test.com is successfully created",
            ),
        ],
    )
    def test_create_user_with_existing_user(
        self, mocked_session, name, email, role, expected_exit_code, expected_output
    ):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-n", name, "-e", email, "-r", role, "--password", "1234"]
        result = self.runner.invoke(
            create_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output

    @pytest.mark.parametrize("name, email, role", [("leo", "leo@test.com", "1")])
    def test_create_user_with_correct_argument(self, mocked_session, name, email, role):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-n", name, "-e", email, "-r", role, "--password", "1234"]
        result = self.runner.invoke(
            create_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 0
        assert f"User {email} is successfully created" in result.output
        created_user = mocked_session.scalar(select(User).where(User.email == email))
        assert created_user is not None
        assert created_user.name == name


class TestGetUserController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "id_argument, expected_exit_code, expected_output",
        [
            (None, 2, "Missing option"),
            ("777", 1, "Sorry, this user does not exist."),
            ("ab", 2, "Invalid value"),
            ("2", 0, "User(id=2"),
        ],
    )
    def test_get_user(
        self, mocked_session, id_argument, expected_exit_code, expected_output
    ):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = []
        if id_argument:
            options.extend(["-id", id_argument])
        result = self.runner.invoke(
            get_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output

    def test_get_user_with_unknown_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "777"]
        result = self.runner.invoke(
            get_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 1
        assert "Sorry, this user does not exist." in result.output

    def test_get_user_with_non_digit_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "ab"]
        result = self.runner.invoke(
            get_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 2
        assert "Invalid value" in result.output

    def test_get_user_with_correct_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 2]
        result = self.runner.invoke(
            get_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 0
        assert "User(id=2" in result.output


class TestUpdateUserController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "id_argument, name_argument, email_argument, role_argument, expected_exit_code, expected_output",
        [
            (
                2,
                "leo",
                "commercial_leo@test.com",
                1,
                0,
                "User commercial_leo@test.com is successfully updated",
            ),
            (2, None, None, None, 1, "Can't update without data in the command."),
            (2, "leo", None, 777, 1, "777 is not a correct role."),
        ],
    )
    def test_update_user(
        self,
        mocked_session,
        id_argument,
        name_argument,
        email_argument,
        role_argument,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", str(id_argument)]
        if name_argument is not None:
            options.extend(["-n", name_argument])
        if email_argument is not None:
            options.extend(["-e", email_argument])
        if role_argument is not None:
            options.extend(["-r", str(role_argument)])
        result = self.runner.invoke(
            update_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output

    def test_update_user_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        email = "commercial_leo@test.com"
        options = ["-id", 2, "-n", "leo", "-e", email, "-r", 1]
        result = self.runner.invoke(
            update_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 0
        assert f"User {email} is successfully updated" in result.output

    def test_update_user_without_optional_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 2]
        result = self.runner.invoke(
            update_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 1
        assert "Can't update without data in the command." in result.output

    def test_update_user_with_unknown_role(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        email = "commercial_leo@test.com"
        options = ["-id", 2, "-n", "leo", "-e", email, "-r", 777]
        result = self.runner.invoke(
            update_user,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 1
        assert "777 is not a correct role." in result.output


class TestDeleteUserController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "user_id, confirmation_input, expected_exit_code, expected_output",
        [
            (777, "y", 1, "Sorry, this user does not exist."),
            (3, "y", 0, "This user is successfully deleted"),
            (3, "N", 1, "Aborted"),
        ],
    )
    def test_delete_user(
        self,
        mocked_session,
        user_id,
        confirmation_input,
        expected_exit_code,
        expected_output,
    ):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", str(user_id)]
        result = self.runner.invoke(
            delete_user,
            options,
            input=confirmation_input,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        assert expected_output in result.output

    def test_delete_user_with_unknown_user_id(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "777"]
        result = self.runner.invoke(
            delete_user,
            options,
            input="y",
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 1
        assert "Sorry, this user does not exist." in result.output

    def test_delete_user_with_confirmation_to_no(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", "3"]
        result = self.runner.invoke(
            delete_user,
            options,
            input="N",
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == 1
        assert "Aborted" in result.output


class TestListUserController:
    runner = CliRunner()

    def create_current_user(self, mocked_session):
        return mocked_session.scalar(select(User).where(User.id == 1))

    @pytest.mark.parametrize("role_id, expected_exit_code", [(777, 1), (3, 0)])
    def test_list_user(self, mocked_session, role_id, expected_exit_code):
        current_user = self.create_current_user(mocked_session)
        options = ["-r", str(role_id)]
        result = self.runner.invoke(
            list_users,
            options,
            obj={"session": mocked_session, "current_user": current_user},
        )
        assert result.exit_code == expected_exit_code
        if expected_exit_code == 1:
            assert f"{role_id} is not a correct role." in result.output
        elif expected_exit_code == 0:
            assert "Id" in result.output

    def test_list_user_without_filter(self, mocked_session):
        current_user = self.create_current_user(mocked_session)
        result = self.runner.invoke(
            list_users, obj={"session": mocked_session, "current_user": current_user}
        )
        assert result.exit_code == 0
        assert 5 == result.output.count("Id")
