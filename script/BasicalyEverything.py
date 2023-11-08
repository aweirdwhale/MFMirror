#Import modules
import tkinter as tk
from PIL import ImageTk, Image

 


#make a window
window = tk.Tk()
window.title("Hand Recognition IA")

#make the window fullscreen
window.geometry("1920x1080")
window.attributes('-fullscreen', False)

#black background
window.configure(bg='black')

frame = tk.Frame(window, width=1920, height=1080, bg="black", borderwidth=0, highlightthickness=0)
frame.pack()
frame.place(anchor='center', relx=.5, rely=.5)

#load the image
img = Image.open("../visuel/MFM/mfmPhase1.png")
img = img.resize((1280,720))
img = ImageTk.PhotoImage(img)

#put the image in a label to display it in the window
label = tk.Label(frame, image=img)
label.pack()




#show the window
window.mainloop()

