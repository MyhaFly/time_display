from datetime import datetime
import os
import re
import sys
import time

sys.path.append(os.getcwd() + "/..")
sys.path.append(os.getcwd() + "/../..")

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, \
    QFrame
from data.form import Ui_MainWindow
from lmp.comconnector1c import ComConnector1C
from lmp.decorators import createLogger, try_exept_pyqt_dekorator, \
    logger_dekorator
from lmp.functions import fullDateToHHMMSS, secToHHMMwithText
from lmp.qlabeldraw import QLabelDraw
from utilitys.rowdict import rowDict
from utilitys.timer_display_confparser import ConstantsTimerDisplay


CONSTANTS = ConstantsTimerDisplay("../global_params.config")

log = createLogger()

class createBlocksRow(QMainWindow):
    """
    Класс создания строки блоков (блок заднего фона и поверх него блок с текстом)
    с применением стилизации
    """
    
    @try_exept_pyqt_dekorator(log, "createBlocksRow", "Ошибка при создании блоков") 
    def __init__(self, parent, rowName, params, bgAdresses, D_textStyle):
        
        self.skelet = CONSTANTS.T_nameSkelet
        self.coords = rowDict(params)
        self.coordsDict = {}
        
        QtGui.QFontDatabase.addApplicationFont("../data/font/Jovanny Lemonad - Bender-Bold.otf")
        QtGui.QFontDatabase.addApplicationFont("../data/font/Jovanny Lemonad - Bender-Black.otf")
        
        self.font = QFont('Bender', CONSTANTS.D_textFont, QFont.Bold)
        
        for colID in range(len(bgAdresses)):
            name = self.skelet % (rowName, colID)
            newBGBlock = self.createBackgroundBlock(parent, bgAdresses[colID])
            parent.ui.frame.__setattr__(name, newBGBlock)
            
            newTextBlock = self.createTextBlock(parent, D_textStyle[colID])
            parent.ui.frame.__setattr__(name + CONSTANTS.T_textMark, newTextBlock)
            
            self.coordsDict[name] = self.coords.getDict()

            self.coords.toNextBlock(newBGBlock.image.width(), newBGBlock.image.height())
        
        parent.coordsDict.update(self.coordsDict)
    
    @try_exept_pyqt_dekorator(log, "createBlocksRow", "Ошибка при создании фоновых блоков")
    def createBackgroundBlock(self, parent, bgImg):
        """
        Создаем блок в нужной позиции
        
        parent: класс родителя
        bgImg: адресс фона
        """
        new = QLabelDraw(parent.ui.frame)
        new.loadImgFromFile(bgImg)
        self.coords.setImgSize(new.image.width(), new.image.height() )
        new.setGeometry(self.coords.startX, 
                        self.coords.startY,
                        self.coords.sizeX,
                        self.coords.sizeY)
        new.displayImage()
        
        return new
    
    @try_exept_pyqt_dekorator(log, "createBlocksRow", "Ошибка при создании текстовых блоков")
    def createTextBlock(self, parent, D_textStyle):
        """
        Создаем блок в нужной позиции
        
        parent: класс родителя
        D_textStyle: стили для текста
        """
        new = QLabel(parent.ui.frame)
        new.setStyleSheet(D_textStyle)
        
        new.setFont(self.font)
        new.setGeometry(self.coords.startX, 
                self.coords.startY,
                self.coords.sizeX,
                self.coords.sizeY)
        new.setText("")
        
        return new



class MainForm(QMainWindow):

    @try_exept_pyqt_dekorator(log, "Main_form", "Запуск приложения")
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(CONSTANTS.D_pathToIcon))
        
        self.setGeometry(CONSTANTS.startX,
                         CONSTANTS.startY,
                         CONSTANTS.sizeW,
                         CONSTANTS.sizeH)
        self.timer_active = False
        self.orderTable = None
        self.coordsDict = {}
        self.rowCount = 0
        self.blockNow = 0
        
        self.comConnector = ComConnector1C(CONSTANTS.path1c, CONSTANTS.isServer1c)
        
        self.ui.bgLbl = QLabelDraw(self.ui.centralwidget)
        self.ui.bgLbl.setGeometry(0, 0,
                                  CONSTANTS.sizeW,
                                  CONSTANTS.sizeH)
        self.ui.bgLbl.loadImgFromFile(CONSTANTS.F_bgWindow)
        self.ui.bgLbl.displayImage()  
        
        self.createBlocks()
        self.createTitle()
        
        self.startTimer()
        
    #####################################
    # MARK: Update QDrawLabels
    #####################################
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при создании заголовков")
    def createTitle(self):
        """
        Создание блоков с текстом названий колонок
        """          
        font = QFont('Bender', CONSTANTS.D_titleFont, QFont.Bold)
        
        startY = CONSTANTS.N_startTitleY

        for colId in range(CONSTANTS.N_colCount):
            name = CONSTANTS.T_titleNameSkelet % colId
            cordsBlockName = CONSTANTS.T_nameSkelet % (0, colId)
            
            newTitle = QLabel(self.ui.centralwidget)
            newTitle.setFont(font)
            newTitle.setGeometry(
                self.coordsDict[cordsBlockName]['startX'], 
                startY,
                self.coordsDict[cordsBlockName]['sizeX'],
                self.coordsDict[cordsBlockName]['sizeY']
            )
            newTitle.setText(CONSTANTS.L_titleNames[colId])            
            self.ui.__setattr__(name, newTitle)

    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при создании блоков")
    def createBlocks(self):
        """
        Создание блоков относительно количества строк
        """
                
        self.ui.frame = QFrame(self.ui.centralwidget)
        self.ui.frame.setFrameShape(QFrame.StyledPanel)
        self.ui.frame.setFrameShadow(QFrame.Raised)
        self.ui.frame.setObjectName("frame")
        self.ui.horizontalLayout.addWidget(self.ui.frame)
        
        D_textStyle = CONSTANTS.D_textStyle
        
        if self.rowCount <= CONSTANTS.N_rowCount6:
            bgAdresses = CONSTANTS.F_bgAdress6
            rowCount = CONSTANTS.N_rowCount6
            margin = CONSTANTS.N_rowMargin6
        else:
            bgAdresses = CONSTANTS.F_bgAdress9
            rowCount = CONSTANTS.N_rowCount9
            margin = CONSTANTS.N_rowMargin9
        
        self.blockNow = rowCount  
        for rowId in range(rowCount):
            createBlocksRow(
                self, 
                rowId, 
                (CONSTANTS.N_startBlocksX,
                 CONSTANTS.N_startBlocksY + margin*rowId,
                 CONSTANTS.N_colMargin
                ), 
                bgAdresses, 
                D_textStyle)

        
    #####################################
    # MARK: Update data
    #####################################        
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при получении данных из 1с")
    def takeDataFrom1c(self):
        """
        Получение информации из 1с
        """
        orderTable = self.comConnector.takeOrderList(CONSTANTS.organ, CONSTANTS.object)
#         orderTable = from1c
        orderTable = self.comConnector.text1c2Table(orderTable, sort="Made")
        
        if orderTable is not None:
            orderTable.columns = ['number_plate', 'start', 'finish', 'timeleft']
            orderTable = orderTable[['number_plate', 'start', 'timeleft', 'finish']]
            orderTable = orderTable.sort_values(by="timeleft")
            
            orderTable.start = orderTable.start.apply(fullDateToHHMMSS)
            orderTable.finish = orderTable.finish.apply(fullDateToHHMMSS)
            
            self.orderTable = orderTable

    #####################################
    # MARK: Update blocks
    #####################################
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при определении необходимости перестраивать блоки")
    def needChangeBlocks(self, oldCount, newCount):
        """
        Изменилось ли количество для перерисовки блоков
        
        oldCount: Старое количество строк
        newCount: Новое количество строк
        """
        flag = False
        limit = CONSTANTS.N_rowCount6
        if ((newCount > limit and oldCount <= limit) or 
            (newCount <= limit and oldCount > limit)):
            flag = True
        return flag
    
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при удалении блоков")
    def removeBlocks(self):
        """
        Удаление блоков при смене количества
        """
        self.ui.frame.deleteLater()
        self.coordsDict = {}
    
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при подготовки таблицы")
    def prepareTable(self):
        """
        Подготовка таблицы к отображению
        
        table: таблица с текстом
        """
        table = self.orderTable.copy()
        table.timeleft = table.timeleft - 1
        table.loc[table.timeleft < 0, "timeleft"] = 0
        table.timeleft = table.timeleft
        
        self.orderTable = table.copy()
        
        table["timeleftText"] = table.timeleft.apply(secToHHMMwithText)
        return table
    
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при подготовки текста для строк")
    def prepareTextForRow(self, data):
        """
        Приводим текст в вид для отображения
        
        data: данные с текстом
        """
        numberPlate = data.number_plate.lower()
        numberPlate = re.sub(CONSTANTS.R_numberPlate, " ", numberPlate)
        return [numberPlate, data.start, data.timeleftText, data.finish]

    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при записи теста в блок")
    def setTextInBlock(self, rowId, colId, text):
        """
        Меняем текст в блоке
        
        rowId: В какой строке изменить данные
        colId: В каком столбце изменить данные
        text: текст
        """
        name = (CONSTANTS.T_nameSkelet % (rowId, colId)) + CONSTANTS.T_textMark
        block = self.ui.frame.__getattribute__(name)
        block.setText(str(text))
    
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при записи теста в блоки")   
    def setTextInBlocks(self, rowId, textForBlocks):
        """
        Меняем текст в блоках
        
        rowId: В какой строке изменять данные
        textForBlocks: данные с текстом
        """
        for colId, text in enumerate(textForBlocks):
            self.setTextInBlock(rowId, colId, text)
    
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при очищении блоков")      
    def clearEmptyBlocks(self, rowId):
        """
        Зачищаем блоки без информации
        
        rowId: С какой строки зачищать старый тест
        """     
        for _id in range(rowId, self.blockNow):
            for colId in range(CONSTANTS.N_colCount):
                self.setTextInBlock(rowId, colId, "")
    
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при изменении стиля блока")
    def setTextStyle(self, rowId, colId):
        """
        Задаем нужной ячейке подходящий стиль
        
        rowId: В каком строке изменить стиль
        colId: В каком столбце изменить стиль
        """    
        name = (CONSTANTS.T_nameSkelet % (rowId, colId)) + CONSTANTS.T_textMark
        block = self.ui.frame.__getattribute__(name)
        data = self.orderTable.iloc[rowId]
        
        if data.timeleft < CONSTANTS.N_midTime:
            block.setStyleSheet(CONSTANTS.D_bgGood)
        elif data.timeleft < CONSTANTS.N_goodTime:
            block.setStyleSheet(CONSTANTS.D_bgMid)
        else:
            block.setStyleSheet(CONSTANTS.D_bgBad)
    
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка при обновлении блоков")          
    def updateBlocks(self):
        """
        Обновление информации в блоках
        """
        if self.orderTable is not None:
            
            oldCount = self.rowCount

            self.rowCount = self.orderTable.shape[0]
            if self.needChangeBlocks(oldCount, self.rowCount):
                self.removeBlocks()
                self.createBlocks()
            
            table = self.prepareTable()
            
            for rowId, row in enumerate(table.iterrows()):
                
                if rowId > (self.rowCount - 1):
                    break
                
                data = row[1]
                textForBlocks = self.prepareTextForRow(data)
                self.setTextInBlocks(rowId, textForBlocks)
                self.setTextStyle(rowId, CONSTANTS.D_designedRow)
                
            last = rowId + 1
            if self.blockNow != last:
                self.clearEmptyBlocks(last)

    @logger_dekorator(log, "startTimer", "Запуск таймера.")
    @try_exept_pyqt_dekorator(log, "Main_form", "Ошибка запуске таймера")
    def startTimer(self, *args):
        """ 
        Запуск потока для постоянного обновления таблицы
        """
        self.takeDataFrom1c()
                
        self.timerUpdateTbl = QTimer(self)
        self.timerUpdateTbl.timeout.connect(self.takeDataFrom1c)
        self.timerUpdateTbl.start(CONSTANTS.N_update1cInterval)
        
        self.timerSec = QTimer(self)
        self.timerSec.timeout.connect(self.updateBlocks)
        self.timerSec.start(CONSTANTS.N_updateVizInterval)#60 * 
        

            
if __name__ == '__main__':
    log.info("Запуск приложения")
    app = QApplication(sys.argv)
    ex = MainForm()
    ex.show()
    exit(app.exec_())
