"""S1: nonce words on the Mac. One close rendition is enough. No HTTP."""


def _words(text: str) -> list[str]:
    out = []
    for raw in text.split():
        w = raw.strip(".,!?;:\"'").lower()
        if w:
            out.append(w)
    return out


def _edits(a: list[str], b: list[str]) -> int:
    dp = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, dp[0] = dp[0], i
        for j, y in enumerate(b, 1):
            cur = dp[j]
            dp[j] = prev if x == y else 1 + min(prev, dp[j], dp[j - 1])
            prev = cur
    return dp[-1]


def s1(transcript: str, nonce: str) -> bool:
    """True if one stretch is the nonce with a few Whisper mistakes, order kept."""
    need = _words(nonce)
    got = _words(transcript)
    if not need:
        return False
    n = len(need)
    slack = 0 if n < 4 else max(1, n // 4)
    if len(got) < len(need):
        return False
    # windows at least as long as the nonce so a swap cannot look like a 1-delete prefix
    hi = len(need) + slack + 2
    return any(
        _edits(need, got[i : i + w]) <= slack
        for i in range(len(got) - len(need) + 1)
        for w in range(len(need), min(hi, len(got) - i) + 1)
    )
