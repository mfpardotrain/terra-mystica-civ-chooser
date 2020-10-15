import random
import tkinter as tk
import os
import sys
from src.faction import Faction


class App:
    def __init__(self, win, n_choices):
        os.chdir(os.path.dirname(sys.argv[0]))
        self.win = win
        self.win.title("Terra Mystica Civ Chooser")
        self.win.geometry("800x500")
        tk.Label(self.win, text="Choose a Civ:").pack()

        self.n_choices = n_choices
        self.button_list = []
        self.to_choose = []
        self.previous_choices = []

        colors = ["Yellow", "Yellow", "Brown", "Brown", "Black", "Black", "Blue", "Blue", "Grey", "Grey", "Red", "Red",
                  "Green", "Green"]
        civs = ["Fakirs", "Nomads", "Halflings", "Cultists", "Darklings", "Alchemists", "Mermaids", "Swarmlings",
                "Engineers", "Dwarves", "Chaos_Magicians", "Giants", "Witches", "Auren"]
        self.factions = []
        for i in range(0, len(colors)):
            self.factions.append(Faction(color=colors[i], name=civs[i], image=f"images/{civs[i]}.gif", index=i,
                                 is_chosen=False, is_available=True))

        self.assign_picks()

        self.chosen_string = ""
        self.background_label = tk.Label(self.win)

        self.chosen_frame = tk.Frame(self.win)
        self.chosen_frame.pack(side="left")

        undo_frame = tk.Frame(self.win)
        undo_frame.pack(side="right")
        tk.Button(undo_frame, text="Undo Pick", command=self.undo).grid(row=6, column=5, padx=10)
        tk.Button(undo_frame, text="Refresh Choices", command=self.assign_picks).grid(row=7, column=5, pady=10, padx=5)

    def assign_picks(self):
        available_civs = [faction for faction in self.factions if faction.is_available]
        sample = random.sample(available_civs, self.n_choices)
        self.to_choose = [faction for faction in sample]
        self.render_button_choices()

    def render_button_choices(self):
        button_frame = tk.Frame(self.win)
        button_frame.pack()

        for i in range(self.n_choices):
            chosen_name = self.to_choose[i].name
            faction = self.to_choose[i]
            self.button_list.append(tk.Button(button_frame, text=chosen_name.replace("_", " "),
                                              command=lambda c=i: self.command(c), width=14))
            self.button_list[i].config(text=chosen_name.replace("_", " "))
            self.button_list[i].bind("<Enter>", lambda event, f=faction: self.on_enter(e=event, f=f))
            self.button_list[i].bind("<Leave>", self.on_leave)
            self.button_list[i].grid(row=0, column=i, padx=10, pady=5)

    def command(self, c):
        f = self.to_choose[c]
        n_chosen = len([faction for faction in self.factions if faction.is_chosen])
        other_color = [faction for faction in self.factions if faction.color == f.color][0]
        if n_chosen < 5:
            self.background_label.configure(image=None)
            self.background_label.photo = None
            self.background_label.pack()

            f.is_chosen = True
            f.is_available = False
            other_color.is_available = False

            self.previous_choices.append(self.to_choose)
            self.create_chosen_string()
            if n_chosen < 4:
                self.assign_picks()
        else:
            print("Error: cannot have more than 5 civs in a game.")

    def undo(self):
        n_chosen = len([faction for faction in self.factions if faction.is_chosen])
        last_choices = self.previous_choices[len(self.previous_choices) - 1]
        if n_chosen > 0:
            previous_choice = [faction for faction in last_choices if faction.is_chosen][0]
            previous_choice.is_chosen = False
            self.create_chosen_string()

            self.to_choose = last_choices
            self.previous_choices.pop()
            self.render_button_choices()
        else:
            print("Error: none chosen")

    def create_chosen_string(self):
        chosen_names = [faction.name for faction in self.factions if faction.is_chosen]
        self.chosen_string = f"{', '.join(chosen_names)}"
        text = f"Chosen: {self.chosen_string}".replace("_", " ")
        chosen_label = tk.Label(self.chosen_frame, name="chosen_string", text=text, wraplength=200)
        chosen_label.grid(row=6, column=0, padx=5)

    def on_enter(self, f, e):
        background_image = tk.PhotoImage(file=f.image)
        self.background_label.configure(image=background_image)
        self.background_label.photo = background_image
        self.background_label.pack()

    def on_leave(self, e):
        self.background_label.configure(image=None)
        self.background_label.photo = None
        self.background_label.pack()


win = tk.Tk()
App(win=win, n_choices=3)
win.mainloop()
