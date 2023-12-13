import pytest
from click.testing import CliRunner

from epic_events.controllers.auth_controller import login, logout


class TestAuthController:
    runner = CliRunner()

    @pytest.mark.parametrize(
        "email, password, expected_exit_code, expected_output",
        [
            ("manager_lucas@test.com", "1234", 0, "Connection successful."),
            (
                "manager_lucas@test.com",
                "4567",
                1,
                "Please, be sure to use the correct email and password.",
            ),
            (
                "unknown@test.com",
                "1234",
                1,
                "Please, be sure to use the correct email and password.",
            ),
        ],
    )
    def test_login(
        self, email, password, expected_exit_code, expected_output, mocked_session
    ):
        with self.runner.isolated_filesystem():
            options = ["-e", email, "--password", password]
            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == expected_exit_code
            assert expected_output in result.output

    def test_login_with_connected_user(self, mocked_session):
        with self.runner.isolated_filesystem():
            email = "manager_lucas@test.com"
            password = "1234"
            options = ["-e", email, "--password", password]

            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 0
            assert "Connection successful." in result.output

            # Attempt to login again
            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 1
            assert "You are already connected." in result.output

    def test_logout(self, mocked_session):
        with self.runner.isolated_filesystem():
            email = "manager_lucas@test.com"
            password = "1234"
            options = ["-e", email, "--password", password]

            result = self.runner.invoke(login, options, obj={"session": mocked_session})
            assert result.exit_code == 0
            assert "Connection successful." in result.output

            result = self.runner.invoke(
                logout, input="y", obj={"session": mocked_session}
            )
            assert result.exit_code == 0
            assert "You are disconnected, see you later." in result.output
