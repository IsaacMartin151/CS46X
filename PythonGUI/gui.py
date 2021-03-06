import tkinter as tk
import numpy as np
import random
import gaugelib
import time 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Main screen starts at line 173 
# Fuel screen starts at line 579 
# Ox   screen starts at line 820

#iterators for graphs/dummy data, replace with time values when DAQ is hooked up
i = 1
k = 0

plotDPI = 60 #used for spacing

#for placeholder input values for dial
g_value=0 
x=0


# Button states
global fuel_button_on
global oxidizer_button_on
global command_button_on

global fuel_press_on
global fuel_vent_on
global fuel_isolation_on
global fuel_purge_on
global fuel_main_on

global lox_press_on
global lox_vent_on
global lox_isolation_on
global lox_chill_on
global lox_main_on

global nanny_on
global sensor_stop_on
global cycle_valves_on
global cycle_vent_on
global data_live_on
global fire_on
global engine_start_up_on
global abort_on

fuel_nogo_on = False
oxidizer_nogo_on = False
command_nogo_on = False

fuel_press_on = True
fuel_vent_on = True
fuel_isolation_on = True
fuel_purge_on = True
fuel_main_on = True

lox_press_on = True
lox_vent_on = True
lox_isolation_on = True
lox_chill_on = True
lox_main_on = True
lox_fill_on = True

nanny_on = False
sensor_stop_on = False
cycle_valves_on = False
cycle_vent_on = False
data_live_on = False
fire_on = False
engine_start_up_on = False
abort_on = False

# Each of these functions are called when their corresponding button is pressed. 
# Right now it just toggles them on/off and their color is updated accordingly
def command_nogo_toggle():
    global command_nogo_on
    command_nogo_on = not command_nogo_on

def fuel_nogo_toggle():
    global fuel_nogo_on
    fuel_nogo_on = not fuel_nogo_on

def oxidizer_nogo_toggle():
    global oxidizer_nogo_on
    oxidizer_nogo_on = not oxidizer_nogo_on

def nanny_toggle():
    global nanny_on
    nanny_on = not nanny_on

def sensor_stop_toggle():
    global sensor_stop_on
    sensor_stop_on = not sensor_stop_on

def cycle_valves_toggle():
    global cycle_valves_on
    cycle_valves_on = not cycle_valves_on

def cycle_vent_toggle():
    global cycle_vent_on
    cycle_vent_on = not cycle_vent_on

def data_live_toggle():
    global data_live_on
    data_live_on = not data_live_on


def fuel_vent_toggle():
    global fuel_vent_on
    fuel_vent_on = not fuel_vent_on

def fuel_press_toggle():
    global fuel_press_on
    fuel_press_on = not fuel_press_on

def fuel_isolation_toggle():
    global fuel_isolation_on
    fuel_isolation_on = not fuel_isolation_on

def fuel_purge_toggle():
    global fuel_purge_on
    fuel_purge_on = not fuel_purge_on

def fuel_main_toggle():
    global fuel_main_on
    fuel_main_on = not fuel_main_on


def lox_vent_toggle():
    global lox_vent_on
    lox_vent_on = not lox_vent_on

def lox_press_toggle():
    global lox_press_on
    lox_press_on = not lox_press_on

def lox_isolation_toggle():
    global lox_isolation_on
    lox_isolation_on = not lox_isolation_on

def lox_chill_toggle():
    global lox_chill_on
    lox_chill_on = not lox_chill_on

def lox_main_toggle():
    global lox_main_on
    lox_main_on = not lox_main_on

def lox_fill_toggle():
    global lox_fill_on
    lox_fill_on = not lox_fill_on

def fire_toggle():
    global fire_on
    fire_on = not fire_on

def engine_start_up_toggle():
    global engine_start_up_on
    engine_start_up_on = not engine_start_up_on

def abort_toggle():
    global abort_on
    abort_on = not abort_on

