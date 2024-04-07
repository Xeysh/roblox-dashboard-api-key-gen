import requests
from faker import Faker
import random
import sys
import time

class Dashboard:

    def __init__(self) -> None:
        proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
        if proxy == []:
            raise Exception("'proxy.txt' is empty.")
        self.session = requests.Session()
        self.session.proxies = {'http': 'http://' + proxy.strip()}

    def generator(self, cookie: str) -> str:

        token_response = self.session.post("https://auth.roblox.com/v2/logout",
                                   cookies={".ROBLOSECURITY": cookie})
        token = token_response.headers["X-CSRF-TOKEN"]

        user_response = self.session.get("https://users.roblox.com/v1/users/authenticated",
                                    headers={'x-csrf-token': token, 'User-Agent': 'Roblox'},
                                    cookies={'.ROBLOSECURITY': cookie})
        user_data = user_response.json()

        user_id = user_data["id"]

        inventory_response = self.session.get(
            f"https://inventory.roblox.com/v2/users/{user_id}/inventory/9?limit=10&sortOrder=Asc",
            headers={'x-csrf-token': token, 'User-Agent': 'Roblox'},
            cookies={'.ROBLOSECURITY': cookie})

        inventory_data = inventory_response.json()

        game_id = inventory_data["data"][0]["assetId"]

        unvid_response = self.session.get(f"https://apis.roblox.com/universes/v1/places/{game_id}/universe")
        unvid_data = unvid_response.json()
        universe_id = unvid_data["universeId"]

        r = self.session.post("https://apis.roblox.com/cloud-authentication/v1/apiKey",
                        headers={"Content-Type": "application/json",
                              'User-Agent': 'Roblox/WinInet',
                              'x-csrf-token': token},
                        cookies={".ROBLOSECURITY": cookie},
                        json={'cloudAuthUserConfiguredProperties': {'name': Faker().word().capitalize(),
                                                                 'description': Faker().word().capitalize(),
                                                                 'isEnabled': True,
                                                                 'allowedCidrs': ['0.0.0.0/0'],
                                                                 'scopes': [{'scopeType': "universe-places",
                                                                             'targetParts': [f"{universe_id}"],
                                                                             'operations': ["write"]
                                                                             }]
                                                                 }
                                }
                        ).json()

        if 'message' in r:
            raise Exception(f"Too many API Keys, switch account: {r['message']}")

        with open("keys.txt", "a") as f:
            f.write(r["apikeySecret"] + "\n")

        return f"API Key: {r["apikeySecret"]}"

    def deleter(self, cookie: str) -> str:
        token_response = self.session.post("https://auth.roblox.com/v2/logout",
                                   cookies={".ROBLOSECURITY": cookie})
        token = token_response.headers["X-CSRF-TOKEN"]

        key = random.choice(open("keys.txt", "r").readlines()).strip()
        self.session.delete(f"https://apis.roblox.com/cloud-authentication/v1/apiKey/{key}",
                        headers={'Content-Type': 'application/json',
                                 'User-Agent': 'Roblox/WinInet',
                                 'x-csrf-token': token},
                        cookies={".ROBLOSECURITY": cookie},
                        )
        return f"Deleted an API key: {key}"

if __name__ == "__main__":
    while True:
        time.sleep(1)
        try:
            print(Dashboard().generator("YOUR_ROBLOX_ACCOUNT_COOKIE"))
        except requests.exceptions.ConnectionError:
            print(Dashboard().deleter("YOUR_ROBLOX_ACCOUNT_COOKIE"))
            sys.exit(0)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(1)
