from __future__ import print_function

import sys
from qtpy.QtWidgets import (QApplication, QDockWidget, QMenu, QAction, QWidget, QPushButton, QCheckBox, QMainWindow,
                            QTabWidget)
from qtpy.QtCore import Qt, QMetaObject, QObject, Q_ARG
from qtpy.QtTest import QTest
from qtpy.QtGui import QClipboard
from mantid.simpleapi import Load
from mantidqt.utils.qt.test.gui_window_test import GuiTestBase
import _qti


sys.path.append(r'D:\Work\mantid\qt\python')


def discover_children(widget, child_type=QWidget):
    print('Children widgets of ', widget.objectName(), type(widget))
    for w in widget.findChildren(child_type):
        print(w, w.objectName())


def get_child(widget, name, child_type=QWidget):
    return widget.findChildren(child_type, name)[0]


def find_action_with_text(widget, text):
    for a in widget.findChildren(QAction):
        # print(a, a.text(), a.objectName())
        if a.text() == text:
            return a


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
        self.ida = self.widget.findChildren(QWidget, 'Data Analysis')[0]
        self.ida_tab_widget = get_child(self.ida, 'twIDATabs')
        change_current_tab(self.ida_tab_widget, 3)
        yield 0.1
        self.iqt_fit = self.ida.findChildren(QWidget, 'tabIqtFit')[0]
        self.fit_browser = get_child(self.iqt_fit, 'fitPropertyBrowser')
        self.data_view = get_child(self.ida, 'fitDataView')
        print(self.data_view)
        change_current_tab(self.data_view, 1)
        print(self.data_view.widget(0).objectName())
        print(self.data_view.widget(1).objectName())
        # QMetaObject.invokeMethod(self.data_view, 'setCurrentWidget', Q_ARG('QWidget', self.data_view.widget(1)))


def test():

    class TestFitPropertyBrowser(TestIqtFit):

        def call(self):
            Load(r'D:\Work\mantid_stuff\Issues\24207-multifit-crash\irs26176_graphite002_iqt.nxs', OutputWorkspace='ws')
            yield self.start_iqt_fit()

    TestFitPropertyBrowser().run_test(close_on_finish=False)


threadsafe_call(test)
