'''
检测用户在线状态
'''
import threading
import time


from utils.log import log


def check_status(req):
    user_id = req["user_id"]
    check_time_stamp = time.time(),  # 时间戳
    check_time = req["check_time"]  # 时间
    login_time = req["login_time"]  #
    info = user_cache.get_user_check_info(user_id)
    # 更新用户状态
    user_cache.onfine(user_id)
    if not info:
        user_cache.set_user_check_info(user_id, check_time_stamp, check_time, login_time, 'alive')
    return "alive"


class UserCache():
    def __init__(self):
        self.user_check_info_num = {}
        self.user_check_info = []

    def get_user_check_info(self, user_id):
        if self.user_check_info_num.__contains__(user_id):
            return self.user_check_info[self.user_check_info_num[user_id]]
        else:
            return {}

    def set_user_check_info(self, user_id, check_time_stamp, check_time, login_time, status):
        # 节省时间
        if not self.user_check_info_num.__contains__(user_id):
            self.user_check_info_num['user_id'] = len(self.user_check_info)
        else:
            num = self.user_check_info_num['user_id']

            self.user_check_info[num] = {'user_id': user_id, 'check_time_stamp': check_time_stamp,
                                         "check_time": check_time,
                                         "login_time": login_time, 'status': status}

    def offine(self, user_id):
        # 节省时间
        if not self.user_check_info_num.__contains__(user_id):
            self.user_check_info_num['user_id'] = len(self.user_check_info)
        else:
            num = self.user_check_info_num['user_id']

            self.user_check_info[num]["status"] = "offine"

    def onfine(self, user_id):
        # 节省时间
        if not self.user_check_info_num.__contains__(user_id):
            self.user_check_info_num['user_id'] = len(self.user_check_info)
        else:
            num = self.user_check_info_num['user_id']

            self.user_check_info[num]["status"] = "alive"

    def get_check_user(self):
        return self.user_check_info_num, self.user_check_info


user_cache = UserCache()



class check_util():
    def __init__(self):
        pass

    def check_alive(self):
        log.debug("执行检查")
        user_check_info_num, user_check_info = user_cache.get_check_user()
        check_time_stamp = time.time()
        for user in user_check_info_num:
            # 大于五分钟表示超时或者退出
            from models import Token
            if user['check_time_stamp'] - check_time_stamp > 3000:
                Token.objects.filter(user_id=user['user_id']).update(token=None)
                user_cache.offine(user['user_id'])
                log.debug("用户" + user['user_id'] + "已下线")
            else:
                log.debug("用户" + user['user_id'] + "状态正常")
        log.debug("检查结束")

check = check_util()


def check___():
    check.check_alive()