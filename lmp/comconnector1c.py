import json
import re

from win32com import client

from lmp.decorators import try_exept_dekorator
from lmp.exeptions import programExeption
import pandas as pd


class ComConnector1C():
    """ 
    Работа с 1с
    """
    @try_exept_dekorator("ComConnector1C", "Ошибка в инициализации.")
    def __init__(self, path_1C, isServer):
        super().__init__()
        
        self.path_1C = path_1C
        self.isServer = isServer

    @try_exept_dekorator("ComConnector1C", "Ошибка в подключении.")
    def connect(self):
        return client.Dispatch("V82.ComConnector").connect(self.path_1C)
    
    #@try_exept_dekorator("ComConnector1C", "Ошибка при записи вектора в 1с.")
    def setVectorTo1C(self, id_1c, vector):
        """
        Отправка вектора (антропометрические точки лица) в 1с
        """
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.Picture_Memorise_srv(id_1c, vector)
            else:
                out = V82.Picture_Memorise(id_1c, vector)
        except:
            raise programExeption("critical", "Ошибка при получение списка пользователей из 1с.")
        return out
    
    def timeOfLastVectorUpdate(self):
        """
        Получить время последнего обновления в таблице портретов сотрудников
        """
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.LastPortraitDate_srv()
            else:
                out = V82.LastPortraitDate()
        except:
            raise programExeption("critical", "Ошибка при получение времени добавления вектора в 1с.")
        return out
    
    #@try_exept_dekorator("ComConnector1C", "Ошибка при получение списка пользователей из 1с.")
    def takeUserList(self, organ, region, mod = 1):
        """
        Получить список сотрудников с портретами
        organ: организация из 1с
        region: Регион по которому фильтруется. Текст (Нр: Казань)
        "" - по всем регионам
        mod:
        0 - Все
        1 - Только активные сотрудники
        """
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.GetUsersPortraitList_srv(organ, region, mod)
            else:
                out = V82.GetUsersPortraitList(organ, region, mod)
        except:
            raise programExeption("critical", "Ошибка при получение списка пользователей из 1с.")
        return out
    
    def takeUserStatus(self, id_1c, obj, organ):
        """
        Получить статус сотрудника
        id_1c: айди сотрудника из 1с
        obj: подразделение из 1с (AAA)
        organ: организация из 1с
        """
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.GetWorkerLastStatus_srv(id_1c, obj, organ)
            else:
                out = V82.GetWorkerLastStatus(id_1c, obj, organ)
        except:
            raise programExeption("critical", "Ошибка при получении статуса сотрудника.")
        return out
        
    #@try_exept_dekorator("ComConnector1C", "Ошибка при получение списка регионов из 1с.")
    def takeRegionList(self, organ):
        """
        Получить все регионы по организации
        organ: организация из 1с
        """
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.GetRegionList_srv(organ)
            else:
                out = V82.GetRegionList(organ)
        except:
            raise programExeption("critical", "Ошибка при получении списка регионов из 1с.")
        return out
    
    #@try_exept_dekorator("ComConnector1C", "Ошибка при получение актуального списка нарядов.")
    def takeOrderList(self, job, obj):
        """
        Получить список нарядов. Внетри
        Автомобильный номер, старт, между, конец.
        
        job: организация из 1с
        obj: подразделение из 1с (AAA)
        """
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.GetTimeCars_srv(job, obj)
            else:
                out = V82.GetTimeCars(job, obj)
        except:
            raise programExeption("critical", "Ошибка при получение списка пользователей из 1с.")
        return out 
       
    #@try_exept_dekorator("ComConnector1C", "Ошибка при записи прихода сотрудника в 1c.")
    def userComeIn(self, id_1c, obj, organ):
        """
        Отметить приход сотрудника
        id_1c: айди сотрудника из 1с
        obj: подразделение из 1с (AAA)
        organ: организация из 1с
        """
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.Worker_Come_In_srv(id_1c, obj, organ)
            else:
                out = V82.Worker_Come_In(id_1c, obj, organ)
        except:
            raise programExeption("critical", "Ошибка при записи прихода в 1с.")
        return out

    #@try_exept_dekorator("ComConnector1C", "Ошибка при записи ухода сотрудника в 1c.")
    def userComeOut(self, id_1c, obj, organ):
        """
        Отметить уход сотрудника
        id_1c: айди сотрудника из 1с
        obj: подразделение из 1с (AAA)
        organ: организация из 1с
        """
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.Worker_Come_Out_srv(id_1c, obj, organ)
            else:
                out = V82.Worker_Come_Out(id_1c, obj, organ)
        except:
            raise programExeption("critical", "Ошибка при записи ухода в 1с.")
        return out

    @try_exept_dekorator("ComConnector1C", "Ошибка переводе ФИО в нормальный вид.")
    def fioToNormal(self, text):
        """
        Удаляем в поле FIO все лишние символы
        text: текст в котором удаляются лишние символы
        """
        text = text.replace("\r", "")
        text = text.split("\n")
        for i, row in enumerate(text):
            if re.match('"FIO"', row):
                new = row[7:-2].replace('"', "")
                new = new.replace('\\', "")
                new = '"FIO":"' + new + '",'
                text[i] = new
        text = "\n".join(text)
        return text
    
    @try_exept_dekorator("ComConnector1C", "Ошибка в конвертации данных из 1с в таблицу.")
    def text1c2Table(self, text, sort = None):
        """
        Переводим текст из 1с в таблицу pandas
        text: текст, который станет jsonом
        sort: Имя колонки по которой нужно отсортировать
        """
        try:
#             text = self.fioToNormal(text)
            table = pd.read_json(text, orient='index')
            if sort is not None:
                table = table.sort_values(by=sort)
        except:
            table = None
        return table
    
    @try_exept_dekorator("ComConnector1C", "Ошибка в конвертации данных из 1с в json.")
    def text1c2Json(self, text):
        """
        Переводим текст из 1с в json
        text: текст, который станет jsonом
        """
        #text = json.loads(text)
        try:
            text = json.loads(text)
        except:
            text = None
        return text
    
    #@try_exept_dekorator("ComConnector1C", "Ошибка при добавлении записи в 1с.")
    def setLogDataTo1C(self, _list):
        """
        Переводим текст из 1с в json
        _list -  список со следующими полями:
        
        region: Регион (Казань)
        obj: подразделение из 1с (AAA)
        job: организация из 1с
        time: Время следующего формата ГГГГММДДЧЧММСС
        job_type: Название операции по которому будет поиск информации в 1с
        rez_num: Результат числовой
        rez_text: Результат текстовый
        com_text: Комментарий
        """
        region, obj, job, time, job_type, rez_num, rez_text, com_text = _list
        try:
            V82 = self.connect()
            if self.isServer:
                out = V82.WriteObjectLOG_srv(
                    region, obj, job,
                    time, job_type, rez_num,
                    rez_text, com_text
                )
            else:
                out = V82.WriteObjectLOG(
                    region, obj, job,
                    time, job_type, rez_num,
                    rez_text, com_text
                )
        except:
            raise programExeption("critical", "Ошибка при добавлении записи в 1с.")
        return out   
