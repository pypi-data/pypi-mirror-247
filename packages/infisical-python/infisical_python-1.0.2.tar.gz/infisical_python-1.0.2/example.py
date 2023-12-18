from infisical_client.infisical_client import  InfisicalClient, GetSecretOptions, ClientSettings

settings = ClientSettings(
    client_id="client_id",
    client_secret="client_secret",
)

client = InfisicalClient(settings)

client.getSecret(options=GetSecretOptions(
    environment="dev",
    project_id="sdfsdfd",
    secret_name="sdfsdfs"
))