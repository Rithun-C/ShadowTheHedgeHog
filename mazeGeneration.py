from mazelib.mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.transmute.Perturbation import Perturbation

m = Maze()
m.generator = Prims(5, 5)
m.generate()

m.transmuters = [Perturbation(repeat=1, new_walls=3)]
m.transmute()

print(m.grid)
