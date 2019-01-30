from __future__ import print_function

import sys
from qtpy.QtWidgets import QApplication, QDockWidget, QMenu, QAction, QWidget, QPushButton, QCheckBox
from qtpy.QtCore import Qt, QMetaObject
from qtpy.QtTest import QTest
from qtpy.QtGui import QClipboard
from mantid.simpleapi import Load

sys.path.append(r'D:\Work\mantid\qt\python')


def find_action_with_text(widget, text):
    for a in widget.findChildren(QAction):
        # print(a, a.text(), a.objectName())
        if a.text() == text:
            return a


def click_button(btn):
    QMetaObject.invokeMethod(btn, 'click', Qt.QueuedConnection)


def trigger_action(action):
    QMetaObject.invokeMethod(action, 'trigger', Qt.QueuedConnection)


def test():
    import _qti
    qapp = QApplication.instance()
    from mantidqt.utils.qt.test.gui_window_test import GuiTestBase
    class TestFitPropertyBrowser(GuiTestBase):

        def create_widget(self):
            aw = _qti.app
            return aw

        def call(self):
            Load(r'D:\Work\mantid_stuff\Issues\24207-multifit-crash\irs26176_graphite002_iqt.nxs', OutputWorkspace='ws')
            print(self.widget)
            mfit_action = self.widget.findChildren(QAction, 'Multi dataset fitting')[-1]
            mfit_action.trigger()
            ##yield
            mdf = self.widget.findChildren(QWidget, 'Multi-dataset fitting')[0]

            set_fun_action = find_action_with_text(mdf, 'Copy from clipboard')
            qapp.clipboard().setText('name=FlatBackground,A0=0;name=StretchExp,Height=1,Lifetime=0.01,Stretching=1')
            trigger_action(set_fun_action)
            yield 1

            btnAddWorkspace = mdf.findChildren(QPushButton, 'btnAddWorkspace')[0]
            click_button(btnAddWorkspace)
            yield self.wait_for_modal()
            dlg = self.get_active_modal_widget()
            cbAllSpectra = dlg.findChildren(QCheckBox, 'cbAllSpectra')[0]
            cbAllSpectra.setCheckState(Qt.Checked)
            dlg.accept()

    TestFitPropertyBrowser().run_test(close_on_finish=False)


threadsafe_call(test)
