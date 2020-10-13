import random
import tkinter as tk


class App:
    def __init__(self, win, n_choices):
        self.win = win
        self.win.title("Terra Mystica Civ Chooser")
        self.win.geometry("400x400")
        tk.Label(self.win, text="Choose a Civ:").pack()

        self.chosen = []
        self.n_choices = n_choices
        self.button_list = []
        self.chosen_three = []
        self.previous_choices = []

        self.assign_picks()

        self.chosen_string = ""

        self.chosen_frame = tk.Frame(self.win)
        self.chosen_frame.pack(side="left")

        undo_frame = tk.Frame(self.win)
        undo_frame.pack(side="right")
        tk.Button(undo_frame, text="Undo Pick", command=self.undo).grid(row=6, column=5, padx=10)
        tk.Button(undo_frame, text="Refresh Choices", command=self.assign_picks).grid(row=7, column=5, pady=10, padx=5)

    def assign_picks(self, undo=False):
        colors = ["Yellow", "Yellow", "Brown", "Brown", "Black", "Black", "Blue", "Blue", "Grey", "Grey", "Red", "Red"]
        civs = ["Fakirs", "Nomads", "Halflings", "Cultists", "Darklings", "Alchemists", "Mermaids", "Swarmlings",
                "Engineers", "Dwarves", "Chaos Magicians", "Giants"]

        indices = [civs.index(civ) for civ in self.chosen]
        [indices.append(index + 1) for index in indices if index % 2 == 0]

        available_civs = [i for j, i in enumerate(civs) if j not in indices]
        available_colors = [i for j, i in enumerate(colors) if j not in indices]

        randomized = random.sample(range(0, len(available_civs)), len(available_civs))
        randomized_civs = [available_civs[i] for i in randomized]
        randomized_colors = [available_colors[i] for i in randomized]

        civ_dict = dict(zip(randomized_colors, randomized_civs))

        sample = random.sample(civ_dict.keys(), self.n_choices)

        self.chosen_three = [civ_dict[color] for color in sample]
        self.render_button_choices()

    def render_button_choices(self):
        button_frame = tk.Frame(self.win)
        button_frame.pack()

        for i in range(self.n_choices):
            self.button_list.append(
                tk.Button(button_frame, text=self.chosen_three[i], command=lambda c=i: self.command(c), width=14))
            self.button_list[i].config(text=self.chosen_three[i])
            self.button_list[i].grid(row=0, column=i, padx=10, pady=5)

    def command(self, c):
        if len(self.chosen) < 5:
            self.chosen.append(self.chosen_three[c])
            self.previous_choices.append(self.chosen_three)
            self.create_chosen_string()
            self.assign_picks()
        else:
            print("Error: cannot have more than 5 civs in a game.")

    def undo(self):
        if len(self.chosen) > 0:
            self.chosen.pop()
            self.create_chosen_string()

            self.chosen_three = self.previous_choices[len(self.previous_choices) - 1]
            self.previous_choices.pop()
            self.render_button_choices()
        else:
            print("Error: none chosen")

    def create_chosen_string(self):
        self.chosen_string = f"{', '.join(self.chosen)}"
        chosen_label = tk.Label(self.chosen_frame, name="chosen_string", text=f"Chosen: {self.chosen_string}", wraplength=300)
        chosen_label.grid(row=6, column=0, padx=5)


win = tk.Tk()
App(win=win, n_choices=3)
win.mainloop()
