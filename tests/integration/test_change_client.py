from unittest.mock import patch

from click.testing import CliRunner
from sqlalchemy import select

from epic_events.controllers.cli import cli
from epic_events.models import Client, User


class TestChangeClient:
    runner = CliRunner()
    manager_email = "manager_lucas@test.com"
    manager_password = "1234"
    first_commercial_email = "first_commercial@test.com"
    first_commercial_name = "Nathan"
    first_commercial_password = "1234"
    second_commercial_email = "second_commercial@test.com"
    second_commercial_name = "amélie"
    second_commercial_password = "1234"
    client_email = "luc@mma.com"
    client_name = "luc"
    client_company = "mma tournament"
    new_company_name = "mma tournament 2.0"

    def login_user(self, email, password):
        """
        Connexion d'un utilisateur avec l'email et le mot de passe donnés.
        """
        login_command = ["auth", "login", "-e", email, "--password", password]
        result = self.runner.invoke(cli, login_command)
        assert result.exit_code == 0
        assert "Connection successful." in result.output

    def logout_user(self):
        """
        Déconnexion de l'utilisateur actuellement connecté.
        """
        logout_command = ["auth", "logout"]
        result = self.runner.invoke(cli, logout_command, input="y")
        assert result.exit_code == 0
        assert "You are disconnected, see you later." in result.output

    @patch("epic_events.controllers.cli.current_session")
    def test_change_client_contact(self, mock_current_session, mocked_session):
        """
        Test de modification du contact client.
        """
        mock_current_session.return_value = mocked_session

        with self.runner.isolated_filesystem():
            # Connexion du manager
            manager_email = self.manager_email
            manager_password = self.manager_password
            self.login_user(manager_email, manager_password)

            # Création de deux commerciaux
            first_commercial_email = self.first_commercial_email
            first_commercial_name = self.first_commercial_name
            first_commercial_password = self.first_commercial_password
            create_first_commercial_command = [
                "user",
                "create",
                "-n",
                first_commercial_name,
                "-e",
                first_commercial_email,
                "-r",
                "1",
                "--password",
                first_commercial_password,
            ]
            result = self.runner.invoke(cli, create_first_commercial_command)
            assert result.exit_code == 0
            assert (
                f"User {first_commercial_email} is successfully created"
                in result.output
            )
            first_commercial = mocked_session.scalar(
                select(User).where(User.email == first_commercial_email)
            )
            assert first_commercial is not None

            second_commercial_email = self.second_commercial_email
            second_commercial_name = self.second_commercial_name
            second_commercial_password = self.second_commercial_password
            create_second_commercial_command = [
                "user",
                "create",
                "-n",
                second_commercial_name,
                "-e",
                second_commercial_email,
                "-r",
                "1",
                "--password",
                second_commercial_password,
            ]
            result = self.runner.invoke(cli, create_second_commercial_command)
            assert result.exit_code == 0
            assert (
                f"User {second_commercial_email} is successfully created"
                in result.output
            )
            second_commercial = mocked_session.scalar(
                select(User).where(User.email == second_commercial_email)
            )
            assert second_commercial is not None

            # Déconnexion du manager
            self.logout_user()

            # Connexion du premier commercial
            self.login_user(first_commercial_email, first_commercial_password)

            # Création d'un nouveau client (le premier commercial est le contact)
            client_email = self.client_email
            client_name = self.client_name
            client_company = self.client_company
            create_client_command = [
                "client",
                "create",
                "-e",
                client_email,
                "-n",
                client_name,
                "-ph",
                123456789,
                "-c",
                client_company,
            ]
            result = self.runner.invoke(cli, create_client_command)
            assert result.exit_code == 0
            assert f"Client {client_email} is successfully created." in result.output
            new_client = mocked_session.scalar(
                select(Client).where(Client.email == client_email)
            )
            assert new_client is not None
            assert new_client.name == client_name
            assert new_client.commercial_contact_id == first_commercial.id

            # Déconnexion du premier commercial
            self.logout_user()

            # Connexion du manager
            self.login_user(manager_email, manager_password)

            # Modification du contact client pour le deuxième commercial
            change_client_contact_command = [
                "client",
                "contact",
                "-id",
                new_client.id,
                "-c",
                second_commercial.id,
            ]
            result = self.runner.invoke(cli, change_client_contact_command)
            assert result.exit_code == 0
            assert (
                f"{second_commercial.name} is now responsible for the client {new_client.id}"
                in result.output
            )
            assert new_client.commercial_contact_id == second_commercial.id

            # Déconnexion du manager
            self.logout_user()

            # Connexion du premier commercial (ne devrait plus être en mesure de mettre à jour le client)
            self.login_user(first_commercial_email, first_commercial_password)

            # Tentative de mise à jour du client (doit échouer)
            new_company_name = self.new_company_name
            update_client_command = [
                "client",
                "update",
                "-id",
                new_client.id,
                "-com",
                new_company_name,
            ]
            result = self.runner.invoke(cli, update_client_command)
            assert result.exit_code == 1
            assert "Sorry, you're not authorized." in result.output
            assert new_client.company == client_company

            # Déconnexion du premier commercial
            self.logout_user()

            # Connexion du deuxième commercial
            self.login_user(second_commercial_email, second_commercial_password)

            # Mise à jour du client
            update_client_command = [
                "client",
                "update",
                "-id",
                new_client.id,
                "-com",
                new_company_name,
            ]
            result = self.runner.invoke(cli, update_client_command)
            assert result.exit_code == 0
            assert f"Client {client_email} is successfully updated." in result.output
            assert new_client.company == new_company_name

            # Déconnexion du deuxième commercial
            self.logout_user()


if __name__ == "__main__":
    import unittest

    unittest.main()
