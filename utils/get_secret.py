from google.cloud import secretmanager
import logging

logging.basicConfig(level=logging.DEBUG)


def get_secret(secret_id):
    project_id = "tft-stocks"
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')