class rowDict():
    """
    Класс для удобного хранения данных строки блоков
    """
    def __init__(self, params, width=0, height=0):
        
        self.startX = params[0]
        self.startY = params[1]
        self.margin = params[2]
        self.setImgSize(width, height)
    
    def setImgSize(self, width, height):
        """
        Записываем размеры блока
        """
        self.sizeX = width
        self.sizeY = height
        
    def coordsForNext(self):
        """
        Перемещаем координату по X с учетом ширины блока и отступа
        """
        self.startX = self.startX + self.sizeX + self.margin
    
    def toNextBlock(self, width, height):
        """
        Перемещаем точку построения относительно блока с отступом
        """
        self.coordsForNext()
        self.setImgSize(width, height)
    
    def getDict(self):
        """
        Получаем данные в виде словаря
        """
        return {
            "startX": self.startX,
            "startY": self.startY,
            "margin": self.margin,
            "sizeX": self.sizeX,
            "sizeY": self.sizeY
            }
