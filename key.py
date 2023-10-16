import secrets
import string


def generate_secret_key():
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()_+'
    return ''.join(secrets.choice(alphabet) for _ in range(24))

secret_key = generate_secret_key()
print(f'Secret Key: {secret_key}')
