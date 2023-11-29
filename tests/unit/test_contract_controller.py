from click import ClickException
from click.testing import CliRunner
from sqlalchemy import select

import pytest

from epic_events.controllers.contract_controller import (list_contracts, delete_contract, get_contract,
                                                         update_contract, create_contract, check_amount)
from epic_events.models import User, Contract



@pytest.mark.parametrize("filter_option, expected_count", [
    (None, 2),
    ("-s SIGNED", 1)
])
def test_list_contract(mocked_session, filter_option, expected_count):
    current_user = mocked_session.scalar(select(User).where(User.id == 1))
    options = [] if filter_option is None else filter_option.split()
    runner = CliRunner()
    result = runner.invoke(list_contracts, options, obj={"session": mocked_session, "current_user": current_user})
    assert result.exit_code == 0
    assert expected_count == result.output.count("Id")


class TestUpdateContractController:
    runner = CliRunner()

    @pytest.mark.parametrize("contract_id, amount, left_to_pay, status", [
        (2, 90, 10, "SIGNED")
    ])
    def test_update_contract_with_correct_argument(self, mocked_session, contract_id, amount, left_to_pay, status):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        updated_contract = mocked_session.scalar(select(Contract).where(Contract.id == contract_id))
        assert updated_contract.total_amount == 100
        assert updated_contract.status == "UNSIGNED"
        options = ["-id", contract_id, "-a", amount, "-ltp", left_to_pay, "-s", status]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 0
        assert all(arg in result.output for arg in [str(contract_id), str(amount), str(left_to_pay), status])
        assert updated_contract.status == status
        assert updated_contract.total_amount == amount


class TestGetContractController:
    runner = CliRunner()

    @pytest.mark.parametrize("contract_id", [
        1
    ])
    def test_get_contract_with_correct_argument(self, mocked_session, contract_id):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", contract_id]
        result = self.runner.invoke(get_contract, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 0
        assert f"Id: {contract_id}" in result.output


class TestDeleteContractController:
    runner = CliRunner()

    @pytest.mark.parametrize("contract_id", [
        1
    ])
    def test_delete_contract_with_unknown_contract(self, mocked_session, contract_id):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", contract_id]
        result = self.runner.invoke(delete_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this contract does not exist." in result.output


class TestCreateContractController:
    runner = CliRunner()

    @pytest.mark.parametrize("client_id, amount", [
        (777, 100)
    ])
    def test_create_contract_with_unknown_client(self, mocked_session, client_id, amount):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-client", client_id, "-a", amount]
        result = self.runner.invoke(create_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this client does not exist." in result.output

    @pytest.mark.parametrize("client_id, amount", [
        (1, 100)
    ])
    def test_create_contract_with_correct_argument(self, mocked_session, client_id, amount):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-client", client_id, "-a", amount]
        result = self.runner.invoke(create_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 0
        assert "Contract 3 is successfully created." in result.output



class TestCreateContractController:
    runner = CliRunner()

    def test_create_contract_with_unknown_client(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-client", 777, "-a", 100]
        result = self.runner.invoke(create_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this client does not exist." in result.output

    def test_create_contract_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-client", 1, "-a", 100]
        result = self.runner.invoke(create_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 0
        assert "Contract 3 is successfully created." in result.output


class TestUpdateContractController:
    runner = CliRunner()

    def test_update_contract_without_optional_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 1]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Can't update without data in the command." in result.output

    def test_update_contract_with_unknown_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777, "-s", "SIGNED"]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this contract does not exist." in result.output

    def test_update_contract_with_unauthorized_user(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 4))
        options = ["-id", 1, "-s", "SIGNED"]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, you're not authorized." in result.output

    def test_update_contract_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 3))
        contract_id = 2
        amount = 90
        left_to_pay = 10
        status = "SIGNED"
        updated_contract = mocked_session.scalar(select(Contract).where(Contract.id == contract_id))
        assert updated_contract.total_amount == 100
        assert updated_contract.status == "UNSIGNED"
        options = ["-id", contract_id, "-a", amount, "-ltp", left_to_pay, "-s", status]
        result = self.runner.invoke(update_contract, options, obj={"session": mocked_session,
                                                                   "current_user": current_user})
        assert result.exit_code == 0
        assert [arg in result.output for arg in [str(contract_id), str(amount), str(left_to_pay), status]]
        assert updated_contract.status == status
        assert updated_contract.total_amount == amount


class TestGetContractController:
    runner = CliRunner()

    def test_get_contract_with_unknown_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777]
        result = self.runner.invoke(get_contract, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this contract does not exist." in result.output

    def test_get_contract_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        contract_id = 1
        options = ["-id", contract_id]
        result = self.runner.invoke(get_contract, options, obj={"session": mocked_session,
                                                                "current_user": current_user})
        assert result.exit_code == 0
        assert f"Id: {contract_id}" in result.output


class TestDeleteContractController:
    runner = CliRunner()

    def test_delete_contract_with_unknown_contract(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 777]
        result = self.runner.invoke(delete_contract, options, input="y", obj={"session": mocked_session,
                                                                              "current_user": current_user})
        assert result.exit_code == 1
        assert "Sorry, this contract does not exist." in result.output

    def test_delete_contract_with_correct_argument(self, mocked_session):
        current_user = mocked_session.scalar(select(User).where(User.id == 1))
        options = ["-id", 1]
        result = self.runner.invoke(delete_contract, options, input="y", obj={"session": mocked_session,
                                                                              "current_user": current_user})
        assert result.exit_code == 0
        assert "This contract is successfully deleted." in result.output


class TestCheckAmount:

    @pytest.mark.parametrize("amount, left_to_pay", [
        (100, 50)
    ])
    def test_check_amount_with_correct_argument(self, amount, left_to_pay):
        result = check_amount(amount, left_to_pay)
        assert result is True

    @pytest.mark.parametrize("amount, left_to_pay", [
        (100, 200)
    ])
    def test_check_amount_with_left_to_pay_bigger_than_amount(self, amount, left_to_pay):
        error = ("Total amount and left to pay must be positive integer and left to pay can't be bigger "
                 "than total amount.")
        with pytest.raises(ClickException) as e:
            check_amount(amount, left_to_pay)
        assert error in str(e.value)
