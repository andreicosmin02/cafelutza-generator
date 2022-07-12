import requests
import json
from PIL import Image, ImageDraw, ImageFont
import io
import random
import os
from argparse import ArgumentParser


def getQuotes(number):
    f = open('quote.txt', 'w')
    quote = ''
    for i in range(number):
        quotesWebsite = 'https://api.adviceslip.com/advice'
        resp = requests.get(quotesWebsite)
        quote += json.loads(resp.text)['slip']['advice']
        quote += '\n'

    print(quote)

    f.write(quote)


def getCoffeeImage():
    coffeeWebsite = 'https://coffee.alexflipnote.dev/random'
    imageRequest = requests.get(coffeeWebsite)
    image = Image.open(io.BytesIO(imageRequest.content))
    return image


''' If no width is given, defaults to 1080 '''
def resizeImage(image, newWidth=1080):
    width, height = image.size
    newHeight = int(height / width * newWidth)

    return image.resize((newWidth, newHeight))


def getQuote():
    with open('citate.txt', 'r+', encoding='utf-8') as f:
        lines = f.readlines()
    line = lines[random.randint(0, len(lines))]
    line = line.replace('\n', '')
    line = line.split(' ')
    quote = ''
    w = 0
    for word in line:
        if w < 1060:
            quote += word + ' '
        else:
            w = 0
            quote += '\n' + word + ' '
        w += len(word) * 100
    return quote


def createImage(image, text, path):
    quoteImage = ImageDraw.Draw(image, 'RGBA')
    width, height = image.size
    shape = [(0, 0), (width, height)]
    quoteImage.rectangle(shape, fill=(0, 0, 0, 125))

    # Font needs to support ALL Romanian characters
    myFont = ImageFont.truetype(os.path.join(os.getcwd(), "fonts", 'StingerFitTrial-Regular.ttf'), 80)

    quoteImage.text((20, 20), text, font=myFont)
    image.save(path)


def getFormattedQuotes(quote_type, line_width=1060, max_quotes=0):

    quote_types = {
        'cudetoate': 'cudetoate.txt',
        'optimiste': 'optimiste.txt',
        'pesimiste': 'pesimiste.txt',
    }
    quotes = []

    with open(os.path.join(os.getcwd(), "data_sources", quote_types[quote_type]), 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    for index, line in enumerate(lines):

        line = line.replace('\n', '').split(' ')
        newquote = ''
        w = 0
        for word in line:
            if w < line_width:
                newquote += word + ' '
            else:
                w = 0
                newquote += '\n' + word + ' '
            w += len(word) * 90

        quotes.append(newquote)
        if 0 < max_quotes < index:
            break

    return quotes


def handle_output_dir(folder, tip):

    cwd = os.getcwd()
    if folder == '':
        # Get the dir name from image type
        folder = tip
    fullpath = os.path.join(cwd, folder)
    if not os.path.isdir(fullpath):
        try:
            os.mkdir(fullpath)
            if not os.path.isdir(fullpath):
                print("Failed to create dir, and yet didn't catch an exception")
        except Exception as e:
            print("Am prins o exceptie: ", e)


if __name__ == "__main__":

    arg = ArgumentParser()
    arg.add_argument('-n', '--nimg', default=1, type=int, nargs=1, required=False, help='Numar de IMaGini de generat')
    arg.add_argument('-d', '--dir', default='', type=str, nargs=1,
                     required=False,
                     help="Directorul unde se vor plasa imaginile. Implicit va fi numit dupa optiunea de imagini.")
    arg.add_argument('-t', '--tip', default='cudetoate', nargs=1,
                     required=False, choices=['optimiste', 'pesimiste', 'cudetoate'],
                     help="Tipul de mesaje de generat. Implicit vor fi amestecate, adica cudetoate")
    arguments = arg.parse_args()

    handle_output_dir(dir=arguments.dir, tip=arguments.tip)

    quote_set = getFormattedQuotes(arguments.tip, max_quotes=10)
    for index, quote in enumerate(quote_set):
        try:
            coffeeImage = resizeImage(getCoffeeImage())
            createImage(coffeeImage, quote,  f'rezultaturat/rezultat{index}.png')
        except Exception as e:
            print("Ceva a mers gresit. Exceptie: ", e)

    #
    # for i in range(25):
    #     try:
    #         coffeeImage = getCoffeeImage()
    #         coffeeImage = resizeImage(coffeeImage)
    #         quote = getQuote()
    #         createImage(coffeeImage, quote, f'rezultat/rezultat{i}.png')
    #     except:
    #         print(f'exceptie la generare poza {i}')

''' Todo: 

Add quotes to bank
Place quotes in a json to allow other potentially useful metadata to be added later
    subtask: maybe all quotes could be in one json, and add a relevant attribute for what kind they are (encouraging etc)
...
'''