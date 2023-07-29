from z3 import *
from tkinter import Tk, Label, Button
import random

solver = Solver()

grid = [[Int("x_%s_%s" % (i, j)) for j in range(9)] for i in range(9)]



for i in range(9):
    for j in range(9):
        solver.add(grid[i][j] >= 1, grid[i][j] <= 9)
      
for i in range(9):
    solver.add(Distinct(grid[i]))

for j in range(9):
    solver.add(Distinct([grid[i][j] for i in range(9)]))

for r in range(0, 9, 3):
    for c in range(0, 9, 3):
        solver.add(Distinct([grid[i][j] for i in range(r, r + 3) for j in range(c, c + 3)]))

if solver.check() == sat:
  model = solver.model()
  grid_values = [[model.evaluate(grid[i][j]).as_long() for j in range(9)] for i in range(9)]


class SudokuGui:

  def __init__(self, master):

    self.master = master
    master.title("Sudoku Generator Owen Hushka")

    self.label = Label(master, text="Sudoku Generator")
    self.label.pack()

    self.greet_button = Button(master, text="Generate", command=self.greet)
    self.greet_button.pack()

    self.close_button = Button(master, text="Close", command=master.quit)
    self.close_button.pack()

  def greet(self):
    self.close_button.destroy()
    self.greet_button.destroy()
    self.label.destroy()
    global val
    for i in range(9):
      for j in range(9):
        val = grid_values[i][j]
        if ((i == 0 or i == 1 or i == 6 or i == 2 or i == 8 or i == 7)
            and (j == 0 or j == 1 or j == 2)):
          labell = Label(self.master,
                         width=2,
                         height=1,
                         bg="white",
                         relief="sunken",
                         borderwidth=1)
          labell.grid(row=i, column=j, padx=1, pady=1)
          labell.config(text=str(val))
          labell.place(width=cell_size,
                       height=cell_size,
                       x=j * cell_size,
                       y=i * cell_size)
        elif ((i == 3 or i == 4 or i == 5) and (j == 3 or j == 4 or j == 5)):
          labell = Label(self.master,
                         width=2,
                         height=1,
                         bg="white",
                         relief="sunken",
                         borderwidth=1)
          labell.grid(row=i, column=j, padx=1, pady=1)
          labell.config(text=str(val))
          labell.place(width=cell_size,
                       height=cell_size,
                       x=j * cell_size,
                       y=i * cell_size)

        elif ((j == 6 or j == 7 or j == 8) and ((i == 0 or i == 1 or i == 2) or
                                                (i == 6 or i == 7 or i == 8))):
          labell = Label(self.master,
                         width=2,
                         height=1,
                         bg="white",
                         relief="sunken",
                         borderwidth=1)
          labell.grid(row=i, column=j, padx=1, pady=1)
          labell.config(text=str(val))
          labell.place(width=cell_size,
                       height=cell_size,
                       x=j * cell_size,
                       y=i * cell_size)

        else:
          labell = Label(self.master,
                         width=2,
                         height=1,
                         bg="white",
                         relief="solid",
                         borderwidth=1)
          labell.config(text=str(val))
          labell.grid(row=i, column=j, padx=1, pady=1)
          labell.place(width=cell_size,
                       height=cell_size,
                       x=j * cell_size,
                       y=i * cell_size)


root = Tk()
cell_size = 30
root.geometry(f"{30*9+18}x{30*9+44}")
my_gui = SudokuGui(root)
root.mainloop()
