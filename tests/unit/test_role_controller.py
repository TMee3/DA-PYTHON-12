from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.role_controller import list_roles
from epic_events.models import User


class TestRoleController:
    runner = CliRunner()

    def test_list_roles(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        result = self.runner.invoke(
            list_roles, obj={"session": mocked_session, "current_user": current_user}
        )
        assert result.exit_code == 0

        expected_roles = ["management", "commercial", "support"]
        assert result.output.count("Role") == len(expected_roles)
        assert all(role in result.output for role in expected_roles)
