# Slicer

Slicer created to help slice .stl models to images of layers

### How to use

1. Input filename, step and dpi in application window
2. You can show stl 3D model using 'Show' button
3. Press 'Slice !' to slice stl model - images will appear in pict/ dir

### Tech

Slicer uses a number of libs to work properly:

* Matplotlib
* Stl lib
* Tkinter
* Numpy

### Installation

Slicer requires python 3+ and some libs to be installed

```sh
$ python pip install numpy
$ python pip install stl
$ python pip install matplotlib
```

### Launching Slicer App
```sh
$ python slicer.py
```