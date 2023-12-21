# SPDX-FileCopyrightText: 2023-present Jonathan Treffler <mail@jonathan-treffler.de>
#
# SPDX-License-Identifier: MIT


def get_token():
    path = "/etc/salt/infisical.token"    
    f = open(path, "r")
    token = ""

    try:
        token = f.readlines()
    finally:
        f.close()
        return token

def get_client():
    from infisical import InfisicalClient
    return InfisicalClient(token = get_token())

def fetch_infisical_secrets(
        environment: str = "dev",
        path: str = "/",
    ):
    client = get_client()
    salt = { 'infisical': {} }
    salt["infisical"][environment] = client.get_all_secrets(environment=environment, path=path)

def fetch_infisical_secret(
        secret_name: str,
        environment: str = "dev",
        path: str = "/",
    ):
    salt = { 'infisical': {} }
    salt["infisical"][environment] = {}
    salt["infisical"][environment][secret_name] = client.get_secret(secret_name=secret_name, environment=environment, path=path)
