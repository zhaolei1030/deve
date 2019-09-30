# coding:utf-8
import requests


class Login():
    def __init__(self, s):
        self.s = s

    def login(self, user="user_name", password="password"):
        """
        登录cd
        :param user:
        :param password:
        :return:
        """
        url = "http://chandao_url.com/user-login.html"
        head = {"Content-Type": "application/x-www-form-urlencoded"
                }
        body = {"account": user,
                "password": password,
                "keepLogin[]": "on",
        }
        r = self.s.post(url, headers=head, data=body)
        print(r.status_code)
        print(r.content.decode("utf-8"))
        return r.content.decode("utf-8")

    def decide_login_success(self, result):
        """
        验证是否登陆成功
        :param result:
        :return:
        """
        if "parent.location=" in result:
            print("登录成功!")
            return True
        elif "登录失败，请检查您的用户名或密码是否填写正确" in result:
            print("登录失败，用户名或密码不对")
            return False
        else:
            print("登录失败，其它问题：%s" %result)
            return False

if __name__ == '__main__':
    s = requests.session()
    zentao = Login(s)
    result = zentao.login()             # 登录禅道
    zentao.decide_login_success(result) # 判断结果