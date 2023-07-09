#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   about.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
class Template:
    abt = \
"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Title</title>
<style type=text/css>
    h1 {text-align: center;font-family:Times New Roman;font-size: 30px}
    p.normal {text-align: center;font-family:Times New Roman;font-size: 14px;font-style: normal}
    p.strong {text-align: center;font-family:Times New Roman;font-size: 14px;font-style: normal; font-weight: bold}
</style>
</head>
<body>
<div align="center">
    <img src="./figures/pk.png" alt="PK logo" width="454" height="454" align="center">
</div>
<p class = strong>PK4ADI计算器 0.1.3.c</p>
<p class = normal>(基于PK4ADI 0.1.3)</p>
<br>
<p class = strong>开发团队</p>
<p class = normal>浙江大学生物医学工程与仪器科学学院</p>
<p class = normal>陈杭 教授团队</p>
<p class = normal>浙江大学医学院附属妇产科医院</p>
<p class = normal>陈新忠 教授团队</p>
<br>
<p class = strong>开发人员</p>
<p class = normal>江锋</p>
<p class = normal>李华</p>
<p class = normal>张梦鸽</p>
<p class = normal>陈婉琳</p>
<br>
<p class = strong>软件内核</p>
<p class = normal><a href="https://github.com/xfz329/pk4adi">PK4ADI</a></p>
<br>
<p class = strong>感谢</p>
<p class = normal><a href="https://www.csus.edu/faculty/s/smithwd/">Dr. Warren D. Smith</a></p>
<br>
<p class = strong>联系我们</p>
<p class = normal>silencejiang@zju.edu.cn</p>
<br>
<p class = strong>Copyright © 2004-2020 浙江大学</p>
<br>
<p class = strong>本软件基于MIT协议开源</p>
<p class = normal>特此免费授予任何获得本软件副本和相关文档文件（下称“软件”）的人不受限制地处置该软件</p>
<p class = normal>的权利，包括不受限制地使用、复制、修改、合并、发布、分发、转授许可和/或出售该软件副</p>
<p class = normal>本，以及再授权被配发了本软件的人如上的权利，须在下列条件下：上述版权声明和本许可声明</p>
<p class = normal>应包含在该软件的所有副本或实质成分中。</p>
</br>
<p class = normal>本软件是“如此”提供的，没有任何形式的明示或暗示的保证，包括但不限于对适销性、特定用</p>
<p class = normal>途的适用性和不侵权的保证。在任何情况下，作者或版权持有人都不对任何索赔、损害或其他责</p>
<p class = normal>任负责，无论这些追责来自合同、侵权或其它行为中，还是产生于、源于或有关于本软件以及本</p>
<p class = normal>软件的使用或其它处置。</p>
<br>
<p class = strong>This software is open source based on the MIT license.</p>
<p class = normal>Permission is hereby granted, free of charge, to any person obtaining a copy of this</p>
<p class = normal>software and associated documentation files (the “Software”), to deal in the Software</p>
<p class = normal>without restriction, including without limitation the rights to use, copy, modify, merge,</p>
<p class = normal>publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons</p>
<p class = normal>to whom the Software is furnished to do so, subject to the following conditions: The</p>
<p class = normal>above copyright notice and this permission notice shall be included in all copies or</p> 
<p class = normal>substantial portions of the Software.</p>
<p class = normal>The Software is provided “as is”, without warranty of any kind, express or implied,</p>
<p class = normal>including but not limited to the warranties of merchantability, fitness for a particular</p> 
<p class = normal>purpose and noninfringement. In no event shall the authors or copyright holders be</p>
<p class = normal>liable for any claim, damages or other liability, whether in an action of contract, tort</p>
<p class = normal>or otherwise, arising from, out of or in connection with the software or the use or other</p>
<p class = normal>dealings in the Software.</p>
</body>
</html>
"""
    logs = \
"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Title</title>
<style type=text/css>
    h1 {text-align: center;font-family:Times New Roman;font-size: 30px}
    p.normal {text-align: center;font-family:Times New Roman;font-size: 14px;font-style: normal}
    p.strong {text-align: center;font-family:Times New Roman;font-size: 14px;font-style: normal; font-weight: bold}
    p.italic {text-align: center;font-family:Times New Roman;font-size: 14px;font-style: italic; font-weight: bold}
</style>
</head>
<body>
<div align="center">
    <img src="./figures/pk.png" alt="PK logo" width="454" height="454" align="center">
</div>
<p class = strong>PK4ADI计算器 更新日志</p>
<br>
<p class = italic>0.1.3.d released on 2022.07.09</p>
<p class = normal>基于PK4ADI 0.1.3</p>
<p class = normal>调整了分析窗口的默认大小，增加了窗口最大化功能</p>
<p class = normal>为分析窗口的变量设置增加了复选功能</p>
<br>
<p class = italic>0.1.3.c released on 2022.06.27</p>
<p class = normal>基于PK4ADI 0.1.3</p>
<p class = normal>软件UI设计优化，完善了相关帮助功能</p>
<p class = normal>软件输出日志规范</p>
<p class = normal>其他功能完善等</p>
<br>
<p class = italic>0.1.3.b released on 2022.06.26</p>
<p class = normal>基于PK4ADI 0.1.3</p>
<p class = normal>支持对包含多个工作簿的xls、xlsx文件进行分析</p>
<p class = normal>软件UI优化</p>
<br>
<p class = italic>0.1.3.a released on 2022.06.20</p>
<p class = normal>基于PK4ADI 0.1.3</p>
<p class = normal>完全支持基于PK4ADI 0.1.3的全部功能</p>
<p class = normal>软件UI重新设计</p>
<p class = normal>引入线程读取文件</p>
<p class = normal>引入软件操作日志</p>
<p class = normal>可批量分析PK值、批量比较多个PK值</p>
<p class = normal>可将分析结果导出为xlsx与csv文件</p>
<p class = normal>可为每次分析增加批注</p>
<br>
<p class = italic>0.0.1 released on 2022.01.18</p>
<p class = normal>基于PK4ADI 0.0.1</p>
<p class = normal>完全支持基于PK4ADI 0.1.1的全部功能</p>
</body>
</html>
"""
    mydict = {"about" : abt, "logs" : logs }
    def __init__(self):
        self.res = ""

    def get(self, tp):
        return Template.mydict.get(tp,"None")


if __name__ == "__main__":
    t= Template()
    ans = t.get()
    print(ans)