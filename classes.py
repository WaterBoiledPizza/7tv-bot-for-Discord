import requests
import json
import os
from types import SimpleNamespace
import time

class Emote:
    def __init__(self,id, size):
        self.id = id
        self.url = f"https://7tv.io/v3/emotes/{id}"

        if size < 1:
            print("The size is not in range. Changed to size 1")
            self.size = 1
        elif size > 4:
            print("The size is not in range. Changed to size 4")
            self.size = 4
        else: self.size = size


        response = requests.get(self.url)

        self.info = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        if hasattr(self.info, 'message'):
            self.message = f"Error {self.info.status}: {self.info.message}"

        self.isAnimated = not (self.info.host.files[0].frame_count == 1)

        self.file_path = ""
        # self.mime = ""
        self.output_folder = ""

        self.startTime = 0
        self.currTime = 0

    def getFile(self):
        #Download as PNG
        filename = f"{self.info.name}_{self.size}x.png"
        self.file_path = os.path.join(self.output_folder, filename)
        # emote_url = self.info.host.urls[self.size-1][1]+ ".png"
        emote_url = f"https:{self.info.host.url}/{self.size}x.png"
        r = requests.get(emote_url, stream=True)
        if r.ok:
            print("Downloading reference...")
            with open(self.file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024 * 8):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())

        else:  # HTTP status code 4XX/5XX Download as gif
            filename = f"{self.info.name}_{self.size}x.gif"
            self.file_path = os.path.join(self.output_folder, filename)
            emote_url = f"https:{self.info.host.url}/{self.size}x.gif"
            r = requests.get(emote_url, stream=True)
            if r.ok:
                print("Downloading reference...")
                with open(self.file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            os.fsync(f.fileno())

            else:  # HTTP status code 4XX/5XX
                print("Download failed: status code {}\n{}".format(r.status_code, r.text))
        self.currTime = time.time()
        print(f"Download finished. ({self.currTime - self.startTime} seconds)")

    def download(self,output_folder):
        if hasattr(self.info, 'message'):
            return
        self.output_folder = output_folder
        self.startTime = time.time()
        self.getFile()

class Channel:
    def __init__(self,name):
        self.url = f"https://api.7tv.app/v2/users/{name}"
        response = requests.get(self.url)
        self.info = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
        self.name = self.info.display_name
        self.id = self.info.id

        emoteurl = f"https://api.7tv.app/v2/users/{name}/emotes"
        response = requests.get(emoteurl)
        self.info = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
        self.list = []

    def findEmotes(self,emote,exact= True):
        for i in self.info:
            if (emote in (i.name).lower() and not exact) or (emote == i.name and exact):
                self.list.append(i)
        return(self.list)

    def findEmotesByTags(self,tag):
        for i in self.info:
            if tag in i.tags:
                self.list.append(i)
        return(self.list)

    def getEmotes(self,emote, size, output_folder,exact= True):
        for i in self.findEmotes(emote, exact):
            e = Emote(i.id, size)
            e.download(output_folder)

if __name__ == "__main__":
    # me = Channel("60ae3c29b2ecb015051f8f9a")
    # print(me.name)
    me = Emote("60abf171870d317bef23d399",size=4)
    print(me.isAnimated)
