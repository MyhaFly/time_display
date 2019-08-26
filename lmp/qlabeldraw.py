#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" 
Класс QLabelDraw
"""

from PyQt5 import QtWidgets, QtCore
from PyQt5.Qt import QTextOption
from PyQt5.QtCore import Qt, QRect, QRectF, QSize, QPoint
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap, QFont
from PyQt5.QtWidgets import QLabel, QFrame

from lmp.decorators import try_exept_dekorator


# TODO: Добавить отрисовку фигуры, понадобится для определения заняты ли парковочные места
# TODO: Красить разные типы групп в разные цвета
# TODO: Обновлять разрешение картинки при запуске видео и изменении окна
class QLabelDraw(QLabel):
    """ 
    Виджет для вывода изображений.
    Возможности:
        Добавление зон с помощью мыши
        удаление
    draw:
    Возможность рисовать квадраты на картинке
    
    label:
    0: не подписывать
    1: номер
    2: текст
    """
    @try_exept_dekorator("QLabelDraw", "Ошибка в инициализации.")   
    def __init__(self, parent=None, draw=False, label=-1):
        super().__init__(parent=parent)
        
        self.image = None
        self.rect = [] # [Номер, Имя, X, Y, W, H]
        self.draw = draw
        self.label = label
        self.dispSize = 0
        
        self.begin = None
        self.end = None
        
        self.wscaled = 0
        self.hscaled = 0
        
        #self.setFrameShape(QFrame.Box)
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        #self.rect = []
    
    @try_exept_dekorator("QLabelDraw", "Ошибка в отчистке изображения.")
    def clearImage(self):
        self.image = None
        self.rect = []
        self.clear()
        
    @try_exept_dekorator("QLabelDraw", "Ошибка в установки точки старта.")
    def setBegin(self, x, y):
        """ 
        Установка точки начала старта
        """
        self.begin = QPoint(x, y)
    
    @try_exept_dekorator("QLabelDraw", "Ошибка в установки точки конца.")
    def setEnd(self, x, y):
        """ 
        Установка точки начала конца
        """
        self.end = QPoint(x, y)
    
    @try_exept_dekorator("QLabelDraw", "Ошибка в загрузке файла.")
    def loadImgFromFile(self, file):
        """ 
        Загрузка изображения из файла
        """
        self.image = QPixmap(file)
    
    @try_exept_dekorator("QLabelDraw", "Ошибка в отрисовке.")       
    def paintEvent(self, event):
        """ 
        Стандартное событие отрисовки
        """
        super().paintEvent(event)
        if len(self.rect) != 0:
            width = self.image.width() / self.wscaled
            height = self.image.height() / self.hscaled
            for _line in self.rect:
                _list = [(_line[2] - _line[4] / 2) * width,
                        (_line[3] - _line[5] / 2) * height,
                        _line[4] * width,
                        _line[5] * height]
                
                if self.label == -1:
                    self.drawRectF(_list)
                else:
                    self.drawRectF(_list, str(_line[self.label]))
            
        # Отрисоваваем зону от нажатия мышки
        if self.draw:
            if self.end:
                self.drawRect(QRect(self.begin, self.end))

    @try_exept_dekorator("QLabelDraw", "Ошибка в отрисовке квадрата.")
    def drawRectF(self, _list, text = None):
        """ 
        _list -> left, top, width, height
        Рисование квадрата по 4 параметрам
        
        text - надпись над квадратом
        """
        q = QPainter(self)
        q.setPen(QPen(Qt.green, 2, Qt.SolidLine))
        rect = QRectF(int(_list[0]), int(_list[1]), int(_list[2]), int(_list[3]))
        q.drawRect(rect)
        if text is not None:
            q.setPen(QPen(Qt.red))
            q.setFont(QFont("times", 14))
            q.drawText(rect, str(text))
    
    @try_exept_dekorator("QLabelDraw", "Ошибка в отрисовке изображения.")
    def displayImage(self, image=None, size=0):
        """ 
        Отрисовываем изображение
        
        size
        0: Размер по экрану
        1: Оригинальный размер
        2: Увеличить в 4 раза
        3: Растянуть по экрану сохраняя пропорции
        """
        self.dispSize = size
        if image is not None:
            self.image = image
            
        if size == 1:
            qsize = QSize(self.image.width(), self.image.height())
            img = self.image.scaled(qsize)
            
        elif size == 2:
            qsize = QSize(self.image.width()*4, self.image.height()*4)
            img = self.image.scaled(qsize)
            
        elif size == 3:
            qsize = self.size()
            img = self.image.scaledToHeight(qsize.height())
            if qsize.width()/qsize.height() < self.image.width()/self.image.height():
                img = img.scaledToWidth(qsize.width())
            qsize = img.size()
        else:
            qsize = self.size()
            img = self.image.scaled(qsize)
        
        self.wscaled = self.image.width() / img.width()
        self.hscaled = self.image.height() / img.height()
        self.setMaximumSize(qsize)
        self.setPixmap(img)
        self.resize(qsize)
    
    @try_exept_dekorator("QLabelDraw", "Ошибка при получении отображенного изображения.")
    def takeImgWH(self):
        return [self.width(), self.height()]
        
    @try_exept_dekorator("QLabelDraw", "Ошибка при получении уникальных регионов для добавления в форму.")
    def frame2Img(self, frame):
        """ 
        frame -> image
        Переводим кадр с камеры в изображение для отрисовки
        """
        if frame is not None:
            qformat = QImage.Format_Indexed8
            if len(frame.shape)==3 :
                if frame.shape[2]==4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888  
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], qformat)
            image = image.rgbSwapped()
            image = QPixmap(image)
            self.image = image

    #@try_exept_dekorator("QLabelDraw", "Ошибка в момент нажатии кнопки мыши.")
    def mousePressEvent(self, event):
        """ 
        Измененная стандартная функция
        self.begin и self.end отслеживаем выделенную зону 
        """
        
        self.begin = event.pos()
        self.end = event.pos()
    
        self.update()

    #@try_exept_dekorator("QLabelDraw", "Ошибка в момент отпускания кнопки мыши.")
    def mouseMoveEvent(self, event):
        """ 
        Измененная стандартная функция
        Отслеживаем отпускания кнопки мыши
        """
        self.end = event.pos()
        self.update()
    
    @try_exept_dekorator("QSliderMove", "Ошибка в изменении шага.") 
    def drawRect(self, qrect):#, text = None
        """ 
        Рисуем квадрат по 4 полученым координатам
        
        qrect <=> X и Y левого верхнего и X и Y нижнего правого
        
                
        text - надпись над квадратом
        """
        q = QPainter(self)
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        q.setPen(pen)
        q.drawRect(qrect)
#         if text is not None:
#             q.setPen(QPen(Qt.red))
#             q.setFont(QFont("times", 14))
#             q.drawText(qrect, str(text))

    @try_exept_dekorator("QLabelDraw", "Ошибка в добавлении зоны.")
    def addRect(self, _id = None, name = None):
        """ 
        Добавляем зону в данные
        _id - номер для зоны либо задается, либо берется максимальный + 1
        name - название зоны, либо _id
        """
        if self.begin is not None:
            if _id is None:
                _id = len(self.rect) + 1
            if name is None:
                name = str(_id)
            zone = [_id, name] + self.ltrb2xywh()
            self.rect.append(zone)
            self.update()
    
    @try_exept_dekorator("QLabelDraw", "Ошибка в добавлении зоны предоставленную пользователем.")
    def addUserRect(self, zone):
        """ 
        Добавляем зону предоставленную пользователем в данные
        """
        self.rect.append(zone)
        self.update()
    
    @try_exept_dekorator("QLabelDraw", "Ошибка в получении последней зоны.")
    def getLastRect(self):
        return self.rect[len(self.rect) - 1]
    
    @try_exept_dekorator("QLabelDraw", "Ошибка удалении зоны.") 
    def delRect(self, num):
        """ 
        Удаляем зону из данных
        """
        self.rect.pop(num)
        self.update()
        
    @try_exept_dekorator("QLabelDraw", "Ошибка в конвертации.")
    def ltrb2xywh(self, wImg=None, hImg=None):
        """ 
        Конвертируем (1) в (2) используя ширину и высоту,
        так как изначально данные нормируются
        
        1 = (X и Y левого верхнего и X и Y нижнего правого)
        2 = (X и Y центра зоны и ширина и высота)
        """
        if wImg is None:
            wImg=self.width()#self.wscaled
        if hImg is None:
            hImg=self.height()#self.hscaled
        x1=self.begin.x()
        x2=self.end.x()
        y1=self.begin.y()
        y2=self.end.y()
        # Делаем подходящие координаты с учетом границы картинки
        if x2 < x1:
            x2 = x2 + x1
            x1 = x2 - x1
            x2 = x2 - x1
        if y2 < y1:
            y2 = y2 + y1
            y1 = y2 - y1
            y2 = y2 - y1
        # Обрезание лишнего
        if x1 < 0:
            x1 = 0
        if x2 > wImg:
            x2 = wImg
        if y1 < 0:
            y1 = 0
        if y2 > hImg:
            y2 = hImg
        width = round((x2 - x1) / wImg, 5)
        x = round((width * wImg/ 2 + x1) / wImg, 5)
        height = round((y2 - y1) / hImg, 5)
        y = round((height * hImg/ 2 + y1) / hImg, 5)
        # width = (x2 - x1) / wImg
        # x = (width * wImg / 2 + x1) / wImg
        # height = (y2 - y1) / hImg
        # y = (height * hImg / 2 + y1) / hImg
        return [x, y, width, height]
    
    def resizeImage(self, width, height):
        # Изменение размера до нужного
        self.image = self.image.scaled(width, height) #self.width(), self.height()
    
    
