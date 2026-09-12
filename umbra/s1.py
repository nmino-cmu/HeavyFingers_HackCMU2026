"""S1: nonce words on the Mac. One close rendition is enough. No HTTP."""

# tiny.en regulars on this vocab — fold before edit distance.
_ALIAS = {
    "lettuce": "lattice",
    "letus": "lattice",
    "nonsam": "nonce",
    "non-sam": "nonce",
    "asterix": "asterisk",
}


def _words(text: str) -> list[str]:
    out = []
    for raw in text.split():
        w = raw.strip(".,!?;:\"'").lower()
        w = _ALIAS.get(w, w)
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
    # 4-word cards still require every token (missing "fox" must fail). 6+ can lose one to Whisper.
    min_got = n if n < 6 else n - slack
    if len(got) < min_got:
        return False
    # windows at least as long as the nonce so a swap cannot look like a 1-delete prefix
    hi = len(need) + slack + 2
    return any(
        _edits(need, got[i : i + w]) <= slack
        for i in range(0, len(got) - min_got + 1)
        for w in range(min_got, min(hi, len(got) - i) + 1)
    )
