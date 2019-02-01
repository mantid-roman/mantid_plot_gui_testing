from __future__ import print_function

import sys
from qtpy.QtWidgets import (QApplication, QDockWidget, QMenu, QAction, QWidget, QPushButton, QCheckBox, QMainWindow,
                            QTabWidget)
from qtpy.QtCore import Qt, QMetaObject, QObject, Q_ARG
from qtpy.QtTest import QTest
from qtpy.QtGui import QClipboard
from mantid.simpleapi import Load
# sys.path.append(r'D:\Work\mantid\qt\python')

from mantidqt.utils.qt.test.gui_window_test import GuiTestBase
import _qti


def discover_children(widget, child_type=QWidget):
    print('Children widgets of ', widget.objectName(), type(widget))
    for w in widget.findChildren(child_type):
        print(w, w.objectName())


def get_child(widget, name, child_type=QWidget):
    children = widget.findChildren(child_type, name)
    if len(children) == 0:
        raise RuntimeError("Widget doesn't have child with name {}".format(name))
    if len(children) > 1:
        print('Widget has more than 1 child with name {}'.format(name))
    return children[0]


def find_action_with_text(widget, text):
    for a in widget.findChildren(QAction):
        # print(a, a.text(), a.objectName())
        if a.text() == text:
            return a


def print_children(widget, child_type=QWidget, indent=0):
    if indent == 0:
        print('Children of {} {}'.format(widget.objectName(), type(widget)))
    space = ' ' * indent
    for c in widget.children():
        if isinstance(c, child_type):
            print('{0}{1} {2}'.format(space, type(c), c.objectName()))
            print_children(c, child_type, indent + 4)


def click_button(btn):
    QMetaObject.invokeMethod(btn, 'click', Qt.QueuedConnection)


def trigger_action(action):
    QMetaObject.invokeMethod(action, 'trigger', Qt.QueuedConnection)


def change_current_tab(tab_widget, index):
    if not isinstance(tab_widget, QTabWidget):
        raise RuntimeError('Widget must be a QTabWidget, found {t}, {n}'.format(t=type(tab_widget),
                                                                                n=tab_widget.objectName()))
    QMetaObject.invokeMethod(tab_widget, 'setCurrentIndex', Qt.QueuedConnection, Q_ARG('int', index))


class TestIqtFit(GuiTestBase):

    def create_widget(self):
        aw = _qti.app
        return aw

    def start_iqt_fit(self):
        mfit_action = self.widget.findChildren(QAction, 'Data Analysis')[-1]
        mfit_action.trigger()
        self.ida = get_child(self.widget, 'Data Analysis')
        self.ida_tab_widget = get_child(self.ida, 'twIDATabs')
        change_current_tab(self.ida_tab_widget, 3)
        yield 0.1
        self.iqt_fit = get_child(self.ida_tab_widget, 'tabIqtFit')
        self.fit_browser = get_child(self.iqt_fit, 'fitPropertyBrowser')
        self.data_view = get_child(self.iqt_fit, 'fitDataView')
        self.single_input = get_child(self.data_view, 'loSingleInput')
        self.file_input = get_child(self.single_input, 'rfFileInput')

    def set_function(self, fun):
        QMetaObject.invokeMethod(self.fit_browser, 'setFunction', Q_ARG('QString', fun))

    def set_single_input(self, path):
        self.file_input.setFileTextWithSearch(path)


def test():

    class TestFitPropertyBrowser(TestIqtFit):

        def call(self):
            yield self.start_iqt_fit()
            self.set_function('name=LinearBackground')
            self.set_single_input('iris26176_graphite002_iqt.nxs')

    TestFitPropertyBrowser().run_test(close_on_finish=False)


threadsafe_call(test)
