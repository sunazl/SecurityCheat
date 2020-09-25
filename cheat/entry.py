import json
import os
import sys
from configparser import ConfigParser

from django.db.models import QuerySet
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from SecurityCheat import settings
from cheat.utils.json_utils import ComplexEncoder
from cheat.utils.log import log


# 引入模块并缓存
def import_module(import_str):
    __import__(import_str)
    return sys.modules[import_str]


# 允许跨域请求
@csrf_exempt
def ctrl(request):
    if request.method != 'POST':
        return HttpResponse(json.dumps({'tag': '请使用post！'}, cls=ComplexEncoder), content_type='application/json')
    else:
        return router_rest(request)


# 处理post请求
def router_rest(request):
    body = request.body
    p_data = str(body, encoding="utf8")
    if not p_data:
        return HttpResponse(json.dumps({'tag': '数据解析错误,无法从请求中获取到正确的值'}, cls=ComplexEncoder, ensure_ascii=False),
                            content_type='application/json')

    p_data = json.loads(p_data)
    try:
        ctrl_name = p_data.get('ctrl', None)
        class_name = ctrl_name.split("=")[0]
        method_name = ctrl_name.split("=")[1]
    except:
        return HttpResponse(json.dumps({'tag': 'URI解析失败'}, cls=ComplexEncoder, ensure_ascii=False),
                            content_type='application/json')
    # 入口
    result = exe_ctrl(class_name, method_name, p_data)

    if result:
        return HttpResponse(json.dumps(result, cls=ComplexEncoder, ensure_ascii=False),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps({'tag': '发送了错误的URI'}, cls=ComplexEncoder, ensure_ascii=False),
                            content_type='application/json')


def test():
    print("ok")


# 解析ctrl
def exe_ctrl(class_name, method_name, p_data):
    # 查询是否存在此ctrl
    config = ConfigParser()
    cur_path = settings.BASE_DIR + ""
    config_path = os.path.join(cur_path, 'ctrl.ini')
    config.read(config_path)
    if not config.has_option("ctrl", class_name + '.py'):
        log.error("没有文件" + class_name + ".py,请检查")
        return HttpResponse(content_type='application/json')
    folder = config.get("ctrl", class_name + ".py")

    # 导入这个方法
    imp_name = folder.replace('\\', '.').replace('/', '.') + "." + class_name
    obj = import_module(imp_name)
    # 查询方法是否存在
    if not hasattr(obj, method_name):
        log.error("没有成功加载" + class_name + "下的" + method_name + "方法,请检查")
        return False

    # 获取对象中的方法 并执行
    func = getattr(obj, method_name)
    dict_ = func(p_data)
    if dict_:
        if isinstance(dict_, QuerySet):
            # 防止json转换失败
            return list(dict_)
        return dict_
    else:
        return False

    # if dict_ is  not None and dict_.get_send() is None:
    #     return HttpResponse(json.dumps(dict_.get_data(), cls=ComplexEncoder), content_type='application/json')
    # else:
    #     return dict_.get_send()
