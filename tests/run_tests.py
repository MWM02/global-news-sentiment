import sys
import subprocess


def main():
    command = sys.argv[1]

    test_config = {
        "unit": {"dir": "tests/unit_tests", "cov": ["config", "src"]},
    }

    if command in test_config:
        test_dir = test_config[command]["dir"]
        cov_sources = ",".join(test_config[command]["cov"])

        if cov_sources:
            cov_command = (
                f"ENV=test coverage run --source={cov_sources} "
                f"--omit=*/__init__.py -m pytest --verbose {test_dir} "
                "&& coverage report -m && coverage html "
                "&& coverage report --fail-under=90"
            )
        else:
            cov_command = f"ENV=test pytest --verbose {test_dir}"

        if command == "all":
            run_lint()

        subprocess.run(cov_command, shell=True)
    elif command == "lint":
        run_lint()
    else:
        raise ValueError(f"Unknown command: {command}")


def run_lint() -> None:
    print("Running linting for Python files")
    print("Linting Python...")
    subprocess.run(["flake8", "."])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Usage: run_tests.py <unit|component|e2e|all|lint>")
    else:
        main()
