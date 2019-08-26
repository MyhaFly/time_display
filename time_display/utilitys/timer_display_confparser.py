#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" 
Класс ConstantsTimerDisplay
"""

from lmp.configparser import Config
from lmp.decorators import try_exept_dekorator


class ConstantsTimerDisplay():
    """ 
    Спец. класс с константами
    """
    @try_exept_dekorator("ConstantsTimerDisplay", "Ошибка в инициализации.")
    def __init__(self, configPath):
        super().__init__()
        
        self.config = Config(configPath)
        self.config = self.config.readConfig()
        self.appendFromConfig()
        self.toNeedType()
        self.appendNumbers()
        self.appendTexts()
        self.appendSQLs()
        self.appendLists()
        self.appendDicts()
        self.appendFiles()
        self.apeendDesign()
    
    @try_exept_dekorator("ConstantsTimerDisplay", "Ошибка при чтении конфиг файла.") 
    def appendFromConfig(self):
        """
        Чтение конфиг файла
        """
        globalSection = 'global_info'
        self.organ = self.config.get(globalSection, 'organization')
        self.object = self.config.get(globalSection, 'object')
        
        self.scriptType = 'display_with_1c_connect'
        self.startX = self.config.get(self.scriptType, 'startX')
        self.startY = self.config.get(self.scriptType, 'startY')
        self.sizeW = self.config.get(self.scriptType, 'sizeW')
        self.sizeH = self.config.get(self.scriptType, 'sizeH')
        
        self.pathExe1c = self.config.get(self.scriptType, 'path_exe_1c')
        self.connectorName = self.config.get(self.scriptType, 'connector_name')
        self.typeConnect1c = self.config.get(self.scriptType, 'type_connect_1c')
        self.bd1c = self.config.get(self.scriptType, 'bd_1c')
        self.usr1c = self.config.get(self.scriptType, 'usr_1c')
        self.pas1c = self.config.get(self.scriptType, 'pas_1c')
            
        self.isServer1c = True if self.typeConnect1c == "server" else False
        if self.isServer1c:
            self.servIP1c = self.config.get(self.scriptType, 'serv_ip_1c')
            self.path1c = 'srvr="%s";ref=%s;usr=%s;pwd=%s;' % (
                self.servIP1c, self.bd1c, self.usr1c, self.pas1c
            )
        else:
            self.filePath1c = self.config.get(self.scriptType, 'file_path_1c')
            self.path1c = 'file="%s";ref=%s;usr=%s;pwd=%s;' % (
                self.filePath1c, self.bd1c, self.usr1c, self.pas1c
            )
            
                
    @try_exept_dekorator("ConstantsTimerDisplay", "Ошибка в приведении данных.")
    def toNeedType(self):
        """
        Приводим данные к требуемому виду
        """
        self.startX = int(self.startX)
        self.startY = int(self.startY)
        self.sizeW = int(self.sizeW)
        self.sizeH = int(self.sizeH)

    @try_exept_dekorator("ConstantsTimerDisplay", "Константные числа.")
    def appendNumbers(self):
        """
        Добавляем константные числа
        
        начинать с "N_"
        """
        
        self.N_secInterval = 1000
        self.N_update1cInterval = self.N_secInterval * 20
        self.N_updateVizInterval = self.N_secInterval# * 60
        
        self.N_badTime = 0
        self.N_midTime = 60 * 10
        self.N_goodTime = 60 * 60

        self.N_startTitleX = 120
        self.N_startTitleY = 187
                
        self.N_startBlocksX = 120
        self.N_startBlocksY = 270
        self.N_colMargin = 40
        
        self.N_colCount = 4
        
        self.N_rowCount6 = 6
        self.N_rowMargin6 = 115
        
        self.N_rowCount9 = 9
        self.N_rowMargin9 = 76
        
    
    @try_exept_dekorator("ConstantsTimerDisplay", "Константные тексты.")
    def appendTexts(self):
        """
        Добавляем константные тексты
        
        начинать с:
        "T_" - текст
        "R_" - регулярка
        
        """
        self.T_nameSkelet = "row%scol%sLbl"
        self.T_titleNameSkelet = "title%sLbl"
        self.T_textMark = "_text"
        
        self.R_numberPlate = r"(?<=[а-я|-])(?=[\d])|(?<=\d)(?=[а-я|-])|(?<=[а-я])(?=[-])"
        
        self.T_title0 = "Номер автомобиля"
        self.T_title1 = "Время старта"
        self.T_title2 = "Осталось времени"
        self.T_title3 = "Время окончания"
        
    
    @try_exept_dekorator("ConstantsTimerDisplay", "Константные SQL запросы.")
    def appendSQLs(self):
        """
        Добавляем константные запросы
        
        начинать с "SQL_"
        
        TN: TableName
        Table: Tbl
        ColumnName: ColN 
        
        SELECT: St
        CREATE: Ct
        CLEAN: Cn  
        UPDATE: Ut  
        DELETE: Dt #DROP    
        
        globalParams: GP
        """
        pass
    
    def appendLists(self):
        """
        Добавляем все, что со списками
        
        начинать с "L_"
        """
        
        self.L_titleNames = [self.T_title0, self.T_title1, self.T_title2, self.T_title3]
    
    def appendDicts(self):
        """
        Добавляем все, что со словарями
        
        начинать с "D_"
        """
        pass
    
    def appendFiles(self):
        """
        Добавляем все, что связано с дизайном
        
        начинать с "F_"
        """
        self.F_bgWindow = "../data/backgrounds/background.png"
        self.F_bgAdress6 = [
            "../data/backgrounds/red_block_6.png",
            "../data/backgrounds/gray_block_6_1.png",
            "../data/backgrounds/gray_block_6_2.png",
            "../data/backgrounds/gray_block_6_1.png"
            ]
        self.F_bgAdress9 = [
            "../data/backgrounds/red_block_9.png",
            "../data/backgrounds/gray_block_9_1.png",
            "../data/backgrounds/gray_block_9_2.png",
            "../data/backgrounds/gray_block_9_1.png"
            ]
        
    def apeendDesign(self):
        """
        Добавляем все, что связано с дизайном
        
        начинать с:
        D_: дизайн
        C_: цвета
        """
        self.C_green = "rgb(57, 181, 74)"
        self.C_orange = "rgb(247, 147, 30)"
        self.C_gray = "rgb(76, 73, 72)"
        self.C_darkRed = "rgb(140, 43, 40)"
        self.C_black = "rgb(57, 181, 74)"
        self.C_white = "rgb(255, 255, 255)"
        
        self.D_titleFont = 22
        self.D_textFont = 36
        self.D_pathToIcon = "../data/icon.ico"
        self.D_textPadding = "padding-left: 10;"
        self.D_textStyle = [
            "font-weight: 900; color: %s; %s;" % (self.C_white, self.D_textPadding),
            "color: %s; %s;" % (self.C_gray, self.D_textPadding),
            "color: %s; %s;" % (self.C_gray, self.D_textPadding),#(247, 147, 30)
            "color: %s; %s;" % (self.C_gray, self.D_textPadding)
            ]
        
        self.D_designedRow = 2          
        self.D_bgGood = "color: %s; %s" % (self.C_green, self.D_textPadding)
        self.D_bgMid = "color: %s; %s" % (self.C_orange, self.D_textPadding)
        self.D_bgBad = "color: %s; %s" % (self.C_darkRed, self.D_textPadding)

        