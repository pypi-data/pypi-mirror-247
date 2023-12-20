
import datetime
from dateutil.relativedelta import relativedelta
def now():
    """
    获取当前时间
    :return: 当前时间
    """
    return datetime.datetime.now()
def str2time(string: str, format: str = "%Y-%m-%d %H:%M:%S"):
    """
    字符串转时间
    :param string: 字符串
    :param format: 格式
    :return: 时间
    """
    return datetime.datetime.strptime(string, format)

def getExcelTime(delta: int, format: str = "%Y-%m-%d"):
    """
    获取Excel时间 excel时间格式为常规时使用该函数
    :param delta: excel天数
    :param format: 格式
    :return: Excel时间
    """
    delta = datetime.timedelta(days=delta)
    return datetime.datetime.strftime(datetime.datetime.strptime('1899-12-30', '%Y-%m-%d')+delta, format)

def time2str(time: datetime, format: str = "%Y-%m-%d %H:%M:%S"):
    """
    时间转字符串
    :param time: 时间
    :param format: 格式
    :return: 字符串
    """
    return datetime.datetime.strftime(time, format)

def getYear(time: datetime):
    """
    获取年份
    :param time: 时间
    :return: 年份
    """
    return time.year

def getMonth(time: datetime):
    """
    获取月份
    :param time: 时间
    :return: 月份
    """
    return time.month

def getDay(time: datetime):
    """
    获取天数
    :param time: 时间
    :return: 天数
    """
    return time.day

def getWeekDay(time: datetime):
    """
    获取星期几
    :param time: 时间
    :return: 星期
    """
    return time.weekday()

def getWeek(time: datetime):
    """
    获取第几周
    :param time: 时间
    :return: 周次
    """
    return time.isocalendar()[1]

def calTimeDelta(time1: datetime, time2: datetime, type: str = "seconds"):
    """
    计算两个时间差
    :param time1: 时间1
    :param time2: 时间2
    :param type: 返回类型 seconds-秒 minutes-分钟 hours-小时 days-天 months-月 years-年
    :return: 时间差
    """
    if type == "seconds":
        result = (time1 - time2).total_seconds()
    elif type == "minutes":
        result = (time1 - time2).total_seconds() / 60
    elif type == "hours":
        result = (time1 - time2).total_seconds() / 3600
    elif type == "days":
        result = (time1 - time2).days
    elif type == "months":
        result = (time1.year - time2.year) * 12 + (time1.month - time2.month)
    else:
        result = (time1.year - time2.year)
    result = abs(result)
    return result

def changeTimeDelta(time: datetime, seconds: int = 0, minutes: int = 0, hours: int = 0, days: int = 0, months: int = 0, years: int = 0):
        """
        :param time: 初始时间
        :param seconds: 秒
        :param minutes: 分钟
        :param hours: 小时
        :param days: 天数
        :param months: 月份
        :param years: 年份
        :return: 变动日期
        """
        return time + relativedelta(seconds=seconds, minutes=minutes, hours=hours, days=days, months=months, years=years)