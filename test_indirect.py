from __future__ import print_function
import unittest
# from qtpy.QtCore import QObject
from qtpy.QtWidgets import QPushButton
from utils import *
import _qti


class TestIqtFit(object):

    def runTest(self, method=None):
        pass
        # for test in inspect.getmembers(self, is_test_method):
        #     name = test[0]
        #     if method is None or method == name:
        #         self.run_test(method=name, close_on_finish=False)

    def create_widget(self):
        aw = _qti.app
        return aw

    def __init__(self):
        self.app_window = self.create_widget()
        mfit_action = self.app_window.findChildren(QAction, 'Data Analysis')[-1]
        mfit_action.trigger()
        self.ida = get_child(self.app_window, 'Data Analysis')
        self.ida_tab_widget = get_child(self.ida, 'twIDATabs')
        change_current_tab(self.ida_tab_widget, 3)
        self.iqt_fit = get_child(self.ida_tab_widget, 'tabIqtFit')
        self.fit_browser = get_child(self.iqt_fit, 'fitPropertyBrowser')
        # print(self.fit_browser)
        self.data_view = get_child(self.iqt_fit, 'fitDataView')
        self.single_input = get_child(self.data_view, 'loSingleInput')
        self.file_input = get_child(self.single_input, 'rfFileInput')
        browse_btn = get_child(self.file_input, 'browseBtn')
        click_button(browse_btn)
        d = get_active_modal_widget()
        print(d)
        discover_children(d, QPushButton)
        QMetaObject.invokeMethod(d, 'close', Qt.QueuedConnection)

    def set_function(self, fun):
        QMetaObject.invokeMethod(self.fit_browser, 'setFunction', Q_ARG('QString', fun))

    def set_single_input(self, path):
        QMetaObject.invokeMethod(self.file_input, 'setFileTextWithSearch', Qt.QueuedConnection, Q_ARG('QString', path))


class TestFitPropertyBrowser(unittest.TestCase, TestIqtFit):

    def __init__(self):
        unittest.TestCase.__init__(self)
        TestIqtFit.__init__(self)

    def test_stuff(self):
        self.set_function('name=LinearBackground;name=ExpDecay')
        self.set_single_input('iris26176_graphite002_iqt.nxs')
        # self.assertTrue(True)
        # self.iam_done = True


test = TestFitPropertyBrowser()
test.test_stuff()
