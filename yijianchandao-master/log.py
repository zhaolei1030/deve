# coding:utf-8
import requests
import time
from chandao.login_chandao import Login
from chandao.get_id import get_id_title


class AddBug():
    def __init__(self, s,product,module,assignedTo,title,severity,description,reason,influence_range,mailto):
        self.s = s
    def add_bug(self):

        url = "http://chandao_url.html"

        body = {
            "product": "{}".format(product),
            "module": "{}".format(module),
            "project": "",
            "openedBuild[]": "trunk",  # 影响版本
            "assignedTo": "{}".format(assignedTo),
            "deadline": "",
            "type": "codeerror",
            "os": "",
            "browser": "",
            "color": "",
            "title": '{}'.format(title),
            "severity": "{}".format(int(severity)+1),
            "pri": "2",
            "steps": '<p>[详细描述]{}</p> \
                         <p>[根本原因]{}</p> \
                         <p>[影响范围]{}</p>'.format(description,reason,influence_range),
            "story": "0".format(),
            "task": "0",
            "mailto[]": "{}.format()",
            "keywords": "",
            "files[]": "",
            "labels[]": "",
            "uid": "xxxxxxx",
            "case": "0",
            "caseVersion": "0",
            "result": "0",
            "testtask": "0"
        }
        r = self.s.post(url, data=body)
        print("添加BUG: %s" % r.text)
        return r.text

def insert_bug_info(product,module,assignedTo,title,severity,description,reason,influence_range,mailto):
    """
    往cd插入bug信息
    :param product:
    :param module:
    :param assignedTo:
    :param title:
    :param severity:
    :param description:
    :param reason:
    :param influence_range:
    :param mailto:
    :return:
    """
    s = requests.session()
    zen = Login(s)
    zen.login()
    bug = AddBug(s,product,module,assignedTo,title,severity,description,reason,influence_range,mailto)
    bug.add_bug()
    got_id, got_title = get_id_title(product)
    print(got_title)
    if got_title == title:
        return 'http://chandao_url.html'.format(got_id)
    else:
        return '未创建成功'
if __name__ == '__main__':
    product = xxx
    module = xxxxx
    assignedTo = 'xxxxxx'
    title = '插入禅道信息无日期'
    severity = x
    pri = x
    description = x
    reason = x
    influence_range = x
    mailto = 'xxxxxx'
    print(insert_bug_info(product,module,assignedTo,title,severity,description,reason,influence_range,mailto))