import tkinter as tk
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot


class Figure3D:
    def __init__(self, filename):
        self.mesh = mesh.Mesh.from_file(filename)

    def show_figure(self):
        # Creating a plot
        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)

        # Load the STL file
        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.mesh.vectors))

        # Auto scale to the mesh size
        scale = self.mesh.points.flatten()
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        pyplot.show()

    def get_zero_slice(self):
        points = []
        for point in self.mesh.points:
            pass


class MainWindow(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.figure = Figure3D('example2.stl')

        button_show_figure = tk.Button(self, text='Show figure', bg='#d7d8e0', width=300, height=300,
                                       command=self.figure.show_figure)
        button_show_figure.pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title('SLICER')
    root.geometry('300x300')
    application = MainWindow(root)
    application.pack()
    root.mainloop()
