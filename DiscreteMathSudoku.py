from z3 import *
from tkinter import Tk, Label, Button
from random import randint

solver = Solver() #declare a z3 solver
numSolutions = 0
multipleSolutionsPossible = False
sudokuDeletedElements = []
sudokuFull = []
for i in range(9):
  row = []
  for j in range(9):
    row.append(0)
  sudokuFull.append(row)
  #I want an array which I can store the solution to the sudoku in 
  #I initialize it to be a 9x9 array of 0s



#method which adds the constraints of a sudoku

#several of these constraints were taken from Z3 API in Python:
#“Z3 API in Python.” Z3Py Guide, https://ericpony.github.io/z3py-tutorial/guide-examples.htm. 
def addSudokuConstraints(): 
  for i in range(9):
    for j in range(9):
      solver.add(sudoku[i][j] >= 1, sudoku[i][j] <= 9)
  
  for i in range(9):
    solver.add(Distinct(sudoku[i]))
  
  for j in range(9):
    solver.add(Distinct([sudoku[i][j] for i in range(9)]))
  
  for r in range(0, 9, 3):
    for c in range(0, 9, 3):
      solver.add(Distinct([sudoku[i][j] for i in range(r, r + 3) for j in range(c, c + 3)]))


#a function which generates 2 random values between 0 and 8
#which are used to decide which row and column number the 
#square in the sudoku which is about to be deleted should have
def generate_2_values():
  val1 = randint(0, 8)
  val2 = randint(0, 8)
  return val1, val2
  

sudoku = [[Int("x_%s_%s" % (i, j)) for j in range(9)] for i in range(9)]


#variable I used to adjust the difficulty of the sudoku puzzle
#I added a constraint to both of the while loops (and iterator > x)
#by varying x I could vary how many zeros are added to the sudoku and 
#thus how difficult the puzzle was to solve
iterator = 0

#These while loops are used to add zeros to the solved sudoku puzzle
#I run this while loop until there become more than one solution possible 
#to solve the sudoku 
while numSolutions < 2:
  numSolutions = 0
  solver.reset() #I reset the constraints because on line 95 below
  #I run: solver.add(sudoku[i][j] == sudoku_values[i][j]) if sudoku_values[i][j] is not zero
  #and this will change
  addSudokuConstraints() #add the basic constraints
  while solver.check() == sat:
    iterator = iterator + 1  #another zero is going to be added
    numSolutions = numSolutions + 1 #there is another solution
    model = solver.model()
    sudoku_values = [[model.evaluate(sudoku[i][j]).as_long() for j in range(9)]for i in range(9)]
    sudokuFull = sudoku_values
    
    #This line of code was taken from the article cited below: 
    #Bjørner, Nikolaj, et al. Programming Z3 - Stanford University . Stanford University, https://theory.stanford.edu/~nikolaj/programmingz3.html. 
    solver.add(Or([f() != model[f] for f in model.decls() if f.arity() == 0]))  

    #I added my own line to block the solution
    #This is because I did not quite understand how the method on line 75 works
    solver.add(Or(sudoku != sudoku_values))
    

    v1,v2 = generate_2_values()
    threeValues = sudoku_values[v1][v2],v1,v2
    sudokuDeletedElements.append(threeValues)
    #I add the element which was deleted as well as the column and row number to this
    #array so that I can add back zeros in case the sudoku becomes solvable multiple 
    #different ways
    for i in range(len(sudokuDeletedElements) + 1):
      sudoku_values[sudokuDeletedElements[i-1][1]][sudokuDeletedElements[i-1][2]] = 0


    for i in range(9):
     for j in range(9):
      if sudoku_values[i][j] != 0:
       solver.add(sudoku[i][j] == sudoku_values[i][j])

        #I set the constraints to be such that the sudoku is partially 
        #solved. This is to make sure that there are not more than one 
        #possible solutions
        

#if there become multiple possible solutions, I undo the 
#last zero which was added which caused this issue
if multipleSolutionsPossible:
  sudoku_values[threeValues[1]][threeValues[2]] = threeValues[0]



#a GUI I generated which displays a sudoku board 
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
        if sudoku_values[i][j] == 0:
          if ((i == 0 or i == 1 or i == 6 or i == 2 or i == 8 or i == 7) and (j == 0 or j == 1 or j == 2)):
            labell = Label(self.master,width=2,height=1,bg="white",relief="sunken",borderwidth=1)
            labell.grid(row=i, column=j, padx=1, pady=1)

            labell.place(width=cell_size,height=cell_size,x=j * cell_size,y=i * cell_size)
          elif ((i == 3 or i == 4 or i == 5) and (j == 3 or j == 4 or j == 5)):
            labell = Label(self.master,width=2,height=1,bg="white",relief="sunken",borderwidth=1)
            labell.grid(row=i, column=j, padx=1, pady=1)

            labell.place(width=cell_size,height=cell_size,x=j * cell_size,y=i * cell_size)

          elif ((j == 6 or j == 7 or j == 8)
                and ((i == 0 or i == 1 or i == 2) or
                     (i == 6 or i == 7 or i == 8))):
            labell = Label(self.master,width=2,height=1,bg="white",relief="sunken",borderwidth=1)
            labell.grid(row=i, column=j, padx=1, pady=1)

            labell.place(width=cell_size,height=cell_size,x=j * cell_size,y=i * cell_size)

          else:
            labell = Label(self.master,width=2,height=1,bg="white",relief="solid",borderwidth=1)

            labell.grid(row=i, column=j, padx=1, pady=1)
            labell.place(width=cell_size,height=cell_size,x=j * cell_size,y=i * cell_size)
        else:
          val = sudoku_values[i][j]
          if ((i == 0 or i == 1 or i == 6 or i == 2 or i == 8 or i == 7)
              and (j == 0 or j == 1 or j == 2)):
            labell = Label(self.master,width=2,height=1,bg="white",relief="sunken",borderwidth=1)
            labell.grid(row=i, column=j, padx=1, pady=1)
            labell.config(text=str(val))
            labell.place(width=cell_size,height=cell_size,x=j * cell_size,y=i * cell_size)
          elif ((i == 3 or i == 4 or i == 5) and (j == 3 or j == 4 or j == 5)):
            labell = Label(self.master,width=2,height=1,bg="white",relief="sunken",borderwidth=1)
            labell.grid(row=i, column=j, padx=1, pady=1)
            labell.config(text=str(val))
            labell.place(width=cell_size,height=cell_size,x=j * cell_size,y=i * cell_size)

          elif ((j == 6 or j == 7 or j == 8)
                and ((i == 0 or i == 1 or i == 2) or
                     (i == 6 or i == 7 or i == 8))):
            labell = Label(self.master,width=2,height=1,bg="white",relief="sunken",borderwidth=1)
            labell.grid(row=i, column=j, padx=1, pady=1)
            labell.config(text=str(val))
            labell.place(width=cell_size,height=cell_size,x=j * cell_size,y=i * cell_size)

          else:
            labell = Label(self.master,width=2,height=1,bg="white",relief="solid",borderwidth=1)
            labell.config(text=str(val))
            labell.grid(row=i, column=j, padx=1, pady=1)
            labell.place(width=cell_size,height=cell_size,x=j * cell_size,y=i * cell_size)


root = Tk()
cell_size = 30
root.geometry(f"{30*9+18}x{30*9+44}")
my_gui = SudokuGui(root)
root.mainloop()
