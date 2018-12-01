import requests
from pushbullet import Pushbullet
from argparse import ArgumentParser

class Upinator:
    def __init__(self, args):
        self.pb = Pushbullet(args["pushbullet"])
        self.cred = args["user"].split(":")
        self.domain = args["domain"]

    def get_urls(self):
        response = requests.get(self.domain, auth=(self.cred[0], self.cred[1]))
        data = respone.json()

        frontends = {**data["docker"]["frontends"], **data["file"]["frontends"]}

        urls = []
        for frontend in frontends:
            values = frontends[frontend]["routes"].values()
            for v in values:
                url = "https://" + v["rule"][5:]
                urls.append(url)


        for url in urls:
            response = requests.get(url)
            print(url, " ", response.status_code)
            if response.status_code not in [200, 401]:
                print(url, " is DOWN")

#push = pb.push_note("test", "test")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--pushbullet", required=True, help="pushbullet API token")
    parser.add_argument("-u", "--user", required=True, help="user:password")
    parser.add_argument("-d", "--domain", required=True, help="Traefiks url...")
    args = parser.parse_args()
    print(vars(args)["domain"])
    up = Upinator(vars(args))
