from datetime import datetime
import time

# MARK: MATH

def rect_sqwr(rect):
    return rect[4] * rect[5]

# MARK: TIME

def timeToStringWithFormat(time, _from = "%d.%m.%Y %H:%M:%S", _to = "%Y%m%d%H%M%S"):
    """
    Переводим один формат в другой
    """
    time = str(time)
    time = datetime.strptime(time, _from)
    time = time.strftime(_to)
    return time

    
def fullDateToHHMMSS(time):
    """
    Переводим дату с временем из 1с в вид для отображения
    """
    return timeToStringWithFormat(time, "%d.%m.%Y %H:%M:%S", "%H : %M : %S")

def oneSymToTwoSym(sym):
    if len(sym) == 1:
        sym = "0" + sym
    return sym

def secToHHMMSS(sec):
    """
    Переводим секунды для отображения в виде - "00:00:00"
    """
    rezult = "00:00:00"
    if sec != 0:
        _time = time.gmtime(sec)
        #_time = time.strptime(_time)
        #rezult = time.strftime("%H:%M:%S", _time)
        hh = str(_time.tm_hour)
        hh = oneSymToTwoSym(hh)
        mm = str(_time.tm_min)
        mm = oneSymToTwoSym(mm)
        ss = str(_time.tm_sec)
        ss = oneSymToTwoSym(ss)
        rezult = "%s:%s:%s" % (hh, mm, ss)
    return rezult

def secToHHMMwithText(sec):
    """
    Переводим секунды для отображения в виде - "1 ч 2 мин"
    """
    rezult = "0 мин"
    if sec != 0:
        _time = time.gmtime(sec)
        #_time = time.strptime(_time)
        #rezult = time.strftime("%H:%M:%S", _time)
        hh = str(_time.tm_hour)
        hh = oneSymToTwoSym(hh)
        mm = str(_time.tm_min)
        mm = oneSymToTwoSym(mm)
        if hh == "00":
            rezult = "%s мин" % (mm)
        else:
            rezult = "%s ч %s мин" % (hh, mm)
    return rezult    
# MARK: TEXT

def textToVector(text):
    """
    "5.3,6.4" -> [5.3, 6.4]
    """
    return list(map(float, text.rsplit(",")))

# MARK: BOXES
def boxSizeNormilize(box, w, h):
    """
    Нормализуем прямоугольник по ширине и высоте фрейма
    """
    return [box[0] / w, box[1] / h, box[2] / w, box[3] / h]

def boxSizeOriginal(box, w, h):
    """
    Возвращаем оригинальные значения прямоугольника
    """
    return [int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)]

def splitText2Int(text):
    text = text.replace(" ", "")
    text = text.split(",")
    text = [int(elem) for elem in text]
    return text

def xywh2ltrb(_list):
    """ 
    Конвертируем (2) в (1)
    1 = (X и Y левого верхнего и X и Y нижнего правого)
    2 = (X и Y центра зоны и ширина и высота)
    """
    x, y, w, h = _list
    x1 = x - w/2
    y1 = y - h/2
    
    x2 = x + w/2
    y2 = y + h/2
    return [x1, y1, x2, y2]


def detectedIOU(boxA, boxB):
    """
    Насколько сходится зона и объект
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def detectedATOB(boxA, boxB):
    """
    Во сколько раз А меньше Б
    """
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    return boxAArea / boxBArea
    

def detectedBINA(boxA, boxB):
    """
    Насколько объект A относится к зоне B
    Даже если объект А не в Б
    """
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])

    bina = interArea / float(boxAArea)
    return bina
