from click import ClickException


def display_contracts_list(contracts):
    for contract in contracts:
        print(f"Id: {contract.id}, client: {contract.client_id}, amount: {contract.total_amount}, "
              f"left to pay: {contract.left_to_pay}, status: {contract.status}")


def display_contract_created(contract):
    print(f"Contract {contract.id} is successfully created.")


def display_contract_data(contract):
    print(f"Id: {contract.id}, client: {contract.client_id}, amount: {contract.total_amount}, "
          f"left to pay: {contract.left_to_pay}, status: {contract.status}")


def display_unknown_contract():
    raise ClickException("Sorry, this contract does not exist.")


def display_contract_deleted():
    print("This contract is successfully deleted.")


def display_contract_updated(contract):
    print(f"Id: {contract.id}, client: {contract.client_id}, amount: {contract.total_amount}, "
          f"left to pay: {contract.left_to_pay}, status: {contract.status}")


def display_error_amount():
    raise ClickException("Total amount and left to pay must be positive integer and left to pay can't be bigger "
                         "than total amount.")
