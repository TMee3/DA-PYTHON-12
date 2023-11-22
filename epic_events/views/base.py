from click import ClickException, style




def display_successful_connection(login):
    print("Connexion réussie." if login else "Vous êtes déconnecté, à bientôt.")


def display_auth_data_entry_error():
    raise ClickException(style("Veuillez vous assurer d'utiliser l'email et le mot de passe corrects.", fg='red'))


def display_auth_already_connected():
    raise ClickException(style("Vous êtes déjà connecté.", fg='yellow'))


def display_invalid_token():
    raise ClickException(style("Jeton invalide.", fg='red'))


def display_not_connected_error():
    raise ClickException(style("Veuillez d'abord vous connecter.", fg='red'))


def display_missing_requester():
    raise ClickException(style("Demandeur manquant.", fg='red'))


def display_unknown_client():
    raise ClickException("Désolé, ce client n'existe pas.")


def display_client_data(data):
    print(data)


def display_clients_list(clients):
    for client in clients:
        print(f"Id: {client.id}, nom: {client.name}, email: {client.email}, téléphone: {client.phone}, "
              f"entreprise: {client.company}, id_contact_commercial: {client.commercial_contact_id}")


def display_client_already_exists(email):
    raise ClickException(f"Le client ({email}) existe déjà.")


def display_client_created(email):
    print(f"Le client {email} a été créé avec succès.")


def display_client_updated(email):
    print(f"Le client {email} a été mis à jour avec succès.")


def display_client_deleted():
    print("Ce client a été supprimé avec succès.")


def display_client_contact_updated(client, contact):
    print(f"{contact.name} est maintenant responsable du client {client.id}")


def display_contracts_list(contracts):
    for contract in contracts:
        print(f"Id: {contract.id}, client: {contract.client_id}, montant: {contract.total_amount}, "
              f"reste à payer: {contract.left_to_pay}, statut: {contract.status}")


def display_contract_created(contract):
    print(f"Le contrat {contract.id} a été créé avec succès.")


def display_contract_data(contract):
    print(f"Id: {contract.id}, client: {contract.client_id}, montant: {contract.total_amount}, "
          f"reste à payer: {contract.left_to_pay}, statut: {contract.status}")


def display_unknown_contract():
    raise ClickException("Désolé, ce contrat n'existe pas.")


def display_contract_deleted():
    print("Ce contrat a été supprimé avec succès.")


def display_contract_updated(contract):
    print(f"Id: {contract.id}, client: {contract.client_id}, montant: {contract.total_amount}, "
          f"reste à payer: {contract.left_to_pay}, statut: {contract.status}")


def display_error_amount():
    raise ClickException("Le montant total et le montant restant à payer doivent être des entiers positifs et "
                         "le montant restant à payer ne peut pas être supérieur au montant total.")


def display_events_list(events):
    for event in events:
        print(f"Id: {event.id}, contrat: {event.contract_id}, support: {event.support_contact_id}")


def display_unknown_event():
    raise ClickException("Désolé, cet événement n'existe pas.")


def display_event_data(event):
    print(f"Id: {event.id}, contrat: {event.contract_id}, début: {event.start_date}, fin: {event.end_date}, "
          f"support: {event.support_contact_id}, lieu: {event.location}, participants: {event.attendees},"
          f" notes: {event.notes}")


def display_cant_create_event(contract):
    raise ClickException(f"Désolé, le contrat (id:{contract.id}) n'est pas signé, nous ne pouvons pas créer un événement.")


def display_event_created(event):
    print(f"L'événement {event.id} a été créé avec succès.")


def display_error_event_date(start_date, end_date):
    raise ClickException(f"La date de fin {end_date} ne peut pas être antérieure à la date de début {start_date}.")


def display_event_deleted():
    print("Cet événement a été supprimé avec succès.")


def display_event_contact_updated(event, contact):
    print(f"{contact.name} est maintenant responsable de l'événement {event.id}")


def display_event_updated(event):
    print(f"Id: {event.id}, contrat: {event.contract_id}, début: {event.start_date}, fin: {event.end_date}, "
          f"support: {event.support_contact_id}, lieu: {event.location}, participants: {event.attendees},"
          f" notes: {event.notes}")


def display_missing_data():
    raise ClickException("Données manquantes dans la commande")


def display_exception(e):
    raise ClickException(f"Erreur : {e}") from e


def display_no_data_to_update():
    raise ClickException("Impossible de mettre à jour sans données dans la commande.")


def display_not_authorized():
    raise ClickException("Désolé, vous n'êtes pas autorisé.")


def display_roles_list(roles):
    print(roles)


def display_user_already_exists(email):
    raise ClickException(f"[red]Erreur:[/red] L'utilisateur ({email}) existe déjà.")


def display_incorrect_role(role):
    raise ClickException(f"[red]Erreur:[/red] {role} n'est pas un rôle correct.")


def display_user_created(email):
    print(f"[bold green]Succès:[/bold green] L'utilisateur {email} a été créé avec succès.")


def display_unknown_user():
    raise ClickException("[red]Erreur:[/red] Désolé, cet utilisateur n'existe pas.")


def display_user_data(data):
    for key, value in data.items():
        print(f"[bold]{key}:[/bold] {value}")


def display_user_updated(email):
    print(f"[bold green]Succès:[/bold green] L'utilisateur {email} a été mis à jour avec succès.")


def display_user_deleted():
    print("[bold green]Succès:[/bold green] Cet utilisateur a été supprimé avec succès.")


def display_users_list(users):
    for user in users:
        print(f"Id: {user.id}, nom: {user.name}, email: {user.email}, rôle: {user.role}")