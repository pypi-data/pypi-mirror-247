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
import json
import os

from PySide6.QtGui import QAction

from ..utils import trans


class Theme:
    def __init__(self, window=None):
        """
        Theme controller

        :param window: Window instance
        """
        self.window = window
        self.css = {}

    def load_css(self):
        """Load CSS"""
        path = os.path.join(self.window.config.get_root_path(), 'data', 'css', 'highlighter.json')
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    self.css['highlighter'] = json.load(f)
                    f.close()
            except Exception as e:
                print(e)

    def get_css(self, name):
        """
        Return CSS rules

        :param name: css name
        :return: css rules
        :rtype: dict
        """
        if name in self.css:
            return self.css[name]
        return {}

    def toggle(self, name):
        """
        Toggle theme

        :param name: theme name
        """
        self.window.config.set('theme', name)
        self.window.config.save()
        self.apply()
        self.window.set_theme(name + '.xml', 'style.css')  # style.css = additional custom stylesheet
        self.update()

    def apply(self):
        """Apply theme"""
        # windows
        self.window.data['output'].setStyleSheet(self.get_style('chat_output'))
        self.window.data['input'].setStyleSheet(self.get_style('chat_input'))
        self.window.data['ctx.contexts'].setStyleSheet(self.get_style('ctx.contexts'))
        # notepads
        self.window.data['notepad1'].setStyleSheet(self.get_style('chat_output'))
        self.window.data['notepad2'].setStyleSheet(self.get_style('chat_output'))
        self.window.data['notepad3'].setStyleSheet(self.get_style('chat_output'))
        self.window.data['notepad4'].setStyleSheet(self.get_style('chat_output'))
        self.window.data['notepad5'].setStyleSheet(self.get_style('chat_output'))

        # apply to syntax highlighter
        self.apply_syntax_highlighter(self.window.config.get('theme'))

    def get_style(self, element):
        """
        Return style for element

        :param element: element name
        :return: style for element
        :rtype: str
        """
        # get theme element style
        if  element == "chat_output":
            return 'font-size: {}px;'.format(self.window.config.get('font_size'))
        elif element == "chat_input":
            return 'font-size: {}px;'.format(self.window.config.get('font_size.input'))
        elif element == "ctx.contexts":
            return 'font-size: {}px;'.format(self.window.config.get('font_size.ctx'))
        elif element == "text_bold":
            return "font-weight: bold;"
        elif element == "text_small":
            return "font-size: 9px;"
        elif element == "text_faded":
            return "font-size: 9px; color: #999;"

    def apply_syntax_highlighter(self, theme):
        """Apply syntax highlight"""
        self.window.data['output_highlighter'].setTheme(self.get_css('highlighter'))

    def update(self):
        """Update theme menu"""
        for theme in self.window.menu['theme']:
            self.window.menu['theme'][theme].setChecked(False)
        current = self.window.config.get('theme')
        if current in self.window.menu['theme']:
            self.window.menu['theme'][current].setChecked(True)

    def get_themes_list(self):
        """
        Return list of themes

        :return: list of themes
        :rtype: list
        """
        return ['dark_amber',
                'dark_blue',
                'dark_cyan',
                'dark_lightgreen',
                'dark_pink',
                'dark_purple',
                'dark_red',
                'dark_teal',
                'dark_yellow',
                # 'light_amber',
                # 'light_blue',
                # 'light_cyan',
                # 'light_cyan_500',
                # 'light_lightgreen',
                # 'light_pink',
                # 'light_purple',
                # 'light_red',
                # 'light_teal',
                # 'light_yellow'
        ]

    def trans_theme(self, theme):
        """
        Translate theme name

        :param theme: theme name
        :return: translated theme name
        :rtype: str
        """
        return theme.replace('_', ' ').title().replace('Dark ', trans('theme.dark') + ': ').replace('Light ', trans(
            'theme.light') + ': ')

    def setup(self):
        """Setup theme"""
        # load css files
        self.load_css()

        # setup menu
        themes = self.get_themes_list()
        for theme in themes:
            name = self.trans_theme(theme)
            self.window.menu['theme'][theme] = QAction(name, self.window, checkable=True)
            self.window.menu['theme'][theme].triggered.connect(
                lambda checked=None, theme=theme: self.window.controller.theme.toggle(theme))
            self.window.menu['menu.theme'].addAction(self.window.menu['theme'][theme])

        # apply theme
        theme = self.window.config.get('theme')
        self.toggle(theme)

    def reload(self):
        """Reload theme"""
        theme = self.window.config.get('theme')
        self.toggle(theme)
