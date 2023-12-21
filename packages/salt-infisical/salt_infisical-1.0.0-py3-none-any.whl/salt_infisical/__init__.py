# SPDX-FileCopyrightText: 2023-present Jonathan Treffler <mail@jonathan-treffler.de>
#
# SPDX-License-Identifier: MIT


def get_token():
    path = "/etc/salt/infisical.token"    
    f = open(path, "r")
    token = ""

    try:
        token = f.readline().strip('\n')
    finally:
        f.close()
        return token

def get_client():
    from infisical import InfisicalClient
    return InfisicalClient(token = get_token(), debug=True)

def secret_bundle_to_dict(secret_bundle):
    result = {}
    result[getattr(secret_bundle, "secret_name")] = getattr(secret_bundle, "secret_value")
    return result

def secret_bundles_to_dict(secret_bundles):
    result = {}
    for secret_bundle in secret_bundles:
        result[getattr(secret_bundle, "secret_name")] = getattr(secret_bundle, "secret_value")
    return result

def fetch_infisical_secrets(
        environment: str = "dev",
        path: str = "/",
    ):
    client = get_client()
    subdirectories = path.strip("/").split("/")

    secrets = {}
    for item in subdirectories[::-1]:
        if not secrets:
            secrets[item] = secret_bundles_to_dict(client.get_all_secrets(environment=environment, path=path))
        else:
            tmp = {}
            tmp[item] = secrets.copy()
            secrets = dict(tmp)

    salt = { 'infisical': {} }
    salt["infisical"][environment] = secrets

    return salt

def fetch_infisical_secret(
        secret_name: str,
        environment: str = "dev",
        path: str = "/",
    ):
    client = get_client()
    subdirectories = path.strip("/").split("/")

    secrets = {}
    for item in subdirectories[::-1]:
        if not secrets:
            secrets[item] = secret_bundle_to_dict(client.get_secret(secret_name=secret_name, environment=environment, path=path))
        else:
            tmp = {}
            tmp[item] = secrets.copy()
            secrets = dict(tmp)

    salt = { 'infisical': {} }
    salt["infisical"][environment] = secrets

    return salt
