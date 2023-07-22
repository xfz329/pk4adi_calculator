#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   pkthread.py    
@Contact :   Jiang Feng(silencejiang@zju.edu.cn)
@License :   (C)Copyright 2004-2020, Zhejiang University
"""

import pandas as pd
import time
import os
from pk4adi.pk import calculate_pk
from pk4adi.pkc import compare_pks

from PyQt5.QtCore import pyqtSignal

from globalvar.vars import set_value, get_value
from thread.basicthread import BasicThread
from utils.logger import Logger

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

        self.logger = Logger().get_logger()

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

        self.logger.info(self.tr("Working in the thread."))

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

        df.to_csv(csv_name_utf8)
        df.to_csv(csv_name_ansi, encoding="ansi")
        df.to_excel(xlsx_name)

        set_value("last_work_file", xlsx_name)
        set_value("last_work_dir", full_path)

        self.logger.info(self.tr("Save the result to the following files."))
        self.logger.info(csv_name_utf8)
        self.logger.info(csv_name_ansi)
        self.logger.info(xlsx_name)

    def do_calculate_pk(self):
        x_names = get_value("x_names")
        y_names = get_value("y_names")
        pk_ready = len(x_names) > 0 and len(y_names) == 1
        if not pk_ready:
            self.error_signal.emit(self.tr("Must set a independent variable only and a test variable at least for calculating the PKs."))
            self.logger.error(self.tr("Must set a independent variable only and a test variable at least for calculating the PKs."))
            return

        pk_columns = [self.tr("Independent variables"), self.tr("Test variables"), "PK", "SE0", "SE1", self.tr("Jackknife"), "PKj", "SEj",
                      self.tr("Error Detail")]
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
                self.logger.error(self.tr("The result above contains error, calculate pk failed."))

        self.logger.info(self.tr("Calculate PKs command finished. Start saving the results."))
        df = df.applymap(self.myround)

        set_value("last_work", "pk")
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
            self.error_signal.emit(self.tr("Must set a independent variable only and two test variables at least for comparing the PKs."))
            self.logger.error(self.tr("Must set a independent variable only and two test variables at least for comparing the PKs."))
            return

        pks_columns = [self.tr("Independent variables"), self.tr("Test variables 1"), self.tr("Test variables 2"),
                       "PKD", "SED", "ZD", self.tr("P value of norm"), self.tr("Comment 1"),
                       "PKDJ", "SEDJ", "DF", "TD", self.tr("P value of t"), self.tr("Comment 2"), self.tr("Error 1"), self.tr("Error 2")]
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
                            self.warn_signal.emit(e1)
                        if isinstance(ans[1], dict):
                            e2 = ""
                        else:
                            e2 = ans[1]
                            self.warn_signal.emit(e2)

                        new_row = [y_name, i, j,
                                   "", "", "", "", "",
                                   "", "", "", "", "", "", e1, e2]
                        df.loc[df.shape[0]] = new_row
                        self.logger.error(self.tr("The result above contains error, compare pks failed."))

        self.logger.info(self.tr("Compare PKs command finished. Start saving the results."))
        df = df.applymap(self.myround)

        set_value("last_work", "pks")
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
        self.logger.info(self.tr("Query the PK between {0} and {1}").format(x, y))
        for k in self.pk_name_dict:
            if [x, y] == self.pk_name_dict.get(k, "unknown"):
                self.logger.info(self.tr("Get the cache result."))
                return self.pk_dict.get(k, "unknown")
        self.logger.info(self.tr("There is no cache result, start calculating PK."))
        ans = self.get_pk(x, y)
        self.logger.info(self.tr("Calculating PK finished, the result is as the following."))
        self.logger.debug(ans)

        key = str(self.pk_n)
        self.pk_name_dict.update({ key : [x, y] })
        self.pk_dict.update({key: ans})
        self.pk_n = self.pk_n + 1
        return ans

    def query_pks(self, x1, x2, y):
        self.logger.info(self.tr("Query the PKs' comparison result between the PK value of {0} and {1} and the PK value of {2} and {3}.").format(x1, y, x2, y))
        for k in self.pks_name_dict:
            if [x1, x2, y] == self.pks_name_dict.get(k, "unknown"):
                self.logger.info(self.tr("Get the cache result."))
                return self.pks_dict.get(k, "unknown")
        self.logger.info(self.tr("There is no cache result, start compare PK."))
        pk1 = self.query_pk(x1, y)
        pk2 = self.query_pk(x2, y)
        self.logger.info(self.tr("Comparing PK finished, the result is as the following."))
        if isinstance(pk1, dict) and isinstance(pk2, dict):
            ans = compare_pks(pk1, pk2, False)
            key = str(self.pks_n)
            self.pks_name_dict.update({key: [x1, x2, y]})
            self.pks_dict.update({key: ans})
            self.pks_n = self.pks_n + 1
            self.logger.debug(ans)
            return ans
        ans = [pk1, pk2]
        self.logger.debug(ans)
        return ans

    def get_pk(self, xn, yn):
        x = self.data.loc[:, xn]
        y = self.data.loc[:, yn]

        if x.apply(lambda n: not isinstance(n, (int, float))).any():
            warn_str = self.tr("The test variable's data type errors, it should be the int or float.")
            return warn_str
        if x.isna().any():
            warn_str = self.tr("The test variable contains nan.")
            return warn_str
        if y.apply(lambda n: not isinstance(n, (int, float))).any():
            warn_str = self.tr("The independent variable's data type errors, it should be the int or float.")
            return warn_str
        if y.isna().any():
            warn_str = self.tr("The independent variable contains nan.")
            return warn_str
        lx = len(x)
        ly = len(y)
        if lx != ly or lx < 2:
            warn_str = self.tr("The lengths of test and independent variable are not equal or the length less than 2.")
            return warn_str
        sy = y.tolist()
        if len(set(sy)) < 2:
            warn_str = self.tr("The independent variable should contain 2 distinct values at least.")
            return warn_str
        return calculate_pk(x, y, False)

    def myround(self, n ):
        if isinstance(n, float):
            return round(n,3)
        return n




