import requests
from pushbullet import Pushbullet
from argparse import ArgumentParser

class Upinator:
    def __init__(self, args):
        self.pb = Pushbullet(args["pushbullet"])
        self.cred = args["user"].split(":")
        self.domain = args["domain"]
        self.saved_urls = []
        self.urls = []
        self.load_urls()  # load saved urls from disk
        self.update_urls()  # get current urls from traefik
        self.diff_urls()
        self.ping_urls(self.urls)
        self.save_urls()

    def save_urls(self, file="urls.txt"):
        with open(file, "w") as f:
            for url in self.urls:
                f.write(url+"\n")

    def load_urls(self, file="urls.txt"):
        self.saved_urls = []  # clear list
        
        try:
            with open(file, "r") as f:
                lines = f.readlines()
                for lin in lines:
                    self.saved_urls.append(lin.rstrip("\n"))
        except:
            print("No saved urls")

    def update_urls(self):
        try:
            response = requests.get(self.domain, auth=(self.cred[0], self.cred[1]))
        except:
            print("Could not update URLS")
            self.notify("Failed to update URLS", "Server down??")
            return 1
        data = response.json()

        frontends = {**data["docker"]["frontends"], **data["file"]["frontends"]}

        self.urls = []
        for frontend in frontends:
            values = frontends[frontend]["routes"].values()
            for v in values:
                url = "https://" + v["rule"][5:]
                self.urls.append(url)

    def diff_urls(self):
        print(self.urls)
        diff_urls = set(self.saved_urls) - set(self.urls)
        print(diff_urls)
        if len(diff_urls) != 0:
            print("Services lost: ", diff_urls) 
            self.notify("Services lost:", str(diff_urls))
            self.ping_urls(diff_urls)

    def ping_urls(self, urls):
        for url in urls:
            print("Pinging:", url)
            try:
                response = requests.get(url)
            except:
                respone = False
            print(url, " ", response.status_code)
            if response.status_code not in [200, 401]:
                print(url, " is DOWN")
                self.notify("Servicedown", url)

    def notify(self, title, message):
        push = self.pb.push_note(title, message)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--pushbullet", required=True, help="pushbullet API token")
    parser.add_argument("-u", "--user", required=True, help="user:password")
    parser.add_argument("-d", "--domain", required=True, help="Traefiks url...")
    args = parser.parse_args()
    print(vars(args)["domain"])
    up = Upinator(vars(args))
