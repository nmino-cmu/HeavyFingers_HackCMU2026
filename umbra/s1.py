"""S1: exact-order nonce in a local transcript. No network."""


def s1(transcript: str, nonce: str) -> bool:
    words = [w.strip(".,!?;:\"'").lower() for w in transcript.split() if w.strip(".,!?;:\"'")]
    need = [w.lower() for w in nonce.split() if w]
    if not need:
        return False
    i = 0
    for w in words:
        if w == need[i]:
            i += 1
            if i == len(need):
                return True
    return False
