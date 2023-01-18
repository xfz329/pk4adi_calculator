#   -*- coding:utf-8 -*-
#   The author_template.py in FeatureAnalyzer
#   created by Jiang Feng(silencejiang@zju.edu.cn)
#   created at 14:08 on 2022/3/27
from template.changelogs_template import Template as ct

class Template:
    tmp = \
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
            <style type=text/css>
                h1 {text-align: center;font-family:Times New Roman;font-size: 30px}
                p {text-align: center;font-family:Times New Roman;font-size: 14px}
            </style>
        </head>
        <body>
            <h1>麻醉深度评估PK值计算器</h1>
            <br>
            <p>浙江大学生物医学工程与仪器科学学院</p>
            <p>陈杭 教授团队研发</p>
            <br>
            <p>Copyright © 2004-2020 浙江大学</p>
            <p>Version  %(num)s Released on %(date)s</p>
        </body>
        </html>
        """

    def __init__(self):
        self.res = ""

    def get(self):
        self.res = Template.tmp % dict(num = ct.latest_version, date = ct.latest_date)
        # print(self.res)
        return self.res


if __name__ == "__main__":
    t= Template()
    t.get()







