from unittest.mock import patch
from click.testing import CliRunner
from sqlalchemy import select
from epic_events.controllers.cli import cli
from epic_events.models import User, Client, Contract, Event

class TestBasicUsage:
    runner = CliRunner()

    # Define variables here
    manager_email = "manager_lucas@test.com"
    manager_password = "1234"
    commercial_email = "new_commercial@test.com"
    commercial_name = "Leo"
    commercial_password = "1234"
    support_email = "new_support@test.com"
    support_name = "nicolas"
    support_password = "1234"
    client_email = "natasha@test.com"
    client_name = "natasha"
    left_to_pay = 100
    status = "SIGNED"
    attendees = 70

    # Méthodes utilitaires

    def login_user(self, email, password):
        login_options = ["auth", "login", "-e", email, "--password", password]
        result = self.runner.invoke(cli, login_options)
        assert result.exit_code == 0
        assert "Connection successful." in result.output

    def logout_user(self):
        logout_options = ["auth", "logout"]
        result = self.runner.invoke(cli, logout_options, input="y")
        assert result.exit_code == 0
        assert "You are disconnected, see you later." in result.output

    def create_user(self, name, email, role, password):
        create_user_options = ["user", "create", "-n", name, "-e", email, "-r", str(role), "--password", password]
        result = self.runner.invoke(cli, create_user_options)
        assert result.exit_code == 0
        assert f"User {email} is successfully created" in result.output

    def create_contract(self, client_id, amount):
        create_contract_options = ["contract", "create", "-client", str(client_id), "-a", str(amount)]
        result = self.runner.invoke(cli, create_contract_options)
        assert result.exit_code == 0
        assert "Contract" in result.output  # Ajoutez une vérification appropriée ici

    # Méthode de test

    @patch("epic_events.controllers.cli.current_session")
    def test_basic_usage_from_connection_to_disconnection_with_crud_process(
        self, mock_current_session, mocked_session
    ):
        mock_current_session.return_value = mocked_session

        with self.runner.isolated_filesystem():
            # Étape 1 : Connexion du manager à l'application
            manager_email = self.manager_email
            manager_password = self.manager_password
            self.login_user(manager_email, manager_password)

            # Étape 2 : Création d'un commercial et d'un support
            commercial_email = self.commercial_email
            commercial_name = self.commercial_name
            commercial_password = self.commercial_password
            self.create_user(commercial_name, commercial_email, 1, commercial_password)
            new_commercial = mocked_session.scalar(select(User).where(User.email == commercial_email))

            support_email = self.support_email
            support_name = self.support_name
            support_password = self.support_password
            self.create_user(support_name, support_email, 2, support_password)
            new_support = mocked_session.scalar(select(User).where(User.email == support_email))

            # Étape 3 : Déconnexion du manager
            self.logout_user()

            # Étape 4 : Connexion du nouveau commercial
            self.login_user(commercial_email, commercial_password)

            # Étape 5 : Création d'un client
            client_email = self.client_email
            client_name = self.client_name
            create_client_options = ["client", "create", "-e", client_email, "-n", client_name, "-ph", "123456789", "-c", "chess tournament"]
            result = self.runner.invoke(cli, create_client_options)
            assert result.exit_code == 0
            assert f"Client {client_email} is successfully created." in result.output
            new_client = mocked_session.scalar(select(Client).where(Client.email == client_email))
            assert new_client is not None
            assert new_client.name == client_name
            assert new_client.commercial_contact_id == new_commercial.id

            # Étape 6 : Déconnexion du commercial
            self.logout_user()

            # Étape 7 : Connexion du manager
            self.login_user(manager_email, manager_password)

            # Étape 8 : Création d'un contrat pour le nouveau client
            self.create_contract(new_client.id, 100)
            new_contract = mocked_session.scalar(select(Contract).where(Contract.client_id == new_client.id))

            # Étape 9 : Déconnexion du manager
            self.logout_user()

            # Étape 10 : Connexion du commercial
            self.login_user(commercial_email, commercial_password)

            # Étape 11 : Mise à jour du contrat
            left_to_pay = self.left_to_pay
            status = self.status
            assert new_contract.status == "UNSIGNED"
            update_contract_options = ["contract", "update", "-id", str(new_contract.id), "-ltp", str(left_to_pay), "-s", status]
            result = self.runner.invoke(cli, update_contract_options)
            assert result.exit_code == 0
            assert all(arg in result.output for arg in [str(new_contract.id), str(left_to_pay), status])
            assert new_contract.status == status
            assert new_contract.left_to_pay == left_to_pay

            # Étape 12 : Création d'un événement
            create_event_options = ["event", "create", "-c", str(new_contract.id)]
            result = self.runner.invoke(cli, create_event_options)
            assert result.exit_code == 0
            assert "Event" in result.output  # Ajoutez une vérification appropriée ici
            new_event = mocked_session.scalar(select(Event).where(Event.contract_id == new_contract.id))

            # Étape 13 : Déconnexion du commercial
            self.logout_user()

            # Étape 14 : Connexion du manager
            self.login_user(manager_email, manager_password)

            # Étape 15 : Attribution d'un support à l'événement
            assign_support_options = ["event", "contact", "-id", str(new_event.id), "-s", str(new_support.id)]
            result = self.runner.invoke(cli, assign_support_options)
            assert result.exit_code == 0
            assert f"{new_support.name} is now responsible for the event {new_event.id}" in result.output

            # Étape 16 : Déconnexion du manager
            self.logout_user()

            # Étape 17 : Connexion du support
            self.login_user(support_email, support_password)

            # Étape 18 : Mise à jour de l'événement
            attendees = self.attendees
            update_event_options = ["event", "update", "-id", str(new_event.id), "-a", str(attendees)]
            result = self.runner.invoke(cli, update_event_options)
            assert result.exit_code == 0
            assert all(arg in result.output for arg in [str(new_event.id), str(attendees)])
            assert new_event.attendees == attendees

            # Étape 19 : Déconnexion du support
            self.logout_user()

            # Étape 20 : Connexion du commercial
            self.login_user(commercial_email, commercial_password)

            # Étape 21 : Suppression du client
            delete_client_options = ["client", "delete", "-id", str(new_client.id)]
            result = self.runner.invoke(cli, delete_client_options, input="y")
            assert result.exit_code == 0
            assert "This client is successfully deleted." in result.output
            deleted_client = mocked_session.scalar(select(Client).where(Client.id == new_client.id))
            old_contract = mocked_session.scalar(select(Contract).where(Contract.id == new_contract.id))
            old_event = mocked_session.scalar(select(Event).where(Event.id == new_event.id))
            assert deleted_client is None
            assert old_contract is None
            assert old_event is None

            # Étape 22 : Déconnexion du commercial
            self.logout_user()
