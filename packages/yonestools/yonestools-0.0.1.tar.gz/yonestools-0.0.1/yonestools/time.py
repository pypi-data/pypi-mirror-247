from datetime import datetime


def str2time(string: str, format: str = "%Y-%m-%d %H:%M:%S"):
    """
    字符串转时间
    :param string: 字符串
    :param format: 格式
    :return: 时间
    """
    return datetime.strptime(string, format)