from Tkinter import *
import client
from math import exp

def kw_th(t):
   return 30/(1+exp(-(t-15)/3))

def showres():
   #var = StringVar()
   #label = Message(dframe, textvariable=var, relief = RAISED, width = 40)
   #label.config(font=('times',10))
   url = E1.get()
   if url:
      msg = client.main(url, 'test')
      for i in range(10):
         text.insert(INSERT, str(msg[i])+"\n")
   #var.set(str(msg[:10]))
   #label.pack(side = BOTTOM, expand = True)

def showres_event(event):
   showres()

def main():
   root = Tk()
   global ufrane, dframe, E1, text
   uframe = Frame(root)
   uframe.pack()
   ruframe = Frame(uframe)
   ruframe.pack(side = RIGHT)
   luframe = Frame(uframe)
   luframe.pack(side = LEFT)
   dframe = Frame(root, width = 50)
   dframe.pack(side = BOTTOM)
   root.title("RecoSys")
   #root.resizable(0,0)
   
   L1 = Label(luframe, text = "URL : ")
   L1.pack(side = LEFT)
   E1 = Entry(luframe, bd = 5, width = 60)
   E1.pack(side = RIGHT)
   L2 = Label(ruframe, text = "Time : ")
   L2.pack(side = LEFT)
   E2 = Entry(ruframe, bd = 5, width = 10)
   E2.pack(side = RIGHT)
   text = Text(dframe)
   text.pack(side = BOTTOM)
   
   B = Button(dframe, text = "Enter", command = showres)
   B.pack(expand = True)
   root.bind("<Return>", showres_event)
   root.mainloop()

if __name__ == "__main__":
   main()
