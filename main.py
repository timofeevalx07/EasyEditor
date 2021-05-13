from PyQt5.QtWidgets import *
import os
from PIL import Image, ImageFilter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt



class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir =  None
        self.filename =  None
        self.save_dir =  'Modified/'

    def load_image(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(self.dir,self.filename)
        self.image = Image.open(image_path)

    def show_image(self,path):
        image.hide()
        piximg = QPixmap(path)
        w,h = image.width(), image.height()
        piximg = piximg.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(piximg)
        image.show()


    def save_image(self):
        path =os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path)and os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)


    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)


    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)

    def do_sharpen(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)


    def do_blur(self):
        self.image = self.image.filter(ImageFilter.GaussianBlur)
        self.save_image()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.show_image(image_path)




app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle("Easy Editor")

folder_btn = QPushButton("Папка")
img_list = QListWidget()

image = QLabel('Картинка')
left_btn = QPushButton("Лево")
right_btn = QPushButton("Право")
mirror_btn = QPushButton("Зеркало")
sharp_btn = QPushButton("Резкость")
blur_btn = QPushButton("Размытие")
bw_btn = QPushButton("Ч/Б")


layout_1 = QVBoxLayout()
layout_1.addWidget(folder_btn)
layout_1.addWidget(img_list)


layout_2 = QHBoxLayout()
layout_2.addWidget(left_btn)
layout_2.addWidget(right_btn)
layout_2.addWidget(mirror_btn)
layout_2.addWidget(sharp_btn)
layout_2.addWidget(blur_btn)
layout_2.addWidget(bw_btn)


layout_3 = QVBoxLayout()
layout_3.addWidget(image)
layout_3.addLayout(layout_2)


layout_4 = QHBoxLayout()
layout_4.addLayout(layout_1, stretch=1)
layout_4.addLayout(layout_3, stretch=5)

main_win.setLayout(layout_4)



workdir = ''

def choose_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(filenames,extentions):
    result = []
    for fn in filenames:
        for ext in extentions:
            if fn.endswith(ext):
                result.append(fn)
    return result


def show_filenames_list():
    extentions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    choose_workdir()
    filenames = filter(os.listdir(workdir), extentions)
    img_list.clear()
    for fn in filenames:
        img_list.addItem(fn)

work_image = ImageProcessor()

def show_chosen_image():
    if img_list.currentRow() >= 0:
        filename = img_list.currentItem().text()
        work_image.load_image(workdir, filename)
        img_path = os.path.join(work_image.dir, work_image.filename)
        work_image.show_image(img_path)


img_list.currentRowChanged.connect(show_chosen_image)
folder_btn.clicked.connect(show_filenames_list)
bw_btn.clicked.connect(work_image.do_bw)
left_btn.clicked.connect(work_image.do_left)
right_btn.clicked.connect(work_image.do_right)
mirror_btn.clicked.connect(work_image.do_flip)
sharp_btn.clicked.connect(work_image.do_sharpen)
blur_btn.clicked.connect(work_image.do_blur)



main_win.showMaximized()
app.exec()