from click.testing import CliRunner
from main import collaborator, add
from faker import Faker

def test_add_success():
    fake = Faker()
    runner = CliRunner()
    password = fake.password()
    result = runner.invoke(collaborator, ['add'], input=f'{fake.first_name()}\n{fake.last_name()}\n{fake.user_name()}\n{fake.email()}\n{password}\n')
    assert result.exit_code == 0
    assert 'Collaborateur ajouté avec succès.' in result.output



print(test_add_success())



    