# coding:utf-8

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from .frame.tableframe import TableFrame
from .widget.data_toolbar import DataToolBar

class DataInterface(GalleryInterface):
    """ Data interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.view,
            subtitle="选择需要分析的数据",
            parent=parent
        )
        self.setObjectName('dataInterface')

        # table view
        self.tableframe = TableFrame(self)
        self.addExampleCard(
            title=self.tr('A simple TableView'),
            widget=self.tableframe,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/table_view/demo.py',
            stretch= 1
        )

        toolbar = DataToolBar("", "", self)
        self.setToolbar(toolbar)
        self.toolBar.newDataReadSig.connect(self.tableframe.updateData)









