import fsoa_adren_calculation as fsoa
import tkinter as tk

class fsoaCalc:

    def __init__(self, root):
        self.root = root
        root.title('FSOA Adrenaline Calculator')

    def create_window(self):
        """ window geometry """
        # modify these to dependent values later
        full_width = 0
        full_height = 0
        monitor_centre_x = int(root.winfo_screenwidth() / 2 - full_width / 2)
        monitor_centre_y = int(root.winfo_screenheight() / 2 - full_height / 2)
        root.geometry(f"{full_width}x{full_height}+{monitor_centre_x}+{monitor_centre_y}")
        root.minsize(full_width, full_height)

""" Gui """
root = tk.Tk()

"""drop down menus
ability, adrenaline, crit buffs (with max crit chance selection available), tsunami, natty, vigour, invigorating rank"""

# options_ability = tk.OptionMenu(root,)

root.mainloop()