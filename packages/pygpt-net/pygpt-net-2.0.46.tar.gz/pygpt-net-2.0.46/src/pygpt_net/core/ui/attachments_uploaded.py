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

from PySide6.QtGui import QStandardItemModel, Qt
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QHBoxLayout, QCheckBox, QLabel, QWidget

from .widget.select import AttachmentUploadedSelectMenu
from ..utils import trans


class AttachmentsUploaded:
    def __init__(self, window=None):
        """
        Attachments Uplaoded UI

        :param window: Window instance
        """
        self.window = window

    def setup(self):
        """
        Setup list

        :return: QVBoxLayout
        :rtype: QVBoxLayout
        """

        self.setup_attachments()

        self.window.ui.nodes['attachments_uploaded.sync.tip'] = QLabel(trans('attachments_uploaded.sync.tip'))
        self.window.ui.nodes['attachments_uploaded.sync.tip'].setAlignment(Qt.AlignCenter)
        empty_widget = QWidget()

        # buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.window.ui.nodes['attachments_uploaded.btn.sync'])
        buttons_layout.addWidget(self.window.ui.nodes['attachments_uploaded.btn.clear'])
        buttons_layout.addWidget(empty_widget)
        buttons_layout.addWidget(self.window.ui.nodes['attachments_uploaded.sync.tip'])

        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.window.ui.nodes['attachments_uploaded'])
        layout.addLayout(buttons_layout)

        return layout

    def setup_attachments(self):
        """
        Setup attachments uploaded list
        """
        id = 'attachments_uploaded'

        # attachments
        self.window.ui.nodes[id] = AttachmentUploadedSelectMenu(self.window)

        # buttons
        self.window.ui.nodes['attachments_uploaded.btn.sync'] = QPushButton(trans('attachments_uploaded.btn.sync'))
        self.window.ui.nodes['attachments_uploaded.btn.clear'] = QPushButton(trans('attachments_uploaded.btn.clear'))

        self.window.ui.nodes['attachments_uploaded.btn.sync'].clicked.connect(
            lambda: self.window.controller.assistant_files.sync_files())
        self.window.ui.nodes['attachments_uploaded.btn.clear'].clicked.connect(
            lambda: self.window.controller.assistant_files.clear_files())

        self.window.ui.models[id] = self.create_model(self.window)
        self.window.ui.nodes[id].setModel(self.window.ui.models[id])

    def create_model(self, parent):
        """
        Create list model

        :param parent: parent widget
        :return: QStandardItemModel
        :rtype: QStandardItemModel
        """
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(0, Qt.Horizontal, trans('attachments.header.name'))
        model.setHeaderData(1, Qt.Horizontal, trans('attachments.header.path'))
        return model

    def update_list(self, id, data):
        """
        Update list

        :param id: ID of the list
        :param data: Data to update
        """
        self.window.ui.models[id].removeRows(0, self.window.ui.models[id].rowCount())
        i = 0
        for uuid in data:
            if 'name' not in data[uuid]:
                continue
            self.window.ui.models[id].insertRow(i)
            self.window.ui.models[id].setData(self.window.ui.models[id].index(i, 0), data[uuid]['name'])
            self.window.ui.models[id].setData(self.window.ui.models[id].index(i, 1), data[uuid]['path'])
            i += 1