# Code for the Main Control Screen
class MainScreen:
    def __init__(self):
        #Setting variables for the GUI's main display
        self.width = 1600
        self.height = 900

        self.standardizedButtonHeight = 2
        self.standardizedButtonWidth = 25
        self.startingHeight = 350
        self.heightSpacing = 40

        self.timesDisplayed = 0

        #Dummy data
        self.x1 = 10
        self.x2 = 13
        self.x3 = 23

        self.root = tk.Tk()
        self.canvas1 = tk.Canvas(self.root, width = self.width, height = self.height)
        self.canvas1.pack()

        self.background_image = tk.PhotoImage(file = "./background.png", width=self.width, height=self.height)
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, width=self.width, height=self.height)
        

        self.label1 = tk.Label(self.root, text='Control Panel')
        self.label1.config(font=('Arial', 20))
        self.rateLabel = tk.Label(self.root, text='Times Displayed: 0, Avg refresh time: 99999')
        self.rateLabel.config(font=('Arial', 12))
        self.canvas1.create_window(self.width/2, 50, window=self.label1)
        self.canvas1.create_window(self.width/4*3, 50, window=self.rateLabel)

        # Creating the data for the top three buttons
        self.fuel_nogo_button     = tk.Button(self.root, text=' FUEL \'NOGO\' ', command=fuel_nogo_toggle, bg='red', font=('Arial', 11))
        self.oxidizer_nogo_button = tk.Button(self.root, text=' OXIDIZER \'NOGO\' ', command=oxidizer_nogo_toggle, bg='red', font=('Arial', 11))
        self.command_nogo_button  = tk.Button(self.root, text=' COMMAND \'NOGO\' ', command=command_nogo_toggle, bg='red', font=('Arial', 11))
        self.nanny_button    = tk.Button(self.root, text='    Nanny \'OFF\'    ', command=nanny_toggle, bg='pink', font=('Arial', 11))

        # Side buttons
        self.sensor_stop_button  = tk.Button(self.root, text=' Sensor Stop ', command=sensor_stop_toggle, fg='red', bg='gray80', font=('Arial', 11))
        self.cycle_valves_button = tk.Button(self.root, text=' Valve Sequence OFF ', command=cycle_valves_toggle, bg='gray80', font=('Arial', 11))
        self.cycle_vent_button   = tk.Button(self.root, text=' Cycle Vent OFF ', command=cycle_vent_toggle, bg='gray80', font=('Arial', 11))
        self.data_live_button    = tk.Button(self.root, text=' DATA PAUSED ', command=data_live_toggle, bg='gray90', font=('Arial', 11))

        # Creating the data for the left column of center buttons
        self.fuel_press_button     = tk.Button(self.root, text=' ABV-PR-120 (FUEL PRESS) ', command=fuel_press_toggle, bg='green2', font=('Arial', 10))
        self.fuel_vent_button      = tk.Button(self.root, text=' ABV-FU-310 (FUEL VENT) ', command=fuel_vent_toggle, bg='orange', font=('Arial', 10))
        self.fuel_isolation_button = tk.Button(self.root, text=' ABV-FU-320 (FUEL ISOLATION) ', command=fuel_isolation_toggle, bg='orange', font=('Arial', 10))
        self.fuel_purge_button     = tk.Button(self.root, text=' ABV-FU-330 (FUEL PURGE) ', command=fuel_purge_toggle, bg='orange', font=('Arial', 10))
        self.fuel_main_button      = tk.Button(self.root, text=' ABV-FU-340 (FUEL MAIN) ', command=fuel_main_toggle, bg='orange', font=('Arial', 10))

        # Creating the data for the right column of center buttons
        self.lox_press_button     = tk.Button(self.root, text=' ABV-PR-110 (LOx PRESS) ', command=lox_press_toggle, bg='green2', font=('Arial', 10))
        self.lox_vent_button      = tk.Button(self.root, text=' ABV-OX-210 (LOx VENT) ', command=lox_vent_toggle, bg='cyan', font=('Arial', 10))
        self.lox_isolation_button = tk.Button(self.root, text=' ABV-OX-220 (LOx ISOLATION) ', command=lox_isolation_toggle, bg='cyan', font=('Arial', 10))
        self.lox_chill_button     = tk.Button(self.root, text=' ABV-OX-230 (LOx CHILL) ', command=lox_chill_toggle, bg='cyan', font=('Arial', 10))
        self.lox_main_button      = tk.Button(self.root, text=' ABV-OX-240 (LOx MAIN) ', command=lox_main_toggle, bg='cyan', font=('Arial', 10))
        self.lox_fill_button      = tk.Button(self.root, text=' ABV-OX-250 (LOx FILL) ', command=lox_fill_toggle, bg='cyan', font=('Arial', 10))

        self.fire_button            = tk.Button(self.root, text=' FIRE ', command=fire_toggle, fg='white', bg='black', font=('Arial', 10))
        self.engine_start_up_button = tk.Button(self.root, text=' Engine Start Up ', command=engine_start_up_toggle, bg='gray80', font=('Arial', 10))
        self.abort_button           = tk.Button(self.root, text='    ABORT    ', command=abort_toggle, bg='red', font=('Arial', 11))

        self.mylist = tk.Listbox(self.root, width=100)
        global k
        for line in range(50):
           k += 1
           t = time.localtime()
           current_time = time.strftime("%H:%M:%S", t)
           #print(current_time)
           self.mylist.insert(0, current_time + "  " + str(line) + ' Filler text, status update stuff, etc' + str(line))
           if (line % 5 == 0):
              self.mylist.itemconfig(0, bg = "red")
        
        self.mylist.place(x=self.width/2 - 300, y=self.height-300 )

        #Dials for this screen
        self.p1 = gaugelib.DrawGauge2(
            self.root,
            max_value = 1500.0,
            min_value = 0.0,
            size = 200,
            bg_col = 'black',
            unit = "PT-FU-310 (FUEL TANK)",bg_sel = 2)
        self.p1.place(x=0, y=250)

        self.p2 = gaugelib.DrawGauge2(
            self.root,
            max_value = 3000.0,
            min_value = 0.0,
            size = 200,
            bg_col = 'black',
            unit = "PT-FU-120 (FUEL REGULATOR)",bg_sel = 2)
        self.p2.place(x=220, y=250)

        self.p3 = gaugelib.DrawGauge2(
            self.root,
            max_value = 1500.0,
            min_value = 0.0,
            size = 200,
            bg_col ='black',
            unit = "PT-FU-320 (FUEL MAIN LINE)",bg_sel = 2)
        self.p3.place(x=0, y=470)
        
        self.p4 = gaugelib.DrawGauge2(
            self.root,
            max_value= 3000.0,
            min_value= 0.0,
            size=200,
            bg_col='black',
            unit = "PT-OX-130 (LOx REGULATOR)",bg_sel = 2)
        self.p4.place(x=1090, y=250)

        self.p5 = gaugelib.DrawGauge2(
            self.root,
            max_value = 1500.0,
            min_value = 0.0,
            size = 200,
            bg_col ='black',
            unit = "PT-OX-210 (LOx TANK)",bg_sel = 2)
        self.p5.place(x=1300, y=250)

        self.p6 = gaugelib.DrawGauge2(
            self.root,
            max_value = 1500.0,
            min_value = 0.0,
            size = 200,
            bg_col ='black',
            unit = "PT-OX-220 (LOx MAIN LINE)",bg_sel = 2)
        self.p6.place(x=1300, y=470)
        self.timeStarted = time.time()


        self.read_every_second()


    def read_every_second(self):
        global x
        self.p1.set_value(0)
        self.p2.set_value(0)
        self.p3.set_value(0)
        self.p4.set_value(0)
        x+=1
        if x>100:
            #        graph1.draw_axes()
            x=0
        self.root.after(100, self.read_every_second)



    #set uniform sizes for buttons that don't have unique sizes
    def initialize_configurations(self):
        self.fuel_nogo_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.oxidizer_nogo_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.command_nogo_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)

        self.sensor_stop_button.config(height=self.standardizedButtonHeight, width= self.standardizedButtonWidth//2)
        self.cycle_valves_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth//2)
        self.cycle_vent_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth//2)
        self.data_live_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth//2)

        self.fuel_press_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.fuel_vent_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.fuel_isolation_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.fuel_purge_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.fuel_main_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.lox_press_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.lox_vent_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.lox_isolation_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.lox_chill_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.lox_main_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.lox_fill_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)

        self.fire_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth//2 - 1)
        self.engine_start_up_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth//2 - 1)


    #Draw the buttons based on their current state
    def draw_buttons(self):
        self.canvas1.create_window(self.width/2 + self.width/4, 180, window=self.fuel_nogo_button)
        self.canvas1.create_window(self.width/2 - self.width/4, 180, window=self.oxidizer_nogo_button)
        self.canvas1.create_window(self.width/2, 180, window=self.command_nogo_button)
        self.canvas1.create_window(self.width/2, 120, window=self.nanny_button)

        self.canvas1.create_window(self.width/2 - self.width/4, self.startingHeight + self.heightSpacing*3, window=self.sensor_stop_button)
        self.canvas1.create_window(self.width/2 - self.width/4, self.startingHeight + self.heightSpacing*5, window=self.cycle_valves_button)
        self.canvas1.create_window(self.width/2 - self.width/4, self.startingHeight + self.heightSpacing*6, window=self.cycle_vent_button)
        self.canvas1.create_window(self.width/2 + self.width/4 - 100, self.startingHeight + self.heightSpacing*3, window=self.data_live_button)

        self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*0, window=self.lox_press_button)
        self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*1, window=self.lox_vent_button)
        self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*2, window=self.lox_isolation_button)
        self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*3, window=self.lox_chill_button)
        self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*4, window=self.lox_main_button)
        self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*5, window=self.lox_fill_button)
        self.canvas1.create_window(self.width/2 - 120, self.startingHeight + self.heightSpacing*0, window=self.fuel_press_button)
        self.canvas1.create_window(self.width/2 - 120, self.startingHeight + self.heightSpacing*1, window=self.fuel_vent_button)
        self.canvas1.create_window(self.width/2 - 120, self.startingHeight + self.heightSpacing*2, window=self.fuel_isolation_button)
        self.canvas1.create_window(self.width/2 - 120, self.startingHeight + self.heightSpacing*3, window=self.fuel_purge_button)
        self.canvas1.create_window(self.width/2 - 120, self.startingHeight + self.heightSpacing*4, window=self.fuel_main_button)

        self.canvas1.create_window(self.width/2 + self.width/4, self.startingHeight + self.heightSpacing*5, window=self.fire_button)
        self.canvas1.create_window(self.width/2 + self.width/4, self.startingHeight + self.heightSpacing*6, window=self.engine_start_up_button)
        self.canvas1.create_window(self.width/2 + self.width/4, self.startingHeight + self.heightSpacing*7, window=self.abort_button)

    # change button appearance after toggle
    def configure_buttons(self):
        if fuel_nogo_on:
            self.fuel_nogo_button.configure(text=' FUEL \'GO\' ', bg='green2')
        else:
            self.fuel_nogo_button.configure(text=' FUEL \'NOGO\' ', bg='red')

        if oxidizer_nogo_on:
            self.oxidizer_nogo_button.configure(text=' OXIDIZER \'GO\' ', bg='green2')
        else:
            self.oxidizer_nogo_button.configure(text=' OXIDIZER \'NOGO\' ', bg='red')

        if command_nogo_on:
            self.command_nogo_button.configure(text=' COMMAND \'GO\' ', bg='green2')
        else:
            self.command_nogo_button.configure(text=' COMMAND \'NOGO\' ', bg='red')

        if nanny_on:
            self.nanny_button.configure(text='    Nanny \'ON\'    ', bg='yellow')
        else:
            self.nanny_button.configure(text='    Nanny \'OFF\'    ', bg='pink')

        if sensor_stop_on:
            self.sensor_stop_button.configure(bg='gray60')
        else:
            self.sensor_stop_button.configure(bg='gray80')

        if cycle_valves_on:
            self.cycle_valves_button.configure(text=' Cycle Valves ON ', bg='bisque')
        else:
            self.cycle_valves_button.configure(text=' Valve Seq OFF ', bg='gray80')

        if cycle_vent_on:
            self.cycle_vent_button.configure(text=' Cycle Vent ON ', bg='bisque')
        else:
            self.cycle_vent_button.configure(text=' Cycle Vent OFF ', bg='gray80')

        if data_live_on:
            self.data_live_button.configure(text=' DATA LIVE ', bg='SteelBlue1')
        else:
            self.data_live_button.configure(text=' DATA PAUSED ', bg='gray90')

        if fuel_press_on:
            self.fuel_press_button.configure(bg='green2')
        else:
            self.fuel_press_button.configure(bg='red')

        if fuel_vent_on:
            self.fuel_vent_button.configure(bg='orange')
        else:
            self.fuel_vent_button.configure(bg='red')

        if fuel_isolation_on:
            self.fuel_isolation_button.configure(bg='orange')
        else:
            self.fuel_isolation_button.configure(bg='red')

        if fuel_purge_on:
            self.fuel_purge_button.configure(bg='orange')
        else:
            self.fuel_purge_button.configure(bg='red')

        if fuel_main_on:
            self.fuel_main_button.configure(bg='orange')
        else:
            self.fuel_main_button.configure(bg='red')

        if lox_press_on:
            self.lox_press_button.configure(bg='green2')
        else:
            self.lox_press_button.configure(bg='red')

        if lox_vent_on:
            self.lox_vent_button.configure(bg='cyan')
        else:
            self.lox_vent_button.configure(bg='red')

        if lox_isolation_on:
            self.lox_isolation_button.configure(bg='cyan')
        else:
            self.lox_isolation_button.configure(bg='red')

        if lox_chill_on:
            self.lox_chill_button.configure(bg='cyan')
        else:
            self.lox_chill_button.configure(bg='red')

        if lox_main_on:
            self.lox_main_button.configure(bg='cyan')
        else:
            self.lox_main_button.configure(bg='red')

        if lox_fill_on:
            self.lox_fill_button.configure(bg='cyan')
        else:
            self.lox_fill_button.configure(bg='red')

        if fire_on:
            self.fire_button.configure(text=' FIRING ', fg='black', bg='yellow')
        else:
            self.fire_button.configure(text=' FIRE ', fg='white', bg='black')

        if engine_start_up_on:
            self.engine_start_up_button.configure(text=' Start Up Timing ON ', bg='bisque')
        else:
            self.engine_start_up_button.configure(text=' Engine Start Up ', bg='gray80')

        if abort_on:
            self.abort_button.configure(text='    ABORT TRIPPED    ', bg='yellow')
        else:
            self.abort_button.configure(text='    ABORT    ', bg='red')

        self.timesDisplayed += 1

        #self.rateLabel = tk.Label(self.root, text='Times Displayed: 0, Avg refresh time: 99999')
        self.rateLabel.config(text="Times Displayed: "+str(self.timesDisplayed)+", Avg refresh time: "+str((time.time()-self.timeStarted)/self.timesDisplayed))

        self.root.after(16, self.configure_buttons)


    def create_charts(self):
        # These are data values at the top of this function
        global i
        global k

        x = np.linspace(0, 100, num=50)
        i += 1
        k += .1
        k = k % 200
        y = np.sin(2 * np.pi * x + k)
        self.canvas1.delete(self.subplot7)
        self.subplot7.clear()
        self.subplot7.plot(x, y, color = 'lightsteelblue')
        #self.figure7.draw()
        self.scatter1 = FigureCanvasTkAgg(self.figure7, self.root)
        self.scatter1.get_tk_widget().place(x=700, y=550)
        #self.root.after(100, self.create_charts)

    def create_charts2(self):
        #Left side charts
        x1 = self.x1
        x2 = self.x2
        x3 = self.x3
        figure1 = Figure(figsize=(4,3), dpi=plotDPI)
        subplot1 = figure1.add_subplot(111)
        xAxis = [float(x1),float(x2),float(x3)]
        yAxis = [float(x1),float(x2),float(x3)]
        subplot1.bar(xAxis,yAxis, color = 'lightsteelblue')
        bar1 = FigureCanvasTkAgg(figure1, self.root)
        print("placing plot 1")
        bar1.get_tk_widget().place(x=0, y=50)

        figure2 = Figure(figsize=(4,3), dpi=plotDPI)
        subplot2 = figure2.add_subplot(111)
        labels2 = 'Fuel Level', 'Oxidizer\nLevel', 'Regulator\npressure'
        pieSizes = [float(x1),float(x2),float(x3)]
        my_colors2 = ['lightblue','lightsteelblue','silver']
        explode2 = (0, 0, 0)
        subplot2.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=False, startangle=90)
        subplot2.axis('equal')
        pie2 = FigureCanvasTkAgg(figure2, self.root)
        print("placing plot 2")
        pie2.get_tk_widget().place(x=0, y=250)

        figure3 = Figure(figsize=(4,3), dpi=plotDPI)
        subplot3 = figure3.add_subplot(111)
        xAxis2 = [float(x1),float(x2),float(x3)]
        yAxis2 = [float(x1),float(x2),float(x3)]
        subplot3.bar(xAxis2,yAxis2, color = 'lightsteelblue')
        bar2 = FigureCanvasTkAgg(figure3, self.root)
        print("placing plot 3")
        bar2.get_tk_widget().place(x=0, y=450)


        #Right side charts
        figure4 = Figure(figsize=(4,3), dpi=plotDPI)
        subplot4 = figure4.add_subplot(111)
        xAxis = [float(x1),float(x2),float(x3)]
        yAxis = [float(x1),float(x2),float(x3)]
        subplot4.bar(xAxis,yAxis, color = 'lightsteelblue')
        bar3 = FigureCanvasTkAgg(figure4, self.root)
        print("placing plot 4")
        bar3.get_tk_widget().place(x=1300, y=50)

        figure5 = Figure(figsize=(4,3), dpi=plotDPI)
        subplot5 = figure5.add_subplot(111)
        labels2 = 'Fuel Level', 'Oxidizer\nLevel', 'Regulator\npressure'
        pieSizes = [float(x1),float(x2),float(x3)]
        my_colors2 = ['lightblue','lightsteelblue','silver']
        explode2 = (0, 0, 0)
        subplot5.pie(pieSizes, colors=my_colors2, explode=explode2, labels=labels2, autopct='%1.1f%%', shadow=False, startangle=90)
        subplot5.axis('equal')
        pie3 = FigureCanvasTkAgg(figure5, self.root)
        print("placing plot 5")
        pie3.get_tk_widget().place(x=1300, y=250)

        figure6 = Figure(figsize=(4,3), dpi=plotDPI)
        subplot6 = figure6.add_subplot(111)
        xAxis2 = [float(x1),float(x2),float(x3)]
        yAxis2 = [float(x1),float(x2),float(x3)]
        subplot6.bar(xAxis2,yAxis2, color = 'lightsteelblue')
        bar4 = FigureCanvasTkAgg(figure6, self.root)
        print("placing plot 6")
        bar4.get_tk_widget().place(x=1300, y=450)

        self.create_charts()



