"""
Module for the client side of the recomender system application of source prioritization.

Function:
showres
showres_event
main
"""

from Tkinter import *
import client
import globalsfile as gl

def showres():
   """
      Based on url and time outputs the results.
   """
   #var = StringVar()
   #label = Message(dframe, textvariable=var, relief = RAISED, width = 40)
   #label.config(font=('times',10))
   
   url = E1.get()
   time = E2.get()

   if url:
      if time: msg = client.main(url, time = int(time))
      else : msg = client.main(url)

      if not msg == None:
         limit = min(20,len(msg))
         for i in range(limit):
            text.insert(INSERT, msg[i][0]+"\n")

   #var.set(str(msg[:10]))
   #label.pack(side = BOTTOM, expand = True)

def showres_event(event):
   """
      Event Handler for the button event.
   """
   showres()

def main():
   """
      Main function : Creates interface for the application.
   """
   global ufrane, dframe, E1, E2, text
   root = Tk()
   uframe = Frame(root)
   uframe.pack()
   ruframe = Frame(uframe)
   ruframe.pack(side = RIGHT)
   luframe = Frame(uframe)
   luframe.pack(side = LEFT)
   dframe = Frame(root, width = 50)
   dframe.pack(side = BOTTOM)
   root.title("RecoSys - BTP 2013-2014")
   root.resizable(0,0)
   
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
   """
      Main of the module.
   """

   gl.init()
   main()
