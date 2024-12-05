"""
hexagon.py (pending name change)

VoltaWorks
2023

Developed on PyCharm using Python 3.9

Display screen for eInk screen to be used on battery pack.
- Shows the current battery charge level number and hexagon sides based on charge level.
- Shows whether the battery pack is being charged (plugged in)
- It has a Settings menu
- Input values are from a text input file
"""

import tkinter as tk
import math

#the size of the display screen
WIDTH, HEIGHT = 212, 104

font_ = "arial"

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
        ie: the distance from the center to a vertex
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
            canvas.create_line(line, width=5)
        # alternatively, use canvas.create_polygon(points coordinates) instead

"""
get the charge level via user input for now. To be changed to get the values from the battery pack
directly when it is implemented in hardware
"""

root = tk.Tk()

#canvas based on the size and colours of the eInk display
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

#set the point locations on the display for each element
CENTER = Point(WIDTH // 2, HEIGHT // 2)
INPUTROW = Point(15, HEIGHT-4)
INPUTROW2 = Point(35, HEIGHT-4)
INPUTROW3 = Point(60, HEIGHT-4)
INPUTROW4 = Point(95, HEIGHT-4)
INPUTROWSETTINGS = Point(WIDTH-25, HEIGHT-4)

INPUTPOINT = Point(35, 15)
INPUTVALUE = Point(35, 25)
TIMETOFULL = Point(35, 35)
TIMETOFULLMINS = Point(35, 45)

OUTPUTPOINT = Point(WIDTH-35, 15)
OUTPUTVALUE = Point(WIDTH-35, 25)
TIMETOEMPTY = Point(WIDTH-35, 35)
TIMETOEMPTYMINS = Point(WIDTH-35, 45)

DCPOINT = Point(WIDTH-35, 65)
DCPOINTENTER = Point(WIDTH-35, 75)

HEATWARNING = Point(35, 70)

"""
Run the program constantly getting updating values from the text file and update the display
"""
def update():
    canvas.delete("all")
    split_space = ' '

    #read in and store the input values
    with open('input-file.txt') as f:
        read_line = f.readline()
        chrg_p_string = read_line.partition(split_space)[0]
        chrg_p = int(chrg_p_string)

        read_line = f.readline()
        chrging = read_line.partition(split_space)[0]

        read_line = f.readline()
        ac_connected = read_line.partition(split_space)[0]

        read_line = f.readline()
        dc_connected = read_line.partition(split_space)[0]

        read_line = f.readline()
        usba_connected = read_line.partition(split_space)[0]

        read_line = f.readline()
        usbc_connected = read_line.partition(split_space)[0]

        read_line = f.readline()
        input_value = read_line.partition(split_space)[0]

        read_line = f.readline()
        time_to_full_mins = read_line.partition(split_space)[0]

        read_line = f.readline()
        output_value = read_line.partition(split_space)[0]

        read_line = f.readline()
        time_to_empty_mins = read_line.partition(split_space)[0]

        read_line = f.readline()
        dc_input_value = read_line.partition(split_space)[0]

        read_line = f.readline()
        heat_warning = read_line.partition(split_space)[0]

        read_line = f.readline()
        settings_active = read_line.partition(split_space)[0]

        read_line = f.readline()
        setting_selected = read_line.partition(split_space)[0]

        read_line = f.readline()
        car_charger_active = read_line.partition(split_space)[0]

        read_line = f.readline()
        car_charger_status = read_line.partition(split_space)[0]

        read_line = f.readline()
        updating_software_active = read_line.partition(split_space)[0]

        read_line = f.readline()
        update_progress = read_line.partition(split_space)[0]
        #update_progress_percent = int(update_progress)


    # draw the hexagon with number of sides based on current charge level
    n_sides = chrg_p  # 6
    p = RegularPolygon(n_sides, 70, *CENTER)
    p.draw(canvas)

    #print the charge % level of the battery and in red if it is currently charging
    if (chrging == "y"):
        canvas.create_text(*CENTER, fill="red", font=font_+" 20", text = chrg_p_string)
    else:
        canvas.create_text(*CENTER, font=font_+" 20", text = chrg_p_string)

    #the car charger function will have a different screen
    if (car_charger_active == "y"):
        canvas.create_text(*INPUTROW3, fill="red", font=font_+"  8", text="CAR CHARGER ACTIVE")
    #set the active and inactive port connections
    else:
        if (ac_connected == "y"):
            canvas.create_text(*INPUTROW, fill="red", font=font_+"  8", text = "AC")
        else:
            canvas.create_text(*INPUTROW, font=font_+" 8", text = "AC")

        if (dc_connected == "y"):
            canvas.create_text(*INPUTROW2, fill="red", font=font_ + "  8", text="DC")
        else:
            canvas.create_text(*INPUTROW2, font=font_ + " 8", text="DC")

        if (usba_connected == "y"):
            canvas.create_text(*INPUTROW3, fill="red", font=font_+" 8", text="USB-A")
        else:
            canvas.create_text(*INPUTROW3, font=font_+" 8", text="USB-A")

        if (usbc_connected == "y"):
            canvas.create_text(*INPUTROW4, fill="red", font=font_+" 8", text = "USB-C")
        else:
            canvas.create_text(*INPUTROW4, font=font_+" 8", text = "USB-C")

    canvas.create_text(*INPUTROWSETTINGS, font=font_+" 8", text = "Settings")

    #display the current input values
    canvas.create_text(*INPUTPOINT, font=font_+" 7", text = "Charging Input")
    canvas.create_text(*INPUTVALUE, font=font_+" 7", text = input_value + "W")
    canvas.create_text(*TIMETOFULL, font=font_+" 7", text = "Time to Full")
    canvas.create_text(*TIMETOFULLMINS, font=font_+" 7", text = time_to_full_mins + " mins")

    #display the current output values
    #the car charger being active display will the Active or Ready
    if (car_charger_active == "y"):
        if (car_charger_status == "1"):
            canvas.create_text(*OUTPUTPOINT, fill="red", font=font_ + " 8", text="ACTIVE")
        else:
            canvas.create_text(*OUTPUTPOINT, font=font_ + " 8", text="READY")

    else:
        if (output_value >= "200"):
            canvas.create_text(*OUTPUTPOINT, fill="red", font=font_ + " 7", text="Total Output")
            canvas.create_text(*OUTPUTVALUE, fill="red", font=font_ + " 7", text=output_value + "W")
        else:
            canvas.create_text(*OUTPUTPOINT, font=font_+" 7", text="Total Output")
            canvas.create_text(*OUTPUTVALUE, font=font_+" 7", text=output_value + "W")

        canvas.create_text(*TIMETOEMPTY, font=font_+" 7", text="Time to Empty")
        canvas.create_text(*TIMETOEMPTYMINS, font=font_+" 7", text= time_to_empty_mins + " mins")

        canvas.create_text(*DCPOINT, font=font_+" 7", text= dc_input_value + "V DC")
        #canvas.create_text(*DCPOINTENTER, font=font_ + " 7", text="Input")

    #display a heat warning if necessary
    if (heat_warning == "y"):
        canvas.create_text(*HEATWARNING, fill="red", font=font_+" 10", text="HEAT!")

    #display the Settings menu if selected
    if (settings_active == "y"):
        canvas.delete("all")
        canvas.create_text(100, 10, font=font_ + " 8", text="Settings Menu")

        if (setting_selected == "1"):
            canvas.create_text(100, 30, fill="red", font=font_ + " 7", text="1. Begin Car Starter Charging")
            canvas.create_text(100, 45, font=font_ + " 7", text="2. Update Software")
        else:
            canvas.create_text(100, 30, font=font_ + " 7", text="1. Begin Car Starter Charging")
            canvas.create_text(100, 45, fill="red", font=font_ + " 7", text="2. Update Software")

    #display the software update screen if selected
    if (updating_software_active == "y"):
        canvas.delete("all")
        canvas.create_text(100, 30, font=font_ + " 8", text="Updating Software")
        canvas.create_text(100, 45, font=font_ + " 8", text= update_progress+"%")

    canvas.pack()
    root.after(1000, update)  #time until display refresh

#run initial time
update()

#keep display open until it is closed
root.mainloop()
