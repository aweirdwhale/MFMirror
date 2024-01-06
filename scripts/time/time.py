import time


class Clock:
    def __init__(self, label):
        self.label = label
        self.change_label()

    def change_label(self):
        current_time = time.strftime('%H\r%M')
        self.label.configure(text=current_time)
        win.after(60 * 1000, self.change_label)  # Met à jour toutes les secondes

