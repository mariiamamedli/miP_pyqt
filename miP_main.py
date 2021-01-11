"""
Растровый графический редактор. Аналог Paint'а.
Необходимо реализовать простые функции построения геометрических фигур,
копирования области, ластика, сохранения и загрузки изображений.
В базе данных ведется лог действий пользователя.
"""

# импорты
import sys

from PIL import Image
from PyQt5 import uic

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage, QPainter, QPen, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog, QWidget, QInputDialog, QFileDialog


# константы (чтобы не ошибаться)
brush = 'brush'
eraser = 'eraser'
line = 'line'
rect = 'rect'
oval = 'oval'


class miP_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('miP_main.ui', self)  # Загружаем дизайн (надо не забыть в файл переделать)

        # Создаем холст
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False

        # Сразу же выбираем кисть
        self.draw_type = brush
        self.draw_size = 8
        self.draw_color1 = Qt.black
        self.draw_color2 = Qt.white

        self.lastPoint = QPoint()
        self.x = 0
        self.y = 0

        # меню файла
        self.f_create.triggered.connect(self.create_new_file)
        self.f_open.triggered.connect(self.open_file)
        self.f_save.triggered.connect(self.save_file)

        # инструменты
        self.i_brush.dtype = brush
        self.i_brush.triggered.connect(self.choose_draw_type)

        self.i_eraser.dtype = eraser
        self.i_eraser.triggered.connect(self.choose_draw_type)

        self.i_line.dtype = line
        self.i_line.triggered.connect(self.choose_draw_type)

        self.i_rect.dtype = rect
        self.i_rect.triggered.connect(self.choose_draw_type)

        self.i_oval.dtype = oval
        self.i_oval.triggered.connect(self.choose_draw_type)

        # цвет 1 (pen)
        self.c1_black.color = Qt.black
        self.c1_black.triggered.connect(self.choose_color1)
        self.c1_red.color = Qt.red
        self.c1_red.triggered.connect(self.choose_color1)
        self.c1_blue.color = Qt.blue
        self.c1_blue.triggered.connect(self.choose_color1)
        self.c1_yellow.color = Qt.yellow
        self.c1_yellow.triggered.connect(self.choose_color1)
        self.c1_green.color = Qt.green
        self.c1_green.triggered.connect(self.choose_color1)
        self.c1_white.color = Qt.white
        self.c1_white.triggered.connect(self.choose_color1)
        self.c1_other.triggered.connect(self.choose_color1)

        # цвет 2 (brush)
        self.c2_black.color = Qt.black
        self.c2_black.triggered.connect(self.choose_color2)
        self.c2_red.color = Qt.red
        self.c2_red.triggered.connect(self.choose_color2)
        self.c2_blue.color = Qt.blue
        self.c2_blue.triggered.connect(self.choose_color2)
        self.c2_yellow.color = Qt.yellow
        self.c2_yellow.triggered.connect(self.choose_color2)
        self.c2_green.color = Qt.green
        self.c2_green.triggered.connect(self.choose_color2)
        self.c2_white.color = Qt.white
        self.c2_white.triggered.connect(self.choose_color2)
        self.c2_other.triggered.connect(self.choose_color2)

        # выбор размера (толщины) инструмента
        self.c_size.triggered.connect(self.choose_size)

    def create_new_file(self):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(self.draw_color2)
        self.update()

    def save_file(self):
        fname = QFileDialog.getSaveFileName(
            self, 'Сохранить картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        self.image.save(fname)

    def open_file(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);;Все файлы (*)')[0]
        im = Image.open(fname)
        im = im.resize((800, 600))
        im.save('res.png')
        self.image.load('res.png')

    def choose_size(self):
        size, ok_pressed = QInputDialog.getInt(
            self, "Введите размер кисти", "Размер кисти",
            self.draw_size, 1, 1000, 1)
        if ok_pressed:
            self.draw_size = size

    def choose_color1(self):  # палитра, все обычно
        if self.sender() != self.c1_other:
            self.draw_color1 = self.sender().color
        else:
            self.draw_color1 = QColorDialog.getColor()

    def choose_color2(self):  # палитра, все обычно
        if self.sender() != self.c2_other:
            self.draw_color2 = self.sender().color
        else:
            self.draw_color2 = QColorDialog.getColor()

    def choose_draw_type(self):
        self.draw_type = self.sender().dtype

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            self.x = event.x()
            self.y = event.y()
            self.image.save('res.png')

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            if self.draw_type == brush:
                painter = QPainter(self.image)
                painter.setPen(QPen(self.draw_color1, self.draw_size))
                painter.drawLine(self.lastPoint, event.pos())
                self.lastPoint = event.pos()

            if self.draw_type == eraser:
                painter = QPainter(self.image)
                painter.setPen(QPen(self.draw_color2, self.draw_size))
                painter.drawLine(self.lastPoint, event.pos())
                self.lastPoint = event.pos()

            elif self.draw_type == line:
                self.image.load('res.png')
                painter = QPainter(self.image)
                painter.setPen(QPen(self.draw_color1, self.draw_size))
                painter.drawLine(self.lastPoint, event.pos())

            elif self.draw_type == rect:
                self.image.load('res.png')
                painter = QPainter(self.image)
                painter.setPen(QPen(self.draw_color1, self.draw_size))
                painter.setBrush(QBrush(self.draw_color2))
                painter.drawRect(self.x, self.y, event.x() - self.x, event.y() - self.y)

            elif self.draw_type == oval:
                self.image.load('res.png')
                painter = QPainter(self.image)
                painter.setPen(QPen(self.draw_color1, self.draw_size))
                painter.setBrush(QBrush(self.draw_color2))
                painter.drawEllipse(self.x, self.y, event.x() - self.x, event.y() - self.y)

            self.update()

    def mouseReleaseEvent(self, event):
        self.drawing = False
        self.image.save('res.png', 'png')

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

# запуск приложения

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = miP_MainWindow()
    ex.show()
    sys.exit(app.exec())
