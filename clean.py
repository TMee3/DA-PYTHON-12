import subprocess


def run_flake8():
    """
    Runs Flake8 to check for PEP 8 compliance in the code.
    """
    print("Running Flake8...")
    subprocess.run(["flake8", "."], check=False)


def run_black():
    """
    Runs Black to check for PEP 8 compliance in the code.

    """
    print("Running Black...")
    subprocess.run(["black", "."], check=False)


def run_isort():
    """
    Runs isort to check for PEP 8 compliance in the code.
    """

    print("Running isort...")
    subprocess.run(["isort", "."], check=False)


if __name__ == "__main__":
    run_flake8()
    run_black()
    run_isort()
