import requests
from faker import Faker
import random
import sys
import time
class Dashboard:

    def __init__(self) -> None:
        proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
        if proxy == []:
            raise Exception("'proxy.txt' is empty")
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
            print(Dashboard().generator("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_36F0DBE55721D1977CD17C9A9FA30E2E816AE9BA50EB1789AC81B195B8483DF6EEF433510DC65E9E70D8950AF1B639DC344E1DDB35ABE674D6B7231215BCD2999DFEB62984E96689FB5A7E980E370CDD937C215828612ACBB21D5A898695EB511CE3EB8216FFE073DEAC4768E79FA6F6F594CCFCC2E9CE27B65287C4D3DB5FB53C890508EAEC2851D434BACD53E9E9BB9107A1B3746A12BFC678D501EE23433430500BF64D7C532CA08847B719DC7C8930392B6841B4274A29F9FA63BD5D0AC5BDEC6697BDB1B4914BCE5D22422CCB0B1720A7274FACB370B410E46BC0D3A8CBDC3C203B813E4950552211DFA6B90C6AB246BE7E0073B32CB2558BBE1F5BC2C5BAB2144437F76F1204BC0EC76F9BD54DE11A06003A93B2A4C1FB1588678238ADE33561764928AD9174A2083E92F38148C4B695B0EEC9E5837FC0EE277A0B32A5A2DC7E1F6DE329E9854B22825288A040A910969B8F0BDA8EA063F2D56964F3C608DD8B9B17BE620CF00FA1BE98C30B8070C9EFC9222D1D8DD1D6EAE1BFD0E9F19501A61C51F24CFEB1C6D09FCFE4227AC82CFA7E8329EF74033F99DD3F08CD50B96BDE993C66C6D16F6E8115732648A9F784BFFB6C358253CF634B4C540A393F5F1322361709A30CB2DE9258FB9BAD436F7D99ECD0074D86D063ED3666C7350998359507B4229EADEDD646E73F93D2A5CDCC349CAA85AE06F5C5DB7CCE643962D08C06F5DC5673964B1DA6C9075BFB211415502A969240E0C6DE7CE9C4B279C32470F7272689C67FAF2F2C7653CDDA6EF4E1743B81A5615DD6F6C819F3E6B6C653CC7458A15313524E9F3F9B0F7037D949B49C39CF7F03062B95149742130BCC6E423FB4D74A38CDD0B88F0D63D1B4178F740E6D9C48FE09F0434E2847F311D3E71FBE8685005E5D93E052502F01A9F3A6661011491B6A5C89550C1BA2167391CF9E3744A4640891AAB55FB88A8C14B71EA4035B816D6F40F25DE64A21E490E5C325EE65BB606C10013B17B5D2B6DAF4FC1D0AF1F0CFA7BC8BD74D6AC719B80D19DB00D3E7158EAE4ACCD2381CFD67741ED0DE651A7535F57CEC2E535E050C2E902E9AEF"))
        except requests.exceptions.ConnectionError:
            print(Dashboard().deleter("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_36F0DBE55721D1977CD17C9A9FA30E2E816AE9BA50EB1789AC81B195B8483DF6EEF433510DC65E9E70D8950AF1B639DC344E1DDB35ABE674D6B7231215BCD2999DFEB62984E96689FB5A7E980E370CDD937C215828612ACBB21D5A898695EB511CE3EB8216FFE073DEAC4768E79FA6F6F594CCFCC2E9CE27B65287C4D3DB5FB53C890508EAEC2851D434BACD53E9E9BB9107A1B3746A12BFC678D501EE23433430500BF64D7C532CA08847B719DC7C8930392B6841B4274A29F9FA63BD5D0AC5BDEC6697BDB1B4914BCE5D22422CCB0B1720A7274FACB370B410E46BC0D3A8CBDC3C203B813E4950552211DFA6B90C6AB246BE7E0073B32CB2558BBE1F5BC2C5BAB2144437F76F1204BC0EC76F9BD54DE11A06003A93B2A4C1FB1588678238ADE33561764928AD9174A2083E92F38148C4B695B0EEC9E5837FC0EE277A0B32A5A2DC7E1F6DE329E9854B22825288A040A910969B8F0BDA8EA063F2D56964F3C608DD8B9B17BE620CF00FA1BE98C30B8070C9EFC9222D1D8DD1D6EAE1BFD0E9F19501A61C51F24CFEB1C6D09FCFE4227AC82CFA7E8329EF74033F99DD3F08CD50B96BDE993C66C6D16F6E8115732648A9F784BFFB6C358253CF634B4C540A393F5F1322361709A30CB2DE9258FB9BAD436F7D99ECD0074D86D063ED3666C7350998359507B4229EADEDD646E73F93D2A5CDCC349CAA85AE06F5C5DB7CCE643962D08C06F5DC5673964B1DA6C9075BFB211415502A969240E0C6DE7CE9C4B279C32470F7272689C67FAF2F2C7653CDDA6EF4E1743B81A5615DD6F6C819F3E6B6C653CC7458A15313524E9F3F9B0F7037D949B49C39CF7F03062B95149742130BCC6E423FB4D74A38CDD0B88F0D63D1B4178F740E6D9C48FE09F0434E2847F311D3E71FBE8685005E5D93E052502F01A9F3A6661011491B6A5C89550C1BA2167391CF9E3744A4640891AAB55FB88A8C14B71EA4035B816D6F40F25DE64A21E490E5C325EE65BB606C10013B17B5D2B6DAF4FC1D0AF1F0CFA7BC8BD74D6AC719B80D19DB00D3E7158EAE4ACCD2381CFD67741ED0DE651A7535F57CEC2E535E050C2E902E9AEF"))
            sys.exit(0)
        except Exception as e:
            print(f"ERROR: {e}")
            sys.exit(0)
