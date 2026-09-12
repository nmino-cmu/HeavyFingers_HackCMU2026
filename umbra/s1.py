"""S1: exact nonce words in order. Mac-local. No HTTP."""


def _words(text: str) -> list[str]:
    out = []
    for raw in text.split():
        w = raw.strip(".,!?;:\"'").lower()
        if w:
            out.append(w)
    return out


def s1(transcript: str, nonce: str) -> bool:
    """True iff nonce words appear exactly, in order (case/punct ignored)."""
    need = _words(nonce)
    got = _words(transcript)
    if not need:
        return False
    n = len(need)
    return any(got[i : i + n] == need for i in range(len(got) - n + 1))
