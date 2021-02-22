from PySide2 import QtWidgets
from PySide2.QtCore import Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from PySide2.QtGui import QImage, QPixmap
import os
import numpy as np 
from PIL import Image, ImageQt
from glob import glob
dir_name = os.path.dirname(os.path.abspath(__file__))


def update(func):
    def wrapper(cls):
        plt.axis("off")
        func(cls)
        cls.update()
        cls.canvas.draw()
    return wrapper


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(None)

        # buttons
        self.file_button = QtWidgets.QPushButton("select", parent=self)
        self.next_button = QtWidgets.QPushButton("next", parent=self)
        self.last_button = QtWidgets.QPushButton("last", parent=self)

        # show image
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.q_label = QtWidgets.QLabel(self)
        self.q_label.setScaledContents(True)

        self.next_slice_button = QtWidgets.QPushButton("next slice", parent=self)
        self.last_slice_button = QtWidgets.QPushButton('last slice', parent=self)

        self.slice_num = QtWidgets.QLabel(self)

        # layout 
        self.main_layout = QtWidgets.QVBoxLayout()
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_slices_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.file_button)
        self.button_layout.addWidget(self.last_button)
        self.button_layout.addWidget(self.next_button)
        self.button_slices_layout.addWidget(self.last_slice_button)
        self.button_slices_layout.addWidget(self.slice_num)
        self.button_slices_layout.addWidget(self.next_slice_button)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.canvas)
        self.main_layout.addLayout(self.button_slices_layout)

        self.setLayout(self.main_layout)
        self.init_signal()

    
    def init_signal(self):
        self.file_button.clicked.connect(self.show_file_dialog)

        self.next_slice_button.clicked.connect(self.next_slice)

        self.last_slice_button.clicked.connect(self.last_slice)

        self.next_button.clicked.connect(self.next_file)
        self.last_button.clicked.connect(self.last_file)

    @update
    @Slot()
    def show_file_dialog(self) -> None:
        result, _ = QtWidgets.QFileDialog.getOpenFileName(self, "choose a file", filter="Numpy array(*.npy)")
        self.file_dir = file_dir = os.path.dirname(result)
        print(os.listdir(file_dir))
        self.file_lists = [f for f in os.listdir(file_dir) if os.path.isfile(os.path.join(file_dir, f)) 
                and f.endswith(".npy")]
        print(self.file_lists)
        self.file_idx = self.file_lists.index(os.path.basename(result))

        self.slices: np.ndarray =  np.load(result).astype(np.float32)
        print(self.slices.shape, self.slices.dtype)
        self.slice_idx = 0
        self.slice_num.setText(f"{self.slice_idx}/{len(self.slices)}\tfile: {self.file_idx}/{len(self.file_lists)}")
        plt.imshow(self.slices[self.slice_idx], cmap="bone")
        plt.title(f"{self.file_lists[self.file_idx]}")
        
    @update
    @Slot()
    def next_slice(self) -> None:
        self.slice_idx = (self.slice_idx + 1)%len(self.slices)
        self.slice_num.setText(f"{self.slice_idx}/{len(self.slices)}\tfile: {self.file_idx}/{len(self.file_lists)}")
        plt.imshow(self.slices[self.slice_idx], cmap="bone")
        plt.title(f"{self.file_lists[self.file_idx]}")

    @update
    @Slot()
    def last_slice(self) -> None:
        self.slice_idx = (self.slice_idx - 1)%len(self.slices)
        self.slice_num.setText(f"{self.slice_idx}/{len(self.slices)}\tfile: {self.file_idx}/{len(self.file_lists)}")
        plt.imshow(self.slices[self.slice_idx], cmap="bone")
        plt.title(f"{self.file_lists[self.file_idx]}")

    @update
    @Slot()
    def next_file(self) -> None:
        self.file_idx = (self.file_idx + 1)%len(self.file_lists)
        self.slice_idx = 0
        self.slice_num.setText(f"{self.slice_idx}/{len(self.slices)}\tfile: {self.file_idx}/{len(self.file_lists)}")
        self.slices = np.load(self.file_dir + "/" + self.file_lists[self.file_idx]).astype(np.float32)
        plt.imshow(self.slices[self.slice_idx], cmap="bone")
        plt.title(f"{self.file_lists[self.file_idx]}")

    @update
    @Slot()
    def last_file(self) -> None:
        self.file_idx = (self.file_idx - 1)%len(self.file_lists)
        self.slice_idx = 0
        self.slice_num.setText(f"{self.slice_idx}/{len(self.slices)}\tfile: {self.file_idx}/{len(self.file_lists)}")
        self.slices = np.load(self.file_dir + "/" + self.file_lists[self.file_idx]).astype(np.float32)
        plt.imshow(self.slices[self.slice_idx], cmap="bone")
        plt.title(f"{self.file_lists[self.file_idx]}")
