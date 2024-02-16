from tkinter import *
from math import sin, cos



def drawRect(c, x1, y1, x2, y2, feather, res=5, color='black'):
    """
    Function to make a rectangle with rounded corners, 
    args :
    c : tkinter canvas
    x1, y1 : top left corner
    x2, y2 : bottom right corner
    feather : corner radius
    res : number of points for the circle approximation (default 5)
    color : fill color (default black)
    """
    points = []
    # top side
    points += [x1 + feather, y1,
               x2 - feather, y1]
    # top right corner
    for i in range(res):
        points += [x2 - feather + sin(i/res*2) * feather,
                   y1 + feather - cos(i/res*2) * feather]
    # right side
    points += [x2, y1 + feather,
               x2, y2 - feather]
    # bottom right corner
    for i in range(res):
        points += [x2 - feather + cos(i/res*2) * feather,
                   y2 - feather + sin(i/res*2) * feather]
    # bottom side
    points += [x2 - feather, y2,
               x1 + feather, y2]
    # bottom left corner
    for i in range(res):
        points += [x1 + feather - sin(i/res*2) * feather,
                   y2 - feather + cos(i/res*2) * feather]
    # left side
    points += [x1, y2 - feather,
               x1, y1 + feather]
    # top left corner
    for i in range(res):
        points += [x1 + feather - cos(i/res*2) * feather,
                   y1 + feather - sin(i/res*2) * feather]
        
    return c.create_polygon(points, fill=color) #?



if __name__ == "__main__":
    master = Tk()

    c = Canvas(master, width=230, height=230)
    c.pack()

    create_good_rectangle(c, 10, 10, 200, 100, 20)
    create_good_rectangle(c, 100, 40, 220, 200, 40, 8, 'blue')

    mainloop()