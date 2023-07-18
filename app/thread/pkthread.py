#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pkthread.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""
from ..globalvar.vars import set_value, get_value
from .basicthread import BasicThread
from PyQt5.QtCore import pyqtSignal
import pandas as pd
import time
import os
from pk4adi.pk import calculate_pk
from pk4adi.pkc import compare_pks
class PKThread(BasicThread):
    warn_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, name = "pk"):
        super().__init__(name)
        self.data = None

        self.pk_dict = {}
        self.pk_name_dict = {}
        self.pk_n = 0

        self.pks_dict = {}
        self.pks_name_dict = {}
        self.pks_n = 0

        self.warn_str = None
        self.error_str = None
        self.warn_occured = False
        self.work_type = None

    def set_work_type(self, t):
        self.work_type = t

    def run(self):
        self.data = get_value("current_workbook")

        self.pk_dict = get_value("pk_dict")
        self.pk_name_dict = get_value("pk_name_dict")
        self.pk_n = get_value("pk_n")

        self.pks_dict = get_value("pks_dict")
        self.pks_name_dict = get_value("pks_name_dict")
        self.pks_n = get_value("pks_n")


        if self.work_type == "PK":
            self.do_calculate_pk()
        if self.work_type == "PKC":
            self.do_compare_pks()

    def to_files(self, df, type_suffix):

        output_dir = get_value("output_dir")
        full_path = output_dir + "\Analysis_" + time.strftime("%Y-%m-%d", time.localtime())
        if not os.path.exists(full_path):
            os.mkdir(full_path)

        pre = time.strftime("%H-%M-%S", time.localtime()) + "_" + type_suffix
        csv_name_utf8 = os.path.join(full_path, pre + "_utf8.csv")
        csv_name_ansi = os.path.join(full_path, pre + "_ansi.csv")
        xlsx_name = os.path.join(full_path, pre + ".xlsx")

        df = df.round(3)
        df.to_csv(csv_name_utf8)
        df.to_csv(csv_name_ansi, encoding="ansi")
        df.to_excel(xlsx_name)

        set_value("last_write_dir", full_path)

    def do_calculate_pk(self):
        x_names = get_value("x_names")
        y_names = get_value("y_names")
        pk_ready = len(x_names) > 0 and len(y_names) == 1
        if not pk_ready:
            self.error_signal.emit("PK值计算需要设置一个独立变量和至少一个检验变量！")
            return

        pk_columns = ["Independent variables", "Test variables", "PK", "SE0", "SE1", "Jackknife", "PKj", "SEj",
                      "Error Detail"]
        y_name = y_names[0]
        df = pd.DataFrame(columns=pk_columns)
        for x_name in x_names:
            ans = self.query_pk(x_name, y_name)
            if isinstance(ans, dict):
                new_row = [y_name, x_name, ans.get("PK"), ans.get("SE0"), ans.get("SE1"),
                           ans.get("jack_ok"), ans.get("PKj"), ans.get("SEj"), ""]
                df.loc[df.shape[0]] = new_row
            else:
                new_row = [y_name, x_name, "", "", "", "", "", "", ans]
                df.loc[df.shape[0]] = new_row
                self.warn_signal.emit(ans)

        set_value("pk_dict", self.pk_dict)
        set_value("pk_name_dict", self.pk_name_dict)
        set_value("pk_n", self.pk_n)
        set_value("pk", df)

        self.to_files(df, "PK")
        self.finished_signal.emit()

    def do_compare_pks(self):
        x_names = get_value("x_names")
        y_names = get_value("y_names")
        pks_ready = len(x_names) > 1 and len(y_names) == 1
        if not pks_ready:
            self.error_signal.emit("PK值比较需要设置一个独立变量和至少两个检验变量！")
            return

        pks_columns = ["Independent variables", "Test variables 1", "Test variables 2",
                       "PKD", "SED", "ZD", "P value of norm", "Comment 1",
                       "PKDJ", "SEDJ", "DF", "TD", "P value of t", "Comment 2", "Error 1", "Error 2"]
        y_name = y_names[0]
        df = pd.DataFrame(columns=pks_columns)

        for i in x_names:
            for j in x_names:
                if i != j:
                    ans = self.query_pks(i, j, y_name)
                    if isinstance(ans, dict):
                        new_row = [y_name, i, j,
                                   ans.get("PKD"), ans.get("SED"), ans.get("ZD"), ans.get("ZP"), ans.get("ZJ"),
                                   ans.get("PKDJ"), ans.get("SEDJ"), ans.get("DF"), ans.get("TD"), ans.get("TP"),
                                   ans.get("TJ"), "", ""]
                        df.loc[df.shape[0]] = new_row

                    if isinstance(ans, list):
                        if isinstance(ans[0], dict):
                            e1 = ""
                        else:
                            e1 = ans[0]
                        if isinstance(ans[1], dict):
                            e2 = ""
                        else:
                            e2 = ans[1]

                        new_row = [y_name, i, j,
                                   "", "", "", "", "",
                                   "", "", "", "", "", "", e1, e2]
                        df.loc[df.shape[0]] = new_row

        set_value("pk_dict", self.pk_dict)
        set_value("pk_name_dict", self.pk_name_dict)
        set_value("pk_n", self.pk_n)

        set_value("pks_dict", self.pks_dict)
        set_value("pks_name_dict", self.pks_name_dict)
        set_value("pks_n", self.pks_n)

        set_value("pks", df)
        self.to_files(df, "PKC")
        self.finished_signal.emit()

    def query_pk(self, x, y):
        for k in self.pk_name_dict:
            if [x, y] == self.pk_name_dict.get(k, "unknown"):
                return self.pk_dict.get(k, "unknown")
        ans = self.get_pk(x, y)
        key = str(self.pk_n)
        self.pk_name_dict.update({ key : [x, y] })
        self.pk_dict.update({key: ans})
        self.pk_n = self.pk_n + 1
        return ans

    def query_pks(self, x1, x2, y):
        for k in self.pks_name_dict:
            if [x1, x2, y] == self.pks_name_dict.get(k, "unknown"):
                return self.pks_dict.get(k, "unknown")
        pk1 = self.query_pk(x1, y)
        pk2 = self.query_pk(x2, y)
        if isinstance(pk1, dict) and isinstance(pk2, dict):
            ans = compare_pks(pk1, pk2, False)
            key = str(self.pks_n)
            self.pks_name_dict.update({key: [x1, x2, y]})
            self.pks_dict.update({key: ans})
            self.pks_n = self.pks_n + 1
            return ans
        return [pk1, pk2]


    def get_pk(self, xn, yn):
        x = self.data.loc[:, xn]
        y = self.data.loc[:, yn]

        if x.apply(lambda n: not isinstance(n, (int, float))).any():
            warn_str = "检验变量数据类型错误，需要为整型或浮点型"
            return warn_str
        if x.isna().any():
            warn_str = "检验变量包含非数值字符"
            return warn_str
        if y.apply(lambda n: not isinstance(n, (int, float))).any():
            warn_str = "独立变量数据类型错误，需要为整型或浮点型"
            return warn_str
        if y.isna().any():
            warn_str = "独立变量包含非数值字符"
            return warn_str
        lx = len(x)
        ly = len(y)
        if lx != ly or lx < 2:
            warn_str = "独立变量与观测变量长度不等或长度小于2"
            return warn_str
        sy = y.tolist()
        if len(set(sy)) < 2:
            warn_str = "独立变量需要包含至少2个区分数值"
            return warn_str
        return calculate_pk(x, y, False)





