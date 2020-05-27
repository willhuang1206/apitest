from datetime import datetime,timedelta
import math
import time

class DateUtil:
    """
    日期工具类
    """

    @staticmethod
    def delta_day(delta=0):
        """
        :param delta:   偏移量
        :return:        0今天, 1昨天, 2前天, -1明天 ...
        """
        return (datetime.now() + timedelta(days=delta)).strftime('%Y-%m-%d')

    @staticmethod
    def delta_week(delta=0):
        """
        :param delta:   偏移量
        :return:        0本周, -1上周, 1下周 ...
        """
        now = datetime.now()
        week = now.weekday()
        _from = (now - timedelta(days=week - 7 * delta)).strftime('%Y-%m-%d')
        _to = (now + timedelta(days=6 - week + 7 * delta)).strftime('%Y-%m-%d')
        return _from, _to

    @staticmethod
    def delta_month(delta=0):
        """
        :param delta:   偏移量
        :return:        0本月, -1上月, 1下月, 下下个月...
        """

        def _delta_month(__year, __month, __delta):
            _month = __month + __delta
            if _month < 1:
                delta_year = math.ceil(abs(_month) / 12)
                delta_year = delta_year if delta_year else 1
                __year -= delta_year
                _month = delta_year * 12 + __month + __delta
            elif _month > 12:
                delta_year = math.floor(_month / 12)
                __year += delta_year
                _month %= 12
            return __year, _month

        now = datetime.now()
        _from = datetime(*_delta_month(now.year, now.month, delta), 1)

        _to = datetime(*_delta_month(_from.year, _from.month, 1), 1) - timedelta(days=1)
        return _from.strftime('%Y-%m-%d'), _to.strftime('%Y-%m-%d')

    @staticmethod
    def delta_year(delta=0):
        """
        :param delta:   偏移量
        :return:        0今年, -1去年, 1明年 ...
        """
        now = datetime.now()
        _from = datetime(now.year + delta, 1, 1)
        _to = datetime(_from.year + 1, 1, 1) - timedelta(days=1)
        return _from.strftime('%Y-%m-%d'), _to.strftime('%Y-%m-%d')


if __name__ == '__main__':
    print('当前日期: ', datetime.now())
    print('*' * 40)
    print('今天: ', DateUtil.delta_day())
    print('昨天: ', DateUtil.delta_day(-1))
    print('前天: ', DateUtil.delta_day(-2))
    print('明天: ', DateUtil.delta_day(1))
    print('后天: ', DateUtil.delta_day(2))
    print('*' * 40)
    print('本周: ', DateUtil.delta_week())
    print('上周: ', DateUtil.delta_week(-1))
    print('下周: ', DateUtil.delta_week(1))
    print('*' * 40)
    print('本月: ', DateUtil.delta_month())
    print('上月: ', DateUtil.delta_month(-1))
    print('下月: ', DateUtil.delta_month(1))
    print('*' * 40)
    print('本年: ', DateUtil.delta_year())
    print('去年: ', DateUtil.delta_year(-1))
    print('明年: ', DateUtil.delta_year(1))

    time1 = time.time()
    #要度量时间的程序
    time.sleep(0.3)
    time2 = time.time()

    print(int((time2 - time1)*1000))