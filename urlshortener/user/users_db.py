from ..client.inmemoryclient import InMemoryClient

client = InMemoryClient()

client.set('johndoe@example.com', {
    "email": "johndoe@example.com",
    "hashed_password": "$2b$12$TtB2fBC0v4K1PfCwteiSD.Pd9Xuopkbl3K2hFll5/rj6wZw3yVzuW",
})

client.set('alice@example.com', {
    "email": "alice@example.com",
    "hashed_password": "$2b$12$1uAZBYM2t7NmBDuS67j.P.lln1SDnTcb5ZTp.yfxkuDBbrJZYuy.y",
})


def users_db():
    return client
