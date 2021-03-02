from tkinter import *
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import requests
import webbrowser
import cryptocompare
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) 
from GoogleNews import GoogleNews

def callback(url):
    webbrowser.open_new(url)

def news_scraper(curr):
    cursor = GoogleNews('en','d')
    cursor.search(curr)
    cursor.getpage(1)
    cursor.result()
    return list(zip(cursor.get_texts(),cursor.get_links()))


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

    def OnMotion(self,event):
        x = (event.x_root - self.x - self.label.winfo_rootx() + self.label.winfo_rootx())
        y = (event.y_root - self.y - self.label.winfo_rooty() + self.label.winfo_rooty())
        root.geometry("+%s+%s" % (x, y))


def change_on_hovering(event):
    global close_button
    close_button['bg']='red'
def return_to_normalstate(event):
    global close_button
    close_button['bg']='#2e2e2e'

def convert(all_data=True, limit=1, aggregate=1, exchange=''):
    global canvas
    global e1,e2,e3,e4,e5,e6,e7,e8,e9,e10

    canvas.get_tk_widget().pack_forget()
    out_value.delete(0,'end')
    out_value.config(state="disabled",disabledbackground="#1e1e1e")

    symbol = inp_curr.get()
    comparison_symbol = out_curr.get()
    value = float(inp_value.get())

    a =  cryptocompare.cryptocompare._set_api_key_parameter('54c6cffcecec0e0e40bb541701a6c4cdd81bcdc5734be41b48d11fcac90869ae')
    dict1 = {symbol:cryptocompare.get_price([symbol],[comparison_symbol])}
    ans = dict1[symbol][symbol.upper()][comparison_symbol.upper()]

    outText.set("{}".format(ans*value))

    #NEW EXTRACTION
    search_dict = {
    "DOGE":"Dogecoin",
    "USDT":"tether",
    "BTC":"bitcoin",
    "BCH":'bitcoin cash',
    "ETH":"ethereum",
    "ADA":"cardano",
    "XMR":"monero",
    "LTC":"litecoin",
    "XLM":"stellar",
    "DOT":"Polkadot",
    "INR":"indian rupees",
    "USD":"us dollar",
    "AUD":"australian dollar",
    "JPY":"japanese yen",
    "RUB":"ruble`",
    "EUR":"euro"}
    cr = news_scraper(search_dict.get(symbol))
    n=0
    e1.config(text=cr[n][0])
    e1.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e2.config(text=cr[n][0])
    e2.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e3.config(text=cr[n][0])
    e3.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e4.config(text=cr[n][0])
    e4.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e5.config(text=cr[n][0])
    e5.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e6.config(text=cr[n][0])
    e6.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e7.config(text=cr[n][0])
    e7.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e8.config(text=cr[n][0])
    e8.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e9.config(text=cr[n][0])
    e9.bind("<Button-1>", lambda e: callback(cr[n][1]))
    n+=1
    e10.config(text=cr[n][0])
    e10.bind("<Button-1>", lambda e: callback(cr[n][1]))

    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    if all_data:
        url += '&allData=true'
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]

    # the figure that will contain the plot
    fig = Figure(figsize = (5, 5), dpi = 100)
    a = fig.add_subplot(111)
    df.head()
    a.plot(df.timestamp,df.close)

    canvas = FigureCanvasTkAgg(fig, master = graph)   
    canvas.draw() 
    canvas.get_tk_widget().pack(fill=BOTH, expand=True) 


root=Tk()
root.overrideredirect(True)
root.geometry('700x500+200+200')

#---------------####TITLE BAR####-----------------#
title_bar = Frame(root, bg='#2e2e2e', relief='raised', bd=2,highlightthickness=0)
WindowDraggable(title_bar)
title_bar.pack(side="top", expand=1, fill=X, anchor=N)

