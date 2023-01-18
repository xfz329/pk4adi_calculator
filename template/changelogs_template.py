#   -*- coding:utf-8 -*-
#   The author_template.py in FeatureAnalyzer
#   created by Jiang Feng(silencejiang@zju.edu.cn)
#   created at 14:08 on 2022/3/27

class Template:
    tmp = \
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
            <style type=text/css>
                dt {text-align: left;font-family:Times New Roman;font-size: 30px}
                dd.normal {text-align: left;font-family:Times New Roman;font-size: 14px;font-style:normal;}
                dd.italic {text-align: left;font-family:Times New Roman;font-size: 14px;font-style:italic;}
            </style>
        </head>
        <body>
            <dl>
            %(versions)s
            </dl>
        </body>
        </html>
        """
    version = \
        """
        <dt>&emsp;%(num)s</dt>
        <dd class= italic>&emsp;Released on %(date)s</dd>
        %(features)s
        """

    feature = \
        """
        <dd class= normal>&emsp;&emsp;%(feature)s</dd>
        """

    latest_version = "0.01"

    latest_date = "2023.01.07"

    def __init__(self):
        self.res = ""

    def get(self):
        tab = ""

        f = ""
        f +=Template.feature % dict(feature = "完成麻醉深度评估PK值的计算")
        f += Template.feature % dict(feature="支持*.xls、*.xlsx、*.csv等格式的数据输入")
        f += Template.feature % dict(feature="对数据类型有效性进行检查")
        f += Template.feature % dict(feature="显示所有中间辅助变量")
        f += Template.feature % dict(feature="显示所有操作及操作处理结果")
        f += Template.feature % dict(feature="可直接复制PK值至粘贴板")
        tab += Template.version % dict(num = 0.01, date = "2023.01.07", features = f)
        self.res = Template.tmp % dict(versions = tab)

        return self.res


if __name__ == "__main__":
    t= Template()
    t.get()







