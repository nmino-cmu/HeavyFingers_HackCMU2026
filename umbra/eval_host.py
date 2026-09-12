"""Where FHE eval runs for the current build."""
import os


def get_eval_host() -> str:
    return os.environ.get("UMBRA_EVAL_HOST", "vultr").strip().lower()


def is_vultr() -> bool:
    return get_eval_host() == "vultr"
