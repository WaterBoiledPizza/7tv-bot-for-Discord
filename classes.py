import requests
import json
import os
import glob
from PIL import Image, ImageSequence, features
from wand.image import Image as Img
from types import SimpleNamespace
import time

dest_folder = "out"

class Emote:
    def __init__(self,id, size):
        self.id = id
        self.url = f"https://api.7tv.app/v2/emotes/{id}"

        if size < 1:
            print("The size is not in range. Changed to size 1")
            self.size = 1
        elif size > 4:
            print("The size is not in range. Changed to size 4")
            self.size = 4
        else: self.size = size

        response = requests.get(self.url)
        self.info = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
        self.file_path = ""
        self.mime = ""
        self.output_folder = ""

        self.startTime = 0
        self.currTime = 0

    def getFile(self):
        self.mime = self.info.mime[6:]
        filename = f"{self.info.name}_{self.size}x.{self.mime}"
        if self.mime == "webp": self.file_path = os.path.join("tmp", filename)
        else: self.file_path = os.path.join(self.output_folder, filename)
        emote_url = self.info.urls[self.size-1][1]
        r = requests.get(emote_url, stream=True)
        if r.ok:
            print("Downloading emote...")
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

    def getFrames(self):
        try:
            MediaFile = Image.open(self.file_path)
            Index = 0
            for frame in ImageSequence.Iterator(MediaFile):
                # frame.save(f"out/frame{Index}.png")
                Index += 1
            #print(Index)
            return Index
        except:  # If the .webp can't be opened then it is most likely not a .gif or .webp
            return False

    def getDuration(self):
        dur = 0
        num = self.getFrames()
        with Img(filename=self.file_path) as img:
            for f in img.sequence:
                dur += f.delay
        return ((int)(dur * 10) / num)

    def toFrames(self):
        if self.getFrames() > 1:
            MediaFile = Image.open(self.file_path)
            images = []
            index = 1
            for frame in ImageSequence.Iterator(MediaFile):
                frame.save(f"tmp/frame{index}.png")
                images.append(Image.open(f"tmp/frame{index}.png").convert('RGBa'))
                index += 1
            return images

    def toGif(self):

        filename = f"{self.info.name}_{self.size}x.gif"
        gif_path = os.path.join(self.output_folder, filename)
        print("Converting to gif...")
        self.startTime = time.time()
        self.toFrames()[0].save(gif_path, format='GIF', append_images=self.toFrames()[1:], save_all=True,
                               duration=self.getDuration(), disposal=2, loop=0, transparency=0)
        self.currTime = time.time()
        print(f"Conversion finished. ({self.currTime - self.startTime} seconds)")

        files = glob.glob("tmp/*.png")
        for files in files:
            try:
                os.remove(files)
            except:
                print("Error while deleting file : ", files)
        os.remove(self.file_path)
        self.file_path = gif_path

    def toImg(self):
        print("Converting to png...")
        self.startTime = time.time()
        im = Image.open(self.file_path)
        filename = f"{self.info.name}_{self.size}x.png"
        img_path = os.path.join(self.output_folder, filename)
        im.save(img_path, "png")
        self.currTime = time.time()
        print(f"Conversion finished. ({self.currTime - self.startTime} seconds)")
        os.remove(self.file_path)
        self.file_path = img_path

    def download(self,output_folder):
        self.output_folder = output_folder
        self.startTime = time.time()
        self.getFile()
        if self.mime == "webp":
            print("is webp")
            if self.getFrames() > 1:
                print("is animated")
                self.toGif()
            else:
                print("is static")
                self.toImg()

class Channel:
    def __init__(self,name):
        self.name = name
        self.url = f"https://api.7tv.app/v2/users/{name}/emotes"
        response = requests.get(self.url)
        self.info = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

    def findEmotes(self,emote):
        list = []
        for i in self.info:
            if i.name == emote:
                list.append(i)
        return(list)

    def getEmotes(self,emote, size, output_folder):
        for i in self.findEmotes(emote):
            e = Emote(i.id, size)
            e.download(output_folder)


# emotes = [Emote("603c89cbbb69c00014bed23e", 4),Emote("603ca67dfaf3a00014dff0aa", 4),Emote("60f913b315758a7f9a984b5f", 4),Emote("612b8c766b114f8fd7f34a34", 4)]
# emotes[2].download(dest_folder)

# me = Channel("waterboiledpizza")
# me.getEmotes("xqcL", 2, dest_folder)
