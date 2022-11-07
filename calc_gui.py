import calculations # module with fsoa adrenaline calculations
import tkinter as tk # for GUI elements
import tkinter.ttk as ttk

def main() -> None:

    class fsoaCalc:

        def __init__(self, root):
            self.root = root
            root.title('FSOA Adrenaline Calculator')
            # will append all widgets to this list, so as to access them when I need
            self.widget_list = []

            # user-specific buffs
            self.user_buffs = calculations.zeroed_dict_of_buffs()

            # for alignment and sizing of columns (in tkinter grid system)
            # col_direction - so 0_x is col 0 in direction x
            self.col_padding = {
                "0_x": (8,0),
                "0_y": (0,0),
                "1_x": (0,8),
                "1_y": (0,0),
            }

            self.col_sticky = {
                "0": "W",
                "1": "EW"
            }

        def create_window(self):
            """ window geometry """
            # modify these to dependent values later
            full_width = 200
            full_height = 200
            monitor_centre_x = int(root.winfo_screenwidth() / 2 - full_width / 2)
            monitor_centre_y = int(root.winfo_screenheight() / 2 - full_height / 2)
            # root.geometry(f"{full_width}x{full_height}+{monitor_centre_x}+{monitor_centre_y}")
            # root.geometry(f"{full_width}x{full_height}+{monitor_centre_x}+{monitor_centre_y}")
            root.minsize(full_width, full_height)

        """ Custom Tkinter Widget Functions """
        def gui_label(self, row: int, col: int, text: str) -> None:
            my_label = ttk.Label(self.root, text=text)
            my_label.grid(row=row, column=col, sticky=self.get_col_sticky(col), padx=self.get_col_padding(col, "x"))

        def gui_combobox(self, row: int, col: int, text: str, values: list) -> None:
            self.combobox_var = tk.StringVar(root, value=text)
            my_combobox = ttk.Combobox(self.root, textvariable = self.combobox_var, values=values)
            my_combobox.grid(row=row, column=col, sticky=self.get_col_sticky(col), padx=self.get_col_padding(col, "x"))

        # gui entry box that takes an IntVar
        def gui_entry_int(self, row: int, col: int, **kwargs) -> None:
            # if a default_value is specified, place it in the widget as a default value
            if kwargs.get("default_value") != None:
                print(f'{kwargs.get("default_value")}')
                try: # check it's an integer
                    self.int_var = tk.IntVar(value=kwargs.get("default_value"))
                    print("it worked")
                except:
                    print("na mate")
                    self.int_var = tk.IntVar()
            else:
                print("u gave nothing")
                self.int_var = tk.IntVar()

            my_entry = ttk.Entry(self.root, width=10, textvariable=self.int_var)
            my_entry.grid(row=row, column=col, sticky=self.get_col_sticky(col), padx=self.get_col_padding(col, "x"))

        def gui_checkbutton(self, row: int, col: int, text: str) -> None:
            self.checkbutton_var = tk.IntVar(value=0) # default value 0
            my_checkbutton = ttk.Checkbutton(self.root, text=text, variable=self.checkbutton_var)
            my_checkbutton.grid(row=row, column=col, sticky=self.get_col_sticky(col), padx=self.get_col_padding(col, "x"))

        """ Styling Functions """

        # returns the relevant column padding tuple from the dictionary above
        # returns (0, 0) - zero padding - if a value isn't found for the column/direction specified
        def get_col_padding(self, col: int, direction: str):
            padding_tuple = self.col_padding.get(f"{col}_{direction}")
            if padding_tuple == None: # if value not found
                padding_tuple = (0, 0)
            return padding_tuple

        # get sticky direction for a column
        def get_col_sticky(self, col: int):
            col_sticky = self.col_sticky.get(f"{col}")
            if col_sticky == None: # if value not found
                col_sticky = "EW"
            return col_sticky

        """ Adding Widgets """
        def add_widgets(self):
            # Ability selection
            self.widget_list.append(self.gui_label(0, 0, "Select Ability: "))
            self.ability_list = calculations.list_of_abilities()
            self.widget_list.append(self.gui_combobox(0, 1, "Ability", values=self.ability_list))

            # Adrenaline goal
            self.widget_list.append(self.gui_label(1, 0, "Adrenaline Goal: "))
            self.widget_list.append(self.gui_entry_int(1, 1))

            # Biting
            self.widget_list.append(self.gui_label(2, 0, "Biting Rank: "))
            self.widget_list.append(self.gui_entry_int(2, 1, default_value=4))

            # # Invigorating
            # self.gui_label(3, 0, "Invigorating Rank:  ")













            # Ability selection
            # self.ability_label = ttk.Label(root, text="Select Ability: ")
            # self.ability_label.grid(row=0, column=0, sticky=self.col0_sticky, padx=self.col0_padx)
            # # ttk combobox
            # self.ability_list = calculations.list_of_abilities()
            # self.selected_ability = tk.StringVar(root, value="Ability")
            # self.ability_selection_menu = ttk.Combobox(root, textvariable=self.selected_ability, values=self.ability_list)
            # self.ability_selection_menu.grid(row=0, column=1, sticky=self.col1_sticky, padx=self.col1_padx) # sticky "EW" makes it stretch across entire grid column width

            # # Adrenaline goal
            # self.adrenaline_label = ttk.Label(root, text="Adrenaline Goal: ")
            # self.adrenaline_label.grid(row=1, column=0, sticky=self.col0_sticky, padx=self.col0_padx)
            # # Adrenaline 0-100
            # self.adrenaline_goal = tk.IntVar()
            # self.adrenaline_goal_field = ttk.Entry(root, width=10, textvariable=self.adrenaline_goal)
            # self.adrenaline_goal_field.grid(row=1, column=1, sticky=self.col1_sticky, padx=self.col1_padx)

            # """ Player buffs """
            # # Biting
            # self.biting_rank_label = ttk.Label(root, text="Biting Rank: ")
            # self.biting_rank_label.grid(row=2, column=0, sticky=self.col0_sticky, padx=self.col0_padx)
            # # biting rank 0-4
            # self.biting_rank = tk.IntVar(value=4)
            # self.biting_rank_field = ttk.Entry(root, width=10, textvariable=self.biting_rank)
            # self.biting_rank_field.grid(row=2, column=1, sticky=self.col1_sticky, padx=self.col1_padx)

            # # Invigorating
            # self.invigorating_rank_label = ttk.Label(root, text="Invigorating Rank: ")
            # self.invigorating_rank_label.grid(row=3, column=0, sticky=self.col0_sticky, padx=self.col0_padx)
            # # invigorating rank 0-4
            # self.invigorating_rank = tk.IntVar(value=4)
            # self.invigorating_rank_field = ttk.Entry(root, width=10, textvariable=self.invigorating_rank)
            # self.invigorating_rank_field.grid(row=3, column=1, sticky=self.col1_sticky, padx=self.col1_padx)

            # # Level 20 Gear?
            # self.level_20_gear = tk.IntVar(value=0)
            # self.level_20_gear_field = ttk.Checkbutton(root, text="Level 20 Gear", variable=self.level_20_gear)
            # self.level_20_gear_field.grid(row=4, column=0, sticky=self.col1_sticky, padx=self.col0_padx)

            # # Tsunami
            # self.selected_tsunami = tk.IntVar(value=0)
            # self.selected_tsunami_field = ttk.Checkbutton(root, text="Tsunami", variable=self.selected_tsunami)
            # self.selected_tsunami_field.grid(row=5, column=0, sticky=self.col1_sticky, padx=self.col0_padx)

            # # Natural Instinct
            # self.selected_natural_instinct = tk.IntVar(value=0)
            # self.selected_natural_instinct_field = ttk.Checkbutton(root, text="Natural Instinct", variable=self.selected_natural_instinct)
            # self.selected_natural_instinct_field.grid(row=6, column=0, sticky=self.col1_sticky, padx=self.col0_padx)

            # # additional crit buffs label
            # # self.additional_crit_buffs_label = ttk.Label(root, text="Additional Crit Buffs:")
            # # self.additional_crit_buffs_label.grid(row=7, column=0, sticky=self.col0_sticky)

            # # additional crit buffs
            # self.grimoire = tk.IntVar(value=0)
            # self.grimoire_checkbox = ttk.Checkbutton(root, text="Grimoire", variable=self.grimoire)
            # self.grimoire_checkbox.grid(row=4, column=1, sticky=self.col1_sticky, padx=self.col1_padx)

            # self.kalgerion_spec = tk.IntVar(value=0)
            # self.kalgerion_spec_field = ttk.Checkbutton(root, text="Kalgerion Spec", variable=self.kalgerion_spec)
            # self.kalgerion_spec_field.grid(row=5, column=1, sticky=self.col1_sticky, padx=self.col1_padx)

            # self.kalgerion_passive = tk.IntVar(value=0)
            # self.kalgerion_passive_field = ttk.Checkbutton(root, text="Kalgerion Passive", variable=self.kalgerion_passive)
            # self.kalgerion_passive_field.grid(row=6, column=1, sticky=self.col1_sticky, padx=self.col1_padx)

            # self.reavers_ring = tk.IntVar(value=0)
            # self.reavers_ring_field = ttk.Checkbutton(root, text="Reaver's Ring", variable=self.reavers_ring)
            # self.reavers_ring_field.grid(row=7, column=1, sticky=self.col1_sticky, padx=self.col1_padx)


    """ Gui """
    root = tk.Tk()
    calc_GUI = fsoaCalc(root)
    calc_GUI.create_window()
    calc_GUI.add_widgets()

    """ User buffs to be determined """
    user_buffs = calculations.zeroed_dict_of_buffs()

    """drop down menus
    ability, adrenaline, crit buffs (with max crit chance selection available), tsunami, natty, vigour, invigorating rank"""

    # # Ability selection
    # ability_label = tk.Label(root, text="Select Ability: ")
    # ability_label.grid(row=0, column=0, sticky="E")
    # # ttk combobox
    # ability_list = calculations.list_of_abilities()
    # selected_ability = tk.StringVar(root, value="Ability")
    # ability_selection_menu = ttk.Combobox(root, textvariable=selected_ability, values=ability_list)
    # ability_selection_menu.grid(row=0, column=1, sticky="EW", columnspan=2) # sticky "EW" makes it stretch across entire grid column width

    # # Adrenaline goal
    # adrenaline_label = ttk.Label(root, text="Adrenaline Goal: ")
    # adrenaline_label.grid(row=1, column=0, sticky="E")
    # # Adrenaline 0-100
    # adrenaline_goal = tk.IntVar()
    # adrenaline_goal_field = ttk.Entry(root, width=10, textvariable=adrenaline_goal)
    # adrenaline_goal_field.grid(row=1, column=1, sticky="EW", columnspan=2)

    # """ Player buffs """
    # # Biting
    # biting_rank_label = ttk.Label(root, text="Biting Rank:")
    # biting_rank_label.grid(row=2, column=0, sticky="E")
    # # biting rank 0-4
    # biting_rank = tk.IntVar(value=4)
    # biting_rank_field = ttk.Entry(root, width=10, textvariable=biting_rank)
    # biting_rank_field.grid(row=2, column=1, sticky="EW", columnspan=2)

    # # Invigorating
    # invigorating_rank_label = ttk.Label(root, text="Invigorating Rank:")
    # invigorating_rank_label.grid(row=3, column=0, sticky="E")
    # # invigorating rank 0-4
    # invigorating_rank = tk.IntVar(value=4)
    # invigorating_rank_field = ttk.Entry(root, width=10, textvariable=invigorating_rank)
    # invigorating_rank_field.grid(row=3, column=1, sticky="EW", columnspan=2)

    # # Tsunami
    # tsunami_label = ttk.Label(root, text="Tsunami Active?")
    # tsunami_label.grid(row=4, column=0, sticky="E")
    # # yes/no drop down
    # selected_tsunami = tk.StringVar(root)
    # selected_tsunami_menu = ttk.Combobox(root, textvariable=selected_tsunami, values=["Yes", "No"])
    # selected_tsunami_menu.grid(row=4, column=1, columnspan=2, sticky="EW")

    # # Natural Instinct
    # natural_instinct_label = ttk.Label(root, text="Natural Instinct Active?")
    # natural_instinct_label.grid(row=5, column=0, sticky="E")
    # # yes/no drop down
    # selected_natural_instinct = tk.StringVar(root)
    # selected_natural_instinct = ttk.Combobox(root, textvariable=selected_tsunami, values=["Yes", "No"])
    # selected_natural_instinct.grid(row=5, column=1, columnspan=2, sticky="EW")



    # empty field that shows error messages
    ##

    # options menu
    # ability_list = calculations.list_of_abilities()
    # selected_ability = tk.StringVar(value="Ability")
    # ability_selection_menu = tk.OptionMenu(root, selected_ability, *ability_list)
    # ability_selection_menu.grid(row=1, column=1, sticky="W", columnspan=2)

    # extract all the data the user has given you
    def run_calculation():
        # placeholder
        return

    """ Run Button """
    run_button = tk.Button(root, text="Submit", command=run_calculation)

    root.mainloop()

if __name__ == '__main__':
    main()