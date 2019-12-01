"""
A file to hold the GUI logic and instantiation of the host server.
"""
import tkinter as tk
import tkinter.font
import requests
from PIL import Image
from PIL import ImageTk

HEIGHT = 500
WIDTH = 600


def formatResponse(weather):
    print(weather)
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
        finalStr = 'City: %s \nConditions: %s \nTempurature (F): %s' % (name, desc, temp)
    except:
        finalStr = 'There was a problem D:\nPlease make sure that\n you have provided a City!'
    return finalStr


def getWeather(city):
    weatherKey = 'd086d319958263c0e741472bc37d784f'
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': weatherKey, 'q': city, 'units': 'imperial'}
    response = requests.get(url, params)
    print('url: %s%s' % (url, params))
    weather = response.json()
    # change label to be correct info or error message
    label['text'] = formatResponse(weather)


root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

photoImg = Image.open('AnimeBackgroundWhiteHair.jpg')
photoImg = photoImg.resize((WIDTH, HEIGHT), Image.ANTIALIAS)

background_image = ImageTk.PhotoImage(photoImg)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Get Weather", font=('Courier', 12), command=lambda: getWeather(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame, font=('Courier', 18))
label.place(relwidth=1, relheight=1)

root.mainloop()
