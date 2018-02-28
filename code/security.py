users = [
    {
        'id': 1,
        'username': 'bob',
        'password': 'omg'
    }
]

username_mapping = { 'bob': {
        'id': 1,
        'username': 'bob',
        'password': 'omg'
    }
}

userid_mapping = { 1: {
        'id': 1,
        'username': 'bob',
        'password': 'omg'
    }
}

authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
