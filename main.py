import pandas as pd
import datetime
import requests
import webbrowser
import cryptocompare
from GoogleNews import GoogleNews
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define constants
CRYPTOCOMPARE_API_KEY = '54c6cffcecec0e0e40bb541701a6c4cdd81bcdc5734be41b48d11fcac90869ae'
NEWS_SEARCH_KEYWORDS = {
    "DOGE": "Dogecoin",
    "USDT": "tether",
    "BTC": "bitcoin",
    "BCH": 'bitcoin cash',
    "ETH": "ethereum",
    "ADA": "cardano",
    "XMR": "monero",
    "LTC": "litecoin",
    "XLM": "stellar",
    "DOT": "Polkadot",
    "INR": "indian rupees",
    "USD": "us dollar",
    "AUD": "australian dollar",
    "JPY": "japanese yen",
    "RUB": "ruble",
    "EUR": "euro"
}

class WindowDraggable():

    def __init__(self, label):
        self.label = label
        label.bind('<ButtonPress-1>', self.StartMove)
        label.bind('<ButtonRelease-1>', self.StopMove)
        label.bind('<B1-Motion>', self.OnMotion)

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        root.geometry("+%s+%s" % (x, y))

def open_url_in_browser(url):
    webbrowser.open_new(url)

def change_button_bg_on_hover(event):
    close_button['bg'] = 'red'

def reset_button_bg(event):
    close_button['bg'] = '#2e2e2e'

def news_scraper(keyword):
    cursor = GoogleNews('en', 'd')
    cursor.search(keyword)
    cursor.getpage(1)
    cursor.result()
    return list(zip(cursor.get_texts(), cursor.get_links()))

def convert():
    canvas.get_tk_widget().pack_forget()
    out_value.delete(0, 'end')
    out_value.config(state="disabled", disabledbackground="#1e1e1e")

    symbol = inp_curr.get()
    comparison_symbol = out_curr.get()
    value = float(inp_value.get())

    cryptocompare.cryptocompare._set_api_key_parameter(CRYPTOCOMPARE_API_KEY)
    price_data = cryptocompare.get_price([symbol], [comparison_symbol])
    conversion_rate = price_data[symbol][symbol.upper()][comparison_symbol.upper()]

    outText.set("{}".format(conversion_rate * value))

    news_data = news_scraper(NEWS_SEARCH_KEYWORDS.get(symbol))
    for i, news_label in enumerate(news_labels):
        news_label.config(text=news_data[i][0], cursor="hand2")
        news_label.bind("<Button-1>", lambda e, url=news_data[i][1]: open_url_in_browser(url))

    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'.format(
        symbol.upper(), comparison_symbol.upper(), limit, aggregate)

    if exchange:
        url += '&e={}'.format(exchange)

    if all_data:
        url += '&allData=true'

    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]

    fig = Figure(figsize=(5, 5), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(df.timestamp, df.close)

    canvas = FigureCanvasTkAgg(fig, master=graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

root = Tk()
root.overrideredirect(True)
root.geometry('700x500+200+200')

# Title Bar
title_bar = Frame(root, bg='#2e2e2e', relief='raised', bd=2, highlightthickness=0)
WindowDraggable(title_bar)
title_bar.pack(side="top", expand=1, fill=X, anchor=N)

winlabel = Label(title_bar, text='CryptoConvertor', bg="#2e2e2e", font="bold", fg="white", highlightthickness=0)
winlabel.pack(side="left", anchor=W)
close_button = Button(title_bar, text='X', command=root.destroy, bg="#2e2e2e", padx=2, pady=2, activebackground='red',
                     bd=0, font="bold", fg='white', highlightthickness=0)
close_button.pack(side="right")

# Conversion Window
conv = Frame(root, bg="#2e2e2e", relief="ridge", bd=2)
clabel = Label(conv, bg="#2e2e2e", font="bold", fg="white", text="Convert Menu")
conv.place(relx=0, rely=0.08, relwidth=1, relheight=0.45)
clabel.place(relx=0.5, rely=0.15, anchor=CENTER)

# Options
inpOPTIONS = [
    "DOGE", "USDT", "BTC", "BCH", "ETH", "ADA", "XMR", "LTC", "XLM", "DOT",
    "INR", "USD", "AUD", "JPY", "RUB", "EUR"
]

outOPTIONS = [
    "INR", "USD", "AUD", "JPY", "RUB", "EUR", "DOGE", "USDT", "BTC", "BCH",
    "ETH", "ADA", "XMR", "LTC", "XLM", "DOT"
]

# Input
inp_value = Entry(conv, bd=2, bg="#1e1e1e", fg="white", highlightthickness=0)
inp_value.place(relx=0.1, rely=0.3, relwidth=0.35)

inp_curr = StringVar(conv)
inp_curr.set(inpOPTIONS[0])
inp = OptionMenu(conv, inp_curr, *inpOPTIONS)
inp.config(bg="#1e1e1e", fg="white", highlightthickness=0)
inp.place(relx=0.1, rely=0.45, relwidth=0.35, relheight=0.15)

# Output
outText = StringVar()
out_value = Entry(conv, bd=2, bg="#1e1e1e", fg="white", highlightthickness=0,
                   state="disabled", disabledbackground="#1e1e1e", textvariable=outText)
outText.set("0")
out_value.place(relx=0.55, rely=0.3, relwidth=0.35)

out_curr = StringVar(conv)
out_curr.set(outOPTIONS[0])
out = OptionMenu(conv, out_curr, *outOPTIONS)
out.config(bg="#1e1e1e", fg="white", highlightthickness=0)
out.place(relx=0.55, rely=0.45, relwidth=0.35, relheight=0.15)

convBUTT = Button(conv, text="CONVERT", command=convert, bg="#1e1e1e", fg="white")
convBUTT.place(relx=0.5, rely=0.8, anchor=CENTER, relwidth=0.8, relheight=0.2)

# Graph
width = 0.6
height = 0.45
graph = LabelFrame(root, bg="#2e2e2e", relief="ridge", bd=2)
glabel = Label(graph, bg="#2e2e2e", fg="white", text="graph")
graph.place(relx=0, rely=0, relwidth=width, relheight=height)
glabel.place(relx=0, rely=0)

fig = Figure(figsize=(5, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, graph)
canvas.get_tk_widget().pack(fill=BOTH, expand=True)

# News
newsText = StringVar()

news = Frame(root, bg="#2e2e2e", relief="ridge", bd=2)
clabel = Label(news, bg="#2e2e2e", font="bold", fg="white", text="Trending articles")
news.place(relx=0, rely=height, relwidth=1, relheight=0.55)
clabel.place(relx=0, rely=0)

news_labels = []
ydist = 0.11
back = "#1e1e1e"
num = 1
numE = 0

for i in range(10):
    lbl = Frame(news, bg=back)
    lbl.place(relx=0, rely=ydist, relwidth=1, relheight=0.07)
    n = Label(lbl, text=num, bg=back, fg="white")
    n.place(relx=0, rely=0)
    news_label = Label(lbl, text="", bg=back, fg="#00FFFF", cursor="hand2")
    news_label.place(relx=0.06, rely=0)
    news_labels.append(news_label)
    ydist += 0.07
    back = "#2e2e2e"
    num += 1
    numE += 1

# Run the application
root.mainloop()
