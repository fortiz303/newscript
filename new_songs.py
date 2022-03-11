import os
from pytube import YouTube
import telepot
from time import sleep
import ffmpeg
import re
import urllib.request
import pytube

search = "https://www.youtube.com/results?search_query=type+beat&sp=CAISBAgBEAE%253D"

print("DONE")

chat_id = "-749654410"
TOKEN = "2024558047:AAGDmrU2wfhoUFDwqHhve-BjiMj8NrmIcBA"
links = []

def results():
    html = urllib.request.urlopen(search)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    for i in video_ids:
        links.append(i)

print("DONE!!!")

def youtubemp3_dl(link, name):
    yt = YouTube(link)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(filename=name, output_path=".")

def cut_audio(filename, out):
    audio_input = ffmpeg.input(filename)
    audio_cut = audio_input.audio.filter('atrim', duration=15)
    audio_output = ffmpeg.output(audio_cut, out)
    ffmpeg.run(audio_output)


def send_telegram_msg(filename, msg):
    bot = telepot.Bot(TOKEN)
    bot.sendMessage(chat_id, msg)
    file = filename
    bot.sendDocument(chat_id=chat_id, document=open(file, 'rb'))

print("1DONE")

while True:
    "Search started:"
    html = urllib.request.urlopen(search)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    for i in video_ids:
        if i not in links:
            url = "https://www.youtube.com/watch?v=" + i
            title = YouTube(url).title
            print(title)

            infile = title + ".mp4"
            outfile = title + "out.mp4"

            youtubemp3_dl(url, infile)
            print("Download done.")
#inserted sleep
            sleep(1)
            cut_audio(infile, outfile)
            print("Cut.")
            send_telegram_msg(outfile, title)
            print("Sent to telegram.")
            os.remove(infile)
            os.remove(outfile)
            print("Files deleted.")
            links.append(i)
    print("Waiting 15mn.")
    sleep(900)
