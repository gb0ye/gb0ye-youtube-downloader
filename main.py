from yt_dlp import YoutubeDL
import telebot
from telebot import types
from telebot.util import quick_markup
import logging
import json

logging.basicConfig(filename="yt_logger.log")

bot = telebot.TeleBot("")

url = "https://youtu.be/2k5w6eTxGXk?si=oszEUCqYYyUz-Aj7"


def get_available_formats(url):
    ydl_opts = {
        "listformats": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = info.get("formats", [])
        botButtons = []
        for format in formats:
            ext = format["ext"]
            format_note = format.get('format_note', '')
            filesize = format.get("filesize")
            botButtons.append(f"{ext, format_note,}, {format_bytes(filesize)}")
        return botButtons


# showButtons(testBtns)

def format_bytes(size):
    # 2**10 = 1024
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'kilo', 2: 'mega', 3: 'giga', 4: 'tera'}
    while size > power:
        size /= power
        n += 1
    return size, power_labels[n]+'bytes'  


# get_available_formats(url)
def showButtons(arrBtns):
    finalBtns = {}
    for btn in arrBtns:
        finalBtns[btn] = {"callback_data": btn}
    print(finalBtns)
    markup = quick_markup(finalBtns, row_width=2)
    return markup


# @bot.message_handler(commands=["btns"])
# def Show_Dem_Btns(message):
#     markup = showButtons(testBtns)
#     print(markup)
#     bot.reply_to(message, text="here are your btns,", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def Show_Dem_Btns(message):
    bot.reply_to(message, "loading...")
    availableFormats = get_available_formats(message.text)
    markup = showButtons(availableFormats)
    bot.reply_to(message, text="here are your btns,", reply_markup=markup)


bot.infinity_polling()


# def format_selector(ctx):
#     json_data = json.dumps(ctx)
#     # print(json_data)
#     formats = ctx.get("formats")[::-1]

#     # acodec='none' means there is no audio
#     best_video = next(f for f in formats
#                       if f['vcodec'] != 'none' and f['acodec'] == 'none')
#     print(best_video)

#     # find compatible audio extension
#     audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
#     print(audio_ext)

#     # vcodec='none' means there is no video
#     best_audio = next(f for f in formats if (
#         f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))
#     print(best_audio)

#     # These are the minimum required fields for a merged format
#     result =  {
#         'format_id': f'{best_audio["format_id"]}',
#         'ext': best_audio['ext'],
#         'requested_formats': [best_audio],
#         # Must be + separated list of protocols
#         'protocol': f'{best_audio["protocol"]}'
#     }

#     yield(result)

# ydl_opts={
#     "format": format_selector,
#     "outtmpl":"/dowloads/%(title)s.%(ext)s"
# }

# with YoutubeDL(ydl_opts) as ydl:
# ydl.download(URLS)
