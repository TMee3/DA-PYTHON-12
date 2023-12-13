import pytest
from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.user_controller import create_user
from epic_events.models import User


@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize(
    "current_user_id, expected_exit_code, expected_output",
    [
        (2, 1, "Sorry, you're not authorized."),
    ],
)
def test_create_user_with_unauthorized_user(
    runner, mocked_session, current_user_id, expected_exit_code, expected_output
):
    # Create a mock SQLAlchemy session
    current_user = mocked_session.scalar(select(User).where(User.id == current_user_id))

    email = "leo@test.com"
    options = ["-n", "leo", "-e", email, "-r", "1", "--password", "1234"]

    # Invoke the create_user function with the mock session
    result = runner.invoke(
        create_user,
        options,
        obj={"session": mocked_session, "current_user": current_user},
    )

    # Assert the expected behavior
    assert result.exit_code == expected_exit_code

    # Check the expected output if the exit code is not 0
    if expected_exit_code == 1:
        assert expected_output in result.output