class FuelScreen:
    def __init__(self):
        #Setting variables for the GUI's main display
        self.width = 1600
        self.height = 900

        self.standardizedButtonHeight = 2
        self.standardizedButtonWidth = 25
        self.startingHeight = 150
        self.heightSpacing = 40

        #Dummy data
        self.x1 = 10
        self.x2 = 13
        self.x3 = 23

        self.root = tk.Toplevel()
        self.canvas1 = tk.Canvas(self.root, width = self.width, height = self.height)
        self.background_image = tk.PhotoImage(file = "./backgroundrocketred.png")
        # Original artwork courtesy of u/wallpaper_master on HeroScreen
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.canvas1.pack()

        self.label1 = tk.Label(self.root, text='Fuel Control')
        self.label1.config(font=('Arial', 20))
        self.canvas1.create_window(self.width/2, 50, window=self.label1)

        # Creating the data for the top three buttons
        self.fuel_nogo_button     = tk.Button(self.root, text=' FUEL \'NOGO\' ', command=fuel_nogo_toggle, bg='red', font=('Arial', 11))
        # self.oxidizer_nogo_button = tk.Button(self.root, text=' OXIDIZER \'NOGO\' ', command=oxidizer_nogo_toggle, bg='red', font=('Arial', 11))
        self.nanny_button    = tk.Button(self.root, text='    Nanny \'OFF\'    ', command=nanny_toggle, bg='pink', font=('Arial', 11))

        # Creating the data for the left column of center buttons
        self.fuel_press_button     = tk.Button(self.root, text=' ABV-PR-120 (FUEL PRESS) ', command=fuel_press_toggle, bg='green2', font=('Arial', 10))
        self.fuel_vent_button      = tk.Button(self.root, text=' ABV-FU-310 (FUEL VENT) ', command=fuel_vent_toggle, bg='orange', font=('Arial', 10))
        self.fuel_isolation_button = tk.Button(self.root, text=' ABV-FU-320 (FUEL ISOLATION) ', command=fuel_isolation_toggle, bg='orange', font=('Arial', 10))
        self.fuel_purge_button     = tk.Button(self.root, text=' ABV-FU-330 (FUEL PURGE) ', command=fuel_purge_toggle, bg='orange', font=('Arial', 10))
        self.fuel_main_button      = tk.Button(self.root, text=' ABV-FU-340 (FUEL MAIN) ', command=fuel_main_toggle, bg='orange', font=('Arial', 10))

        # Creating the data for the right column of center buttons
        # self.lox_press_button     = tk.Button(self.root, text=' ABV-PR-110 (LOx PRESS) ', command=lox_press_toggle, bg='green2', font=('Arial', 10))
        # self.lox_vent_button      = tk.Button(self.root, text=' ABV-OX-210 (LOx VENT) ', command=lox_vent_toggle, bg='cyan', font=('Arial', 10))
        # self.lox_isolation_button = tk.Button(self.root, text=' ABV-OX-220 (LOx ISOLATION) ', command=lox_isolation_toggle, bg='cyan', font=('Arial', 10))
        # self.lox_chill_button     = tk.Button(self.root, text=' ABV-OX-230 (LOx CHILL) ', command=lox_chill_toggle, bg='cyan', font=('Arial', 10))
        # self.lox_main_button      = tk.Button(self.root, text=' ABV-OX-240 (LOx MAIN) ', command=lox_main_toggle, bg='cyan', font=('Arial', 10))
        # self.lox_fill_button      = tk.Button(self.root, text=' ABV-OX-250 (LOx FILL) ', command=lox_fill_toggle, bg='cyan', font=('Arial', 10))

        self.fire_button            = tk.Button(self.root, text='FIRE', command=fire_toggle, fg='white', bg='black', font=('Arial', 10))
        self.abort_button           = tk.Button(self.root, text='ABORT', command=abort_toggle, bg='red', font=('Arial', 11))


    #set uniform sizes for buttons that don't have unique sizes
    def initialize_configurations(self):
        self.fuel_nogo_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        # self.oxidizer_nogo_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)

        self.fuel_press_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.fuel_vent_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.fuel_isolation_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.fuel_purge_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        self.fuel_main_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)

        # self.lox_press_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        # self.lox_vent_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        # self.lox_isolation_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        # self.lox_chill_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        # self.lox_main_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)
        # self.lox_fill_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth)

        self.fire_button.config(height=self.standardizedButtonHeight, width=self.standardizedButtonWidth//2 - 1)


    def draw_buttons(self):
        #Draw the buttons based on their current state
        self.canvas1.create_window(self.width/2 + self.width/4, 180, window=self.fuel_nogo_button)
        # self.canvas1.create_window(self.width/2 - self.width/4, 180, window=self.oxidizer_nogo_button)

        # self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*0, window=self.lox_press_button)
        # self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*1, window=self.lox_vent_button)
        # self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*2, window=self.lox_isolation_button)
        # self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*3, window=self.lox_chill_button)
        # self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*4, window=self.lox_main_button)
        # self.canvas1.create_window(self.width/2 + 120, self.startingHeight + self.heightSpacing*5, window=self.lox_fill_button)

        self.canvas1.create_window(self.width/2 - 0, self.startingHeight + self.heightSpacing*0, window=self.fuel_press_button)
        self.canvas1.create_window(self.width/2 - 0, self.startingHeight + self.heightSpacing*1, window=self.fuel_vent_button)
        self.canvas1.create_window(self.width/2 - 0, self.startingHeight + self.heightSpacing*2, window=self.fuel_isolation_button)
        self.canvas1.create_window(self.width/2 - 0, self.startingHeight + self.heightSpacing*3, window=self.fuel_purge_button)
        self.canvas1.create_window(self.width/2 - 0, self.startingHeight + self.heightSpacing*4, window=self.fuel_main_button)

        self.canvas1.create_window(self.width/2 + self.width/3, self.startingHeight + 200 + self.heightSpacing*6, window=self.nanny_button)
        self.canvas1.create_window(self.width/2 + self.width/3, self.startingHeight + 200 + self.heightSpacing*7, window=self.fire_button)
        self.canvas1.create_window(self.width/2 + self.width/3, self.startingHeight + 200 + self.heightSpacing*8, window=self.abort_button)


    # change button appearance after toggle
    def configure_buttons(self):
        global fuel_button_on
        # global oxidizer_button_on
        global command_button_on

        global fuel_press_on
        global fuel_vent_on
        global fuel_isolation_on
        global fuel_purge_on
        global fuel_main_on
        # global lox_press_on
        # global lox_vent_on
        # global lox_isolation_on
        # global lox_chill_on
        # global lox_main_on

        global nanny_on
        global fire_on
        global abort_on

        if fuel_nogo_on:
            self.fuel_nogo_button.configure(text=' FUEL \'GO\' ', bg='green2')
        else:
            self.fuel_nogo_button.configure(text=' FUEL \'NOGO\' ', bg='red')

        # if oxidizer_nogo_on:
        #     self.oxidizer_nogo_button.configure(text=' OXIDIZER \'GO\' ', bg='green2')
        # else:
        #     self.oxidizer_nogo_button.configure(text=' OXIDIZER \'NOGO\' ', bg='red')

        if nanny_on:
            self.nanny_button.configure(text='    Nanny \'ON\'    ', bg='yellow')
        else:
            self.nanny_button.configure(text='    Nanny \'OFF\'    ', bg='pink')

        if fuel_press_on:
            self.fuel_press_button.configure(bg='green2')
        else:
            self.fuel_press_button.configure(bg='red')

        if fuel_vent_on:
            self.fuel_vent_button.configure(bg='orange')
        else:
            self.fuel_vent_button.configure(bg='red')

        if fuel_isolation_on:
            self.fuel_isolation_button.configure(bg='orange')
        else:
            self.fuel_isolation_button.configure(bg='red')

        if fuel_purge_on:
            self.fuel_purge_button.configure(bg='orange')
        else:
            self.fuel_purge_button.configure(bg='red')

        if fuel_main_on:
            self.fuel_main_button.configure(bg='orange')
        else:
            self.fuel_main_button.configure(bg='red')

        # if lox_press_on:
        #     self.lox_press_button.configure(bg='green2')
        # else:
        #     self.lox_press_button.configure(bg='red')
        #
        # if lox_vent_on:
        #     self.lox_vent_button.configure(bg='cyan')
        # else:
        #     self.lox_vent_button.configure(bg='red')
        #
        # if lox_isolation_on:
        #     self.lox_isolation_button.configure(bg='cyan')
        # else:
        #     self.lox_isolation_button.configure(bg='red')
        #
        # if lox_chill_on:
        #     self.lox_chill_button.configure(bg='cyan')
        # else:
        #     self.lox_chill_button.configure(bg='red')
        #
        # if lox_main_on:
        #     self.lox_main_button.configure(bg='cyan')
        # else:
        #     self.lox_main_button.configure(bg='red')
        #
        # if lox_fill_on:
        #     self.lox_fill_button.configure(bg='cyan')
        # else:
        #     self.lox_fill_button.configure(bg='red')

        if fire_on:
            self.fire_button.configure(text=' FIRING ', fg='black', bg='yellow')
        else:
            self.fire_button.configure(text=' FIRE ', fg='white', bg='black')

        if abort_on:
            self.abort_button.configure(text='    ABORT TRIPPED    ', bg='yellow')
        else:
            self.abort_button.configure(text='    ABORT    ', bg='red')

        self.root.after(16, self.configure_buttons)

    def create_charts(self):
        # These are data values at the top of this function
        global i
        global k
        figure7 = Figure(figsize=(6,4), dpi=plotDPI)
        subplot7 = figure7.add_subplot(111)
        x = np.linspace(0, 100, 50)
        #print("i is ", i)
        y = np.cos(2 * np.pi * x + k)
        subplot7.plot(x, y, color = 'lightsteelblue', label="Pressure 1")
        x = np.linspace(0, 100, 50)
        #print("i is ", i)
        y = np.sin(2 * np.pi * x + k)
        subplot7.plot(x, y, color = 'orange', label="Pressure 2")
        #subplot4.title("Connected Scatterplot points with line")
        subplot7.set_xlabel("Time")
        subplot7.set_ylabel("Pressure")
        subplot7.legend()
        scatter1 = FigureCanvasTkAgg(figure7, self.root)
        scatter1.get_tk_widget().place(x=100, y=50)

        w1 = tk.Scale(self.root, from_=0, to=120, orient=tk.HORIZONTAL, length=300, label="Fuel Tank Relief Temp", width=10, bg="#fcb603")
        w1.set(19)
        w1.place(x=100, y=450)
        w2 = tk.Scale(self.root, from_=0, to=120, orient=tk.HORIZONTAL, length=300, label="Fuel Main Line Temp", width=10, bg="#fcb603")
        w2.set(32)
        w2.place(x=100, y=500)
        w3 = tk.Scale(self.root, from_=0, to=120, orient=tk.HORIZONTAL, length=300, label="Fuel Venturi Temp", width=10, bg="#fcb603")
        w3.set(57)
        w3.place(x=100, y=550)
        w4 = tk.Scale(self.root, from_=0, to=120, orient=tk.HORIZONTAL, length=300, label="Fuel Main Valve Temp", width=10, bg="#fcb603")
        w4.set(75)
        w4.place(x=100, y=600)
        # Chill Relief is only for OX
        #w5 = tk.Scale(self.root, from_=0, to=120, orient=tk.HORIZONTAL, length=300, label="Fuel Chill Relief Temp", width=10, bg="#fcb603")
        #w5.set(75)
        #w5.place(x=100, y=650)
        w6 = tk.Scale(self.root, from_=0, to=120, orient=tk.HORIZONTAL, length=300, label="Fuel Chill Line Temp", width=10, bg="#fcb603")
        w6.set(75)
        w6.place(x=100, y=650)
        #self.root.after(250, self.create_charts)


bruh = MainScreen()
bruh.initialize_configurations()
#bruh.create_charts2()
bruh.root.after(100, bruh.configure_buttons())
bruh.draw_buttons()

oof = FuelScreen()
oof.initialize_configurations()
oof.create_charts()
oof.root.after(100, oof.configure_buttons())
oof.draw_buttons()

#Continuously display the Screens
#clear_output(wait=True)
# bruh.configure_buttons()


while True:
    bruh.root.update()

    #oof.root.after(1000, oof.create_charts)
    #oof.root.update()

#bruh.root.mainloop()
#oof.root.mainloop()
#clear_charts()
