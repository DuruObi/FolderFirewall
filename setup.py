from setuptools import setup, find_packages

setup(
    name="folderfirewall",
    version="5.0.0",
    description="CLI-based sandbox firewall for scanning and isolating untrusted folders",
    author="DuruObi",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer",
        "rich",
        "docker",
        "watchdog"
    ],
    entry_points={
        "console_scripts": [
            "folderfirewall=folderfirewall.cli:app"
        ]
    },
)
