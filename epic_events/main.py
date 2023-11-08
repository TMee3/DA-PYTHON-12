from getpass import getpass

import click
from rich.console import Console
from rich.table import Table
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from models.base import Base, Collaborator

# Assuming your database URL is set correctly
engine = create_engine('sqlite:///epic_events.db')
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)  # This creates the tables in your database


console = Console()

@click.group()
def cli():
    pass

@cli.group()
def collaborator():
    pass

"""
Ce script contient une commande CLI pour ajouter un nouveau collaborateur à la base de données.

La commande prend les paramètres suivants:
- username: Nom d'utilisateur unique du collaborateur
- name: Prénom du collaborateur
- surname: Nom de famille du collaborateur
- email: Adresse email du collaborateur
- telephone: Numéro de téléphone du collaborateur (optionnel)

La commande utilise la bibliothèque Click pour gérer les options de ligne de commande.
"""
@collaborator.command()
@click.option('--username', prompt=True)
@click.option('--name', prompt=True)
@click.option('--surname', prompt=True)
@click.option('--email', prompt=True)
@click.option('--telephone', default=None)
def add(username, name, surname, email, telephone):
    session = Session()
    collaborator = session.query(Collaborator).filter_by(username=username).first()
    if collaborator:
        console.print(f"[bold red]Le nom d'utilisateur {username} existe déjà.[/bold red]")
        return
    password = generate_password_hash(getpass('Mot de passe : '))  # Demande sécurisée du mot de passe
    new_collaborator = Collaborator(
        username=username,
        password=password,
        name=name,
        surname=surname,
        email=email,
        telephone=telephone,
   
    )
    session.add(new_collaborator)
    try:
        session.commit()
        console.print("[bold green]Collaborateur ajouté avec succès.[/bold green]")
    except Exception as e:
        session.rollback()
        console.print(f"[bold red]Une erreur est survenue : {e}[/bold red]")
    finally:
        session.close()

@collaborator.command()
@click.option('--username', prompt=True)
def get(username):
    """Get a collaborator from the database."""
    session = Session()
    collaborator = session.query(Collaborator).filter_by(username=username).first()
    if collaborator:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Username")
        table.add_column("Name")
        table.add_column("Surname")
        table.add_column("Email")
        table.add_column("Telephone")
        table.add_row(collaborator.username, collaborator.name, collaborator.surname, collaborator.email, collaborator.telephone)
        console.print(table)
    else:
        console.print(f"[bold red]Collaborator not found with username {username}[/bold red]")
    session.close()

@collaborator.command()
def list():
    """List all collaborators in the database."""
    session = Session()
    collaborators = session.query(Collaborator).all()
    if collaborators:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Username")
        table.add_column("Name")
        table.add_column("Surname")
        table.add_column("Email")
        table.add_column("Telephone")
        for collaborator in collaborators:
            table.add_row(collaborator.username, collaborator.name, collaborator.surname, collaborator.email, collaborator.telephone)
        console.print(table)
    else:
        console.print("[bold yellow]No collaborators found.[/bold yellow]")
    session.close()

@collaborator.command()
@click.option('--username', prompt=True)
def delete(username):
    """Delete a collaborator from the database."""
    session = Session()
    collaborator = session.query(Collaborator).filter_by(username=username).first()
    if collaborator:
        session.delete(collaborator)
        session.commit()
        console.print(f"[bold green]Collaborator {username} deleted successfully.[/bold green]")
    else:
        console.print(f"[bold red]Collaborator not found with username {username}[/bold red]")
    session.close()

@collaborator.command()
@click.option('--username', prompt=True)
@click.option('--name', prompt=True)
@click.option('--surname', prompt=True)
@click.option('--email', prompt=True)
@click.option('--telephone', default=None)
def update(username, name, surname, email, telephone):
    """Update a collaborator in the database."""
    session = Session()
    collaborator = session.query(Collaborator).filter_by(username=username).first()
    if not collaborator:
        console.print(f"[bold red]Collaborator not found with username {username}[/bold red]")
        return
    collaborator.name = name
    collaborator.surname = surname
    collaborator.email = email
    collaborator.telephone = telephone
    try:
        session.commit()
        console.print(f"[bold green]Collaborator {username} updated successfully.[/bold green]")
    except Exception as e:
        session.rollback()
        console.print(f"[bold red]An error occurred: {e}[/bold red]")
    finally:
        session.close()

if __name__ == '__main__':
    cli()