winlabel = Label(title_bar, text=' CryptoConvertor',bg="#2e2e2e", font="bold", fg="white", highlightthickness=0)
winlabel.pack(side="left",anchor=W)
close_button = Button(title_bar, text='X', command=root.destroy,bg="#2e2e2e",padx=2,pady=2,activebackground='red',bd=0,font="bold",fg='white',highlightthickness=0)
close_button.pack(side="right")

window = Frame(root, bg='red',highlightthickness=0)
window.place(relx=0,rely=0.08, relwidth=1, relheight=1)

close_button.bind('<Enter>',change_on_hovering)
close_button.bind('<Leave>',return_to_normalstate)

#--------------------------------####WINDOW####--------------------------------#

####GRAPH####
width=0.6
height=0.45
graph = LabelFrame(window, bg="#2e2e2e", relief="ridge", bd=2)
glabel = Label(graph, bg="#2e2e2e", fg="white", text="graph")
graph.place(relx=0,rely=0, relwidth=width, relheight=height)
glabel.place(relx=0,rely=0)

fig = Figure(figsize = (5, 5), dpi = 100)
canvas = FigureCanvasTkAgg(fig, graph)
canvas.get_tk_widget().pack(fill=BOTH, expand=True)



####CONVERSION####
conv = Frame(window, bg="#2e2e2e", relief="ridge", bd=2)
clabel = Label(conv, bg="#2e2e2e",font="bold", fg="white", text="Convert Menu")
conv.place(relx=width,rely=0, relwidth=0.4, relheight=height)
clabel.place(relx=0.5,rely=0.15,anchor=CENTER)

#OPTIONS VALUE TO BE CHANGED ASAP
inpOPTIONS = [
"DOGE",
"USDT",
"BTC",
"BCH",
"ETH",
"ADA",
"XMR",
"LTC",
"XLM",
"DOT",
"INR",
"USD",
"AUD",
"JPY",
"RUB",
"EUR"]
outOPTIONS = [
"INR",
"USD",
"AUD",
"JPY",
"RUB",
"EUR",
"DOGE",
"USDT",
"BTC",
"BCH",
"ETH",
"ADA",
"XMR",
"LTC",
"XLM",
"DOT"
]

#INPUT
inp_value = Entry(conv, bd=2,bg="#1e1e1e", fg="white",highlightthickness=0)
inp_value.place(relx=0.1, rely=0.3, relwidth=0.35)

inp_curr = StringVar(conv)
inp_curr.set(inpOPTIONS[0])
inp = OptionMenu(conv, inp_curr, *inpOPTIONS)
inp.config(bg="#1e1e1e", fg="white",highlightthickness=0)
inp.place(relx=0.1,rely=0.45, relwidth=0.35, relheight=0.15)

#OUTPUT
outText = StringVar()
out_value = Entry(conv, bd=2,bg="#1e1e1e", fg="white",highlightthickness=0,state="disabled",disabledbackground="#1e1e1e", textvariable=outText )
outText.set("0")
out_value.place(relx=0.55, rely=0.3, relwidth=0.35)

out_curr = StringVar(conv)
out_curr.set(outOPTIONS[0])
out = OptionMenu(conv, out_curr, *outOPTIONS)
out.config(bg="#1e1e1e", fg="white",highlightthickness=0)
out.place(relx=0.55,rely=0.45, relwidth=0.35, relheight=0.15)

convBUTT = Button(conv, text="CONVERT", command=convert, bg="#1e1e1e", fg="white")
convBUTT.place(relx=0.5, rely=0.8, anchor=CENTER, relwidth=0.8, relheight=0.2)

####NEWS####

newsText = StringVar()

news = Frame(window, bg="#2e2e2e", relief="ridge", bd=2)
clabel = Label(news, bg="#2e2e2e",font="bold", fg="white", text="Trending articles")
news.place(relx=0,rely=height, relwidth=1, relheight=0.55)
clabel.place(relx=0,rely=0)

l = news_scraper('cryptocurrency')

back="#1e1e1e"
ydist = 0.11
num=1
numE=0

