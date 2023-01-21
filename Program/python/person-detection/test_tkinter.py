import tkinter as tk
import random

# --- constants --- (UPPER_CASE_NAMES)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 200

DISTANCE = 20
NUMBER = (SCREEN_WIDTH // DISTANCE) + 1

# --- classes --- (CamelCaseNames)


class Graph(object):
    def __init__(self, canvas, data, *args, **kwargs):
        super().__init__()
        self.canvas = canvas
        self.data = data
        self.draw()

    def append(self, item, remove_first=True):
        if remove_first:
            self.data.pop(0)
        self.data.append(item)
        self.draw()

    def draw(self):
        # new distance if size changed
        self.distance = int(self.canvas.winfo_width()) / len(self.data) + 1

        # remove all lines
        self.canvas.delete("all")

        # draw new lines
        for x, (y1, y2) in enumerate(zip(self.data, self.data[1:])):
            x1 = x * self.distance
            x2 = (x + 1) * self.distance  # x1 + self.distance
            self.canvas.create_line([x1, y1, x2, y2])


class GraphCanvas(tk.Canvas):
    def __init__(self, master, data, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.data = data
        self.draw()

    def append(self, item, remove_first=True):
        if remove_first:
            self.data.pop(0)
        self.data.append(item)
        self.draw()

    def draw(self):
        # new distance if size changed
        self.distance = int(self.winfo_width()) / len(self.data) + 1

        # remove all lines
        self.delete("all")

        # draw new lines
        for x, (y1, y2) in enumerate(zip(self.data, self.data[1:])):
            x1 = x * self.distance
            x2 = (x + 1) * self.distance  # x1 + self.distance
            self.create_line([x1, y1, x2, y2])


# --- functions --- (lower_case_names)


def move():
    graph.append(random.randint(0, SCREEN_HEIGHT))
    graph_canvas.append(random.randint(0, SCREEN_HEIGHT))

    # run again after 100ms (0.1s)
    root.after(100, move)


# --- main --- (lower_case names)

# data at start
data = [random.randint(0, SCREEN_HEIGHT) for _ in range(NUMBER)]

print(data)

root = tk.Tk()

canvas = tk.Canvas(root, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="#ccffcc")
canvas.pack(fill="both", expand=True)

graph = Graph(canvas, data)

graph_canvas = GraphCanvas(
    root, data, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, bg="#ffcccc"
)
graph_canvas.pack(fill="both", expand=True)

# start animation
move()

root.mainloop()
