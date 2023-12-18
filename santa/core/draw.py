from dataclasses import dataclass
import random


UserId = str
@dataclass
class User:
    id: UserId
    name: str


@dataclass
class Exclusion:
    recipient: str
    target: str


def generate_draw(
    users: list[UserId],
    exclusions: dict[UserId, set[UserId]],
) -> list[tuple[UserId, UserId]]:
    pool = list(range(len(users)))
    for i, u in enumerate(users):
        # draw another user as target of secret santa
        if not pool: # no more users to draw from
            raise RuntimeError('Unable to draw, try again or loosen exclusions')
        target_idx = i
        attempts = 100
        # TODO and also you can't be the target of someone you have in your own blacklist 
        while target_idx == i or users[target_idx] in exclusions.get(u, []):
            if not attempts:
                raise RuntimeError('Unable to draw, try again or loosen exclusions')
            attempts -= 1
            target_idx_idx = random.randrange(len(pool))
            target_idx = pool[target_idx_idx]
        pool.pop(target_idx_idx)
        yield (u, users[target_idx])


def test_draw():

    users = list(range(10))
    exclusions = {0: {1, 2, 3, 4, 5, 6, 8, 9}}

    res = generate_draw(users, exclusions)
    res = list(res)
    print(f"{res = }")
    assert dict(res)[0] == 7
    for a, b in res:
        assert b not in exclusions.get(a, [])


if __name__ == '__main__':
    test_draw()
