#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.17 22:00:00                  #
# ================================================== #

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout

from ..widget.image import GeneratedImageLabel
from ..widget.dialog import GeneratedImageDialog
from ...utils import trans


class Image:
    def __init__(self, window=None):
        """
        Image dialog

        :param window: Window instance
        """
        self.window = window
        self.path = None

    def setup(self):
        """Setup image dialog"""
        id = 'image'
        self.window.ui.nodes['dialog.image.pixmap'] = {}

        for i in range(0, 4):
            self.window.ui.nodes['dialog.image.pixmap'][i] = GeneratedImageLabel(self.window, self.path)
            self.window.ui.nodes['dialog.image.pixmap'][i].setMaximumSize(512, 512)

        row_one = QHBoxLayout()
        row_one.addWidget(self.window.ui.nodes['dialog.image.pixmap'][0])
        row_one.addWidget(self.window.ui.nodes['dialog.image.pixmap'][1])

        row_two = QHBoxLayout()
        row_two.addWidget(self.window.ui.nodes['dialog.image.pixmap'][2])
        row_two.addWidget(self.window.ui.nodes['dialog.image.pixmap'][3])

        layout = QVBoxLayout()
        layout.addLayout(row_one)
        layout.addLayout(row_two)

        self.window.ui.dialog[id] = GeneratedImageDialog(self.window, id)
        self.window.ui.dialog[id].setLayout(layout)
        self.window.ui.dialog[id].setWindowTitle(trans("dialog.image.title"))
