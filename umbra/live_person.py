"""Current roster person. Empty until someone enrolls on this laptop."""
from pathlib import Path

HERE = Path(__file__).resolve().parent


def live_id() -> str:
    from umbra.roster import Roster

    try:
        ids = list(Roster(HERE / "roster_data").ids())
    except Exception:
        return ""
    return ids[-1] if ids else ""


LIVE_ID = ""
