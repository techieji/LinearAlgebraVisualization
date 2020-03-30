from tkinter import *
from math import floor, sqrt, sin

class AlgebraicStructures:
    def __init__(self):
        pass
    def visualize(self):
        tk = Tk()
        graph = Canvas(tk, width=200, height=200)
        graph.pack()
        origin = [100, 100]
        if type(self) == Vector:
            assert(self.dimension == 2) # dimension can only be two
            graph.create_line(100, 0, 100, 200)
            graph.create_line(0, 100, 200, 100)
            scale = floor(90/max(self.coordinates))
            v = Vector.mul(self, scale)
            graph.create_line(100, 100, 100 + v.coordinates[0], 100 - v.coordinates[1], fill="red")
        if type(self) == Point:
            graph.create_line(100, 0, 100, 200)
            graph.create_line(0, 100, 200, 100)
            assert(self.dimension == 2)
            scale = floor(90/max(self.coordinates))
            p = Point.mul(self, scale)
            graph.create_oval(100 + p.coordinates[0], 100 - p.coordinates[1],  102 + p.coordinates[0], 102 - p.coordinates[1], fill="red")
        if (type(self) == Space) or (type(self) == Equation) or (type(self) == Function):
            assert(self.dimensions == 2)
            graph.create_line(100, 0, 100, 200)
            graph.create_line(0, 100, 200, 100)
            scale = 200 # an arbitrarily large value
            for x in self.graphobjs:
                try:
                    if floor(100/max([abs(x) for x in x.coordinates])) < scale:
                        scale = floor(100/max([abs(x) for x in x.coordinates]))
                except:
                    continue
            for x in self.graphobjs:
                v = Vector.mul(x, scale)
                if type(x) == Vector:
                    graph.create_line(100, 100, 100 + v.coordinates[0], 100 - v.coordinates[1], fill="red")
                elif type(x) == Point:
                    graph.create_oval(100 + v.coordinates[0], 100 - v.coordinates[1],  102 + v.coordinates[0], 102 - v.coordinates[1], fill="red")
        else:
            raise NotImplementedError 
        mainloop()

class Vector(AlgebraicStructures):
    def __init__(self, coordinates=[0, 0]):
        self.coordinates = coordinates
        self.dimension = len(coordinates)
        super().__init__()
    def add(v1, v2):
        assert(len(v1.coordinates) == len(v2.coordinates))
        vec = Vector([])
        for x in range(0, len(v1.coordinates)):
            vec.coordinates.append(v1.coordinates[x] + v2.coordinates[x])
        return vec
    def mul(v, scalar):
        vec = Vector([])
        for x in v.coordinates:
            vec.coordinates.append(x * scalar)
        return vec
    def transform(self, mat):
        return Matrix.vecmul(mat, self).elements[0]

class Matrix(AlgebraicStructures):
    def __init__(self, elements=[Vector(), Vector()]):
        self.elements = elements
        super().__init__()
    def add(m1, m2):
        assert(len(m1) == len(m2))
        mat = Matrix([])
        for x in range(0, len(m1)):
            mat.elements.append(Vector.add(m1[x], m2[x]))
        return mat
    def vecmul(m, v):
        mat = Matrix([])
        for x in range(0, len(v.coordinates)):
            mat.elements.append(Vector.mul(m.elements[x], v.coordinates[x]))
        return mat
    def mul(m1, m2):
        mat = Matrix([])
        for x in m1.elements:
            mat.elements.append(Matrix.vecmul(m2, x))
        return mat

class Point(Vector):
    def  __init__(self, coordinates1=[0, 0]):
        super().__init__(coordinates=coordinates1)

class Space(AlgebraicStructures):
    def __init__(self, axes=[Vector([1, 0]), Vector([0, 1])], dimensions=2):
        self.axes = axes
        self.dimensions = dimensions
        self.vectors = []
        self.points = []
        self.graphobjs = []
        super().__init__()
    def plotVector(self, vector):
        self.vectors.append(vector)
        self.graphobjs.append(vector)
    def plotPoint(self, point):
        self.points.append(point)
        self.graphobjs.append(point)
    def transform(self, mat):
        pass

class Equation(Space):
    def __init__(self, f, area=Vector([10, 10])):
        super().__init__()
        for x in range(-area.coordinates[0], area.coordinates[0]):
            for y in range(-area.coordinates[1], area.coordinates[1]):
                if f(x) == y:
                    self.plotPoint(Point([x, y]))

class Function(Equation):
    def __init__(self, f, amount=10):
        super().super().__init__()
        for x in range(-amount, amount):
            self.plotPoint(Point([x, f(x)]))

if __name__ == "__main__":
    s = Equation(lambda x: 2 * x + 3)
    s.visualize()
