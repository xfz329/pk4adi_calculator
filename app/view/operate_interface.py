# coding:utf-8

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from .frame.listframe import ListFrame
from .widget.operate_toolbar import OperateToolBar

class OperateInterface(GalleryInterface):
    """ View interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.view,
            subtitle="对已选数据进行分析",
            parent=parent
        )
        self.setObjectName('operateInterface')

        # list view
        self.addExampleCard(
            title=self.tr('A simple ListView'),
            widget=ListFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/list_view/demo.py'
        )

        toolbar = OperateToolBar("", "", self)
        self.setToolbar(toolbar)









