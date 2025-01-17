import json

from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from app.core.config import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
if settings.credentials_file:
    INFO = json.load(open(settings.credentials_file))
else:
    # в случае ошибки при попытке создания таблицы,
    # стоит добавить для параметра private_key метод replace('\\n', '\n')
    INFO = {
        'type': settings.type,
        'project_id': settings.project_id,
        'private_key_id': settings.private_key_id,
        'private_key': settings.private_key,
        'client_email': settings.client_email,
        'client_id': settings.client_id,
        'auth_uri': settings.auth_uri,
        'token_uri': settings.token_uri,
        'auth_provider_x509_cert_url': settings.auth_provider_x509_cert_url,
        'client_x509_cert_url': settings.client_x509_cert_url,
    }
creds = ServiceAccountCreds(**INFO, scopes=SCOPES)


async def get_service():
    async with Aiogoogle(service_account_creds=creds) as aiogoogle:
        yield aiogoogle
