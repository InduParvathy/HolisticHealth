import pathlib

from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    validators=[
        Validator(
            "production",
            "access_logs",
            is_type_of=bool,
            required=True,
        ),
        Validator(
            "api_secret", "database_uri", "sentry_dsn", is_type_of=str, required=True
        ),
        Validator(
            "log_level",
            is_in=["debug", "info", "warning", "error", "critical"],
            required=True,
        ),
    ],
    envvar_prefix="",
    root_path=str(pathlib.Path(__file__).parent.absolute()),
    settings_files=["settings.toml", ".secrets.toml"],
)
