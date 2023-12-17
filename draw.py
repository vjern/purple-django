from dataclasses import dataclass
import random


UserId = str
@dataclass
class User:
    id: UserId
    name: str


@dataclass
class Ban:
    recipient: str
    target: str


def draw(
    users: list[UserId],
    bans: dict[UserId, set[UserId]],
) -> list[tuple[UserId, UserId]]:
    pool = list(range(len(users)))
    for i, u in enumerate(users):
        # draw another user as target of secret santa
        if not pool: # no more users to draw from
            raise RuntimeError
        target_idx = i
        attempts = 100
        while target_idx == i or users[target_idx] in bans.get(u, []):
            if not attempts:
                raise RuntimeError('Unable to draw, try again or loosen bans')
            attempts -= 1
            target_idx_idx = random.randrange(len(pool))
            target_idx = pool[target_idx_idx]
        pool.pop(target_idx_idx)
        yield (u, users[target_idx])


def test_draw():

    users = list(range(10))
    bans = {0: {1, 2, 3, 4, 5, 6, 8, 9}}

    res = draw(users, bans)
    res = list(res)
    print(f"{res = }")

    for a, b in res:
        assert b not in bans.get(a, [])


if __name__ == '__main__':
    test_draw()
