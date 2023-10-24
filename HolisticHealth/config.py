import pathlib

from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    environments=True,
    envvar_prefix="HHCONF",
    root_path=str(pathlib.Path(__file__).parent.absolute()),
    settings_files=["settings.toml", ".secrets.toml"],
)
