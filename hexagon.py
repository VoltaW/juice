"""
hexagon.py (pending name change)

VoltaWorks
2023

Developed on PyCharm using Python 3.9

Display screen for eInk screen to be used on battery pack.
- Shows the current battery charge level number and hexagon sides based on charge level.
- Shows whether the battery pack is being charged (plugged in)
"""

import tkinter as tk
import math

#the size of the display screen
WIDTH, HEIGHT = 212, 104

class Point:
    """convenience for point arithmetic"""
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def __iter__(self):
        yield self.x
        yield self.y

class RegularPolygon:

    def __init__(self, num_sides, bbox_side, x, y):  # x, y are bbox center canvas coordinates
        self.bbox_side = bbox_side
        self.num_sides = num_sides
        self.side_length = None
        self.apothem = None
        self._calc_side_length()
        self.points = [Point(x - self.side_length // 2, y - self.apothem)]
        self._make_points()
        self.lines = []
        self._make_lines()

    def _calc_side_length(self):
        """Side length given the radius (circumradius):
        i/e the distance from the center to a vertex
        """
        hex = 6
        self.side_length = 2 * (self.bbox_side // 2) * math.sin(math.pi / hex)

        # Apothem, i/e distance from the center of the polygon
        # to the midpoint of any side, given the side length
        self.apothem = self.side_length / (2 * math.tan(math.pi / hex))

    def _make_points(self):
        hex = 6
        _angle = 2 * math.pi / hex
        #display_sides = (self.chrg_p / 100) * hex
        disp_sides = math.floor((self.num_sides / 100) * hex)
        for pdx in range(hex):
            angle = _angle * pdx
            _x = math.cos(angle) * self.side_length
            _y = math.sin(angle) * self.side_length
            if (pdx < disp_sides):     #self.num_sides):
                self.points.append(self.points[-1] + Point(_x, _y))

    def _make_lines(self):
        for p0, p1 in zip(self.points[:-1], self.points[1:]):
                    self.lines.append((*p0, *p1))

    def draw(self, canvas):
        for line in self.lines:
            canvas.create_line(line)
        # alternatively, use canvas.create_polygon(points coordinates) instead

"""
get the charge level via user input for now. To be changed to get the values from the battery pack
directly when it is implemented in hardware
"""
chrg_p_string = input("What is the charge percentage: ")
chrg_p = int(chrg_p_string)
chrging = input("Is it charging (y/n)?: ")

#print(chrg_p)

root = tk.Tk()

#canvas based on the size and colours of the eInk display
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

CENTER = Point(WIDTH // 2, HEIGHT // 2)

while True:
    #draw the hexagon with number of sides based on current charge level
    n_sides = chrg_p  #6
    p = RegularPolygon(n_sides, 90, *CENTER)
    p.draw(canvas)
    #print the charge % level and in red if it is currently charging
    if (chrging == "y"):
        canvas.create_text(*CENTER, fill="red", font="times 30", text = chrg_p_string)
    else:
        canvas.create_text(*CENTER, font="times 30", text = chrg_p_string)
    
    root.mainloop()