#1
lbl1 = Frame(news,bg=back)
lbl1.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n1 = Label(lbl1,text=num,bg=back,fg="white")
n1.place(relx=0,rely=0)
e1 = Label(lbl1,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e1.place(relx=0.06,rely=0)
e1.bind("<Button-1>", lambda e: callback(str(l[numE][1])))

#2
num+=1
numE+=1
ydist += 0.07
back="#2e2e2e"
lbl2 = Frame(news,bg=back)
lbl2.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n2 = Label(lbl2,text=num,bg=back,fg="white")
n2.place(relx=0,rely=0)
e2 = Label(lbl2,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e2.place(relx=0.06,rely=0)
e2.bind("<Button-1>", lambda e: callback(l[numE][1]))

#3
num+=1
numE+=1
ydist += 0.07
back="#1e1e1e"
lbl3 = Frame(news,bg=back)
lbl3.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n3 = Label(lbl3,text=num,bg=back,fg="white")
n3.place(relx=0,rely=0)
e3 = Label(lbl3,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e3.place(relx=0.06,rely=0)
e3.bind("<Button-1>", lambda e: callback(str(l[numE][1])))

num+=1
numE+=1
ydist += 0.07
back="#2e2e2e"
lbl4 = Frame(news,bg=back)
lbl4.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n4 = Label(lbl4,text=num,bg=back,fg="white")
n4.place(relx=0,rely=0)
e4 = Label(lbl4,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e4.place(relx=0.06,rely=0)
e4.bind("<Button-1>", lambda e: callback(l[numE][1]))



num+=1
numE+=1
ydist += 0.07
back="#1e1e1e"
lbl5 = Frame(news,bg=back)
lbl5.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n5 = Label(lbl5,text=num,bg=back,fg="white")
n5.place(relx=0,rely=0)
e5 = Label(lbl5,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e5.place(relx=0.06,rely=0)
e5.bind("<Button-1>", lambda e: callback(str(l[numE][1])))

num+=1
numE+=1
ydist += 0.07
back="#2e2e2e"
lbl6 = Frame(news,bg=back)
lbl6.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n6 = Label(lbl6,text=num,bg=back,fg="white")
n6.place(relx=0,rely=0)
e6 = Label(lbl6,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e6.place(relx=0.06,rely=0)
e6.bind("<Button-1>", lambda e: callback(l[numE][1]))


num+=1
numE+=1
ydist += 0.07
back="#1e1e1e"
lbl7 = Frame(news,bg=back)
lbl7.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n7 = Label(lbl7,text=num,bg=back,fg="white")
n7.place(relx=0,rely=0)
e7 = Label(lbl7,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e7.place(relx=0.06,rely=0)
e7.bind("<Button-1>", lambda e: callback(str(l[numE][1])))

num+=1
numE+=1
ydist += 0.07
back="#2e2e2e"
lbl8 = Frame(news,bg=back)
lbl8.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n8 = Label(lbl8,text=num,bg=back,fg="white")
n8.place(relx=0,rely=0)
e8 = Label(lbl8,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e8.place(relx=0.06,rely=0)
e8.bind("<Button-1>", lambda e: callback(l[numE][1]))



num+=1
numE+=1
ydist += 0.07
back="#1e1e1e"
lbl9 = Frame(news,bg=back)
lbl9.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n9 = Label(lbl9,text=num,bg=back,fg="white")
n9.place(relx=0,rely=0)
e9 = Label(lbl9,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e9.place(relx=0.06,rely=0)
e9.bind("<Button-1>", lambda e: callback(str(l[numE][1])))

num+=1
numE+=1
ydist += 0.07
back="#2e2e2e"
lbl10 = Frame(news,bg=back)
lbl10.place(relx=0,rely=ydist,relwidth=1,relheight=0.07)
n10 = Label(lbl10,text=num,bg=back,fg="white")
n10.place(relx=0,rely=0)
e10 = Label(lbl10,text=l[numE][0],bg=back,fg="#00FFFF",cursor="hand2")
e10.place(relx=0.06,rely=0)
e10.bind("<Button-1>", lambda e: callback(l[numE][1]))









root.mainloop()
