from cfg_utils import argsparser, print_arguments, merge_cfg
from pipeline import main, start
import tkinter as tk
import paddle
import json
class DisplayUI:
    def __init__(self, master):
        self.parser = argsparser()
        self.master = master

        # Read JSON data from file
        with open('region_setting.json') as file:
            data = json.load(file)
        # Print JSON data variables
        print(data['region_type'])
        print(data['line1'])
        print(data['line2'])

        self.region_type = data['region_type']
        master.title("Simple Control UI")
        master.geometry("400x500")

        # Initialize the two numbers
        self.num1 = int(data['line1'])
        self.num2 = int(data['line2'])

        self.label = tk.Label(root, text="Welcome to APM Control UI")
        self.label.pack()
        self.label_msg = tk.Label(root, text=self.region_type
                                  )
        self.label_msg.pack()

        # Create the labels to display the numbers
        self.label1 = tk.Label(master, text="Line 1 (Door1 left): " + str(self.num1))
        self.label1.pack()

        self.label2 = tk.Label(master, text="Line 2 (Door2 right): " + str(self.num2))
        self.label2.pack()

        # Create the buttons to modify the numbers
        self.button1_add = tk.Button(master, text="+", command=self.add_num1)
        self.button1_add.place(x=25, y=220)

        self.button1_sub = tk.Button(master, text="-", command=self.sub_num1)
        self.button1_sub.place(x=45, y=220)

        self.button2_add = tk.Button(master, text="+", command=self.add_num2)
        self.button2_add.place(x=340, y=220)

        self.button2_sub = tk.Button(master, text="-", command=self.sub_num2)
        self.button2_sub.place(x=360, y=220)

        # Create the buttons to modify the door status

        self.button1 = tk.Button(root, text="Door 1 Open (Right)", command=self.get_door1)
        self.button1.config(width=20, height=2)
        self.button1.place(x=25, y=100)


        self.button2 = tk.Button(root, text="Door 2 Open (Left)", command=self.get_door2)
        self.button2.config(width=20, height=2)
        self.button2.place(x=225, y=100)

        self.button3 = tk.Button(root, text="Door 3 Open (Both)", command=self.get_door3)
        self.button3.config(width=20, height=2)
        self.button3.place(x=25, y=150)

        self.button4 = tk.Button(root, text="Door all closed", command=self.get_door4)
        self.button4.config(width=20, height=2)
        self.button4.place(x=225, y=150)

        # Create the buttons to start/end the program
        self.button5 = tk.Button(root, text="Start with video", command=self.video_start)
        self.button5.config(width=15, height=2)
        self.button5.place(x=25, y=300)

        self.button6 = tk.Button(root, text="Start without video", command=self.NOvideo_start)
        self.button6.config(width=15, height=2)
        self.button6.place(x=150, y=300)

        self.button7 = tk.Button(root, text="Stop/End", command=self.end)
        self.button7.config(width=15, height=2)
        self.button7.place(x=280, y=300)

    def add_num1(self):
        self.num1 += 1
        self.update_labels()

    def sub_num1(self):
        self.num1 -= 1
        self.update_labels()

    def add_num2(self):
        self.num2 += 1
        self.update_labels()

    def sub_num2(self):
        self.num2 -= 1
        self.update_labels()

    def update_labels(self):
        if self.num1 >= 0 and self.num2 >= 0:
            self.label1.config(text="Line 1 (Door1 left): " + str(self.num1))
            self.label2.config(text="Line 2 (Door2 right): " + str(self.num2))
            args = self.parser.set_defaults(line1=str(self.num1))
            args = self.parser.set_defaults(line2=str(self.num2))
            self.update_json()

        else:
            if self.num1 < 0:
                self.num1 = 0
            if self.num2 < 0:
                self.num2 = 0
            self.label1.config(text="Line 1 (Door1 left): " + str(self.num1))
            self.label2.config(text="Line 2 (Door2 right): " + str(self.num2))
            args = self.parser.set_defaults(line1=str(self.num1))
            args = self.parser.set_defaults(line2=str(self.num2))
            self.update_json()

    def get_door1(self):
        self.label_msg.config(text="right opened")
        args = self.parser.set_defaults(region_type="right")
        self.region_type = "right"
        self.update_json()
        return "right"

    def get_door2(self):
        self.label_msg.config(text="left opened")
        args = self.parser.set_defaults(region_type="left")
        self.region_type = "left"
        self.update_json()
        return "left"

    def get_door3(self):
        self.label_msg.config(text="both opened")
        args = self.parser.set_defaults(region_type="both")
        self.region_type = "both"
        self.update_json()
        return "both"

    def get_door4(self):
        self.label_msg.config(text="Door Closed")
        args = self.parser.set_defaults(region_type= "closed")
        self.region_type = "closed"
        self.update_json()
        return "closed"

    def video_start(self):
        self.label.config(text="Start with video")
        args = self.parser.set_defaults(play_local=True)
        start()
        return "video start"

    def NOvideo_start(self):
        self.label.config(text="Start without video")
        args = self.parser.set_defaults(play_local=False)
        start()
        return "NOvideo start"

    def end(self):
        self.label.config(text="Program ended")
        import sys
        sys.exit(0)
        return "end"

    def update_json(self):
        # Write JSON data to file
        data = {
            "region_type": self.region_type,
            "line1": str(self.num1),
            "line2": str(self.num2)
        }

        with open('region_setting.json', 'w') as file:
            json.dump(data, file)

# Create the main window
root = tk.Tk()

# Initialize the DisplayUI class
display_ui = DisplayUI(root)

# Start the main loop
root.mainloop()
