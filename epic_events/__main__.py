from os import getenv

import sentry_sdk
from dotenv import load_dotenv

from epic_events.controllers.cli import cli


if __name__ == "__main__":
    load_dotenv()
    db_dsn = getenv("SENTRY_DSN")
    sentry_sdk.init(
        dsn=db_dsn,
        traces_sample_rate=0.5,
        profiles_sample_rate=1.0,
    )
    

    cli()
    

