from santa.core.draw import generate_draw

import pytest


@pytest.mark.parametrize(
    "users,exclusions",
    [
        (list(range(5)), {}),
        (list(range(5)), {3: [4]}),
        (list(range(5)), {1: [2], 2: [3], 3: [4], 0: [1]}),
    ]
)
def test_draw(users, exclusions):
    targets = set()
    recipients = set()
    res = generate_draw(users, exclusions)
    print(f"{res = }")
    for a, b in res:
        assert b not in exclusions.get(a, [])
        assert a != b
        assert b not in targets
        assert a not in recipients
        targets.add(b)
        recipients.add(a)