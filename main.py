import json
import requests
from faker import Faker
import random
import sys
import time
import json

with open("config.json", "r") as f:
    config = json.load(f)

class Dashboard:
    def __init__(self) -> None:
        proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
        self.session = requests.Session()
        self.session.proxies = {'http': 'http://' + proxy}

    def generator(self, cookie: str) -> str:
        self.session.cookies['.ROBLOSECURITY'] = cookie
        
        token = self.session.post("https://auth.roblox.com/v2/logout").headers["X-CSRF-TOKEN"]

        self.session.headers['x-csrf-token'] = token
        self.session.headers['user-agent'] = 'Roblox'

        user_id = self.session.get("https://users.roblox.com/v1/users/authenticated").json()['id']]

        game_id = self.session.get(f"https://inventory.roblox.com/v2/users/{user_id}/inventory/9",
                                   params={'limit': '10',
                                           'sortOrder': 'Asc'}).json()["data"][0]["assetId"]

        universe_id = self.session.get(f"https://apis.roblox.com/universes/v1/places/{game_id}/universe").json()["universeId"]

        try:
            r = self.session.post("https://apis.roblox.com/cloud-authentication/v1/apiKey",
                        json={'cloudAuthUserConfiguredProperties': {'name': Faker().word().capitalize(),
                                                                 'description': Faker().word().capitalize(),
                                                                 'isEnabled': True,
                                                                 'allowedCidrs': ['0.0.0.0/0'],
                                                                 'scopes': [{'scopeType': "asset",
                                                                             'targetParts': ["U"],
                                                                             'operations': ["read","write"]
                                                                             },
                                                                            {'scopeType': "user.advanced",
                                                                             'targetParts': ["*"],
                                                                             'operations': ["read"]},
                                                                            {'scopeType': "user.social",
                                                                             'targetParts': ["*"],
                                                                             'operations': ["read"]},
                                                                            {'scopeType': "group",
                                                                             'targetParts': ["*"],
                                                                             'operations': ["read", "write"]},
                                                                            {'scopeType': "user.inventory-item",
                                                                             'targetParts': ["*"],
                                                                             'operations': ["read"]},
                                                                            {'scopeType': "universe",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["write"]},
                                                                            {'scopeType': "universe.place",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["write"]},
                                                                            {'scopeType': "user.user-notification",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["write"]},
                                                                            {'scopeType': "universe.place.instance",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["read", "write"]},
                                                                            {'scopeType': "universe.user-restriction",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["read", "write"]},
                                                                            {'scopeType': "universe.ordered-data-store.scope.entry",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["read", "write"]},
                                                                            {'scopeType': "universe-datastores.objects",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["read", "create", "update", "delete", "list"]},
                                                                            {'scopeType': "universe-datastores.versions",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["read", "list"]},
                                                                            {'scopeType': "universe-datastores.control",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["list", "create"]},
                                                                            {'scopeType': "universe-messaging-service",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["publish"]},
                                                                            {'scopeType': "universe-places",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["write"]}
                                                                            ]
                                                                 }
                                }
                        ).json()

        except json.JSONDecodeError as e:
            raise Exception(f"Too many API Keys, switch account: {e}")

        with open("keys.txt", "a") as f:
            f.write(r["apikeySecret"] + "\n")

        return f"API Key: {r["apikeySecret"]}"

if __name__ == "__main__":
    while True:
        print(Dashboard().generator(config["cookie"]))
