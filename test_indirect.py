from __future__ import print_function
import inspect
import unittest
from mantidqt.utils.qt.test.gui_window_test import GuiTestBase, is_test_method
# local imports
from testrunner import run_test
from utils import *
import _qti


def test():

    class TestIqtFit(GuiTestBase):

        def runTest(self, method=None):
            for test in inspect.getmembers(self, is_test_method):
                name = test[0]
                if method is None or method == name:
                    self.run_test(method=name, close_on_finish=False)

        def create_widget(self):
            aw = _qti.app
            return aw

        def start_iqt_fit(self):
            self.app_window = self.create_widget()
            mfit_action = self.app_window.findChildren(QAction, 'Data Analysis')[-1]
            mfit_action.trigger()
            self.ida = get_child(self.app_window, 'Data Analysis')
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
            # self.file_input.setFileTextWithSearch(path)
            QMetaObject.invokeMethod(self.file_input, 'setFileTextWithSearch', Qt.QueuedConnection, Q_ARG('QString', path))

    class TestFitPropertyBrowser(unittest.TestCase, TestIqtFit):

        def test_stuff(self):
            yield self.start_iqt_fit()
            self.set_function('name=LinearBackground')
            self.set_single_input('iris26176_graphite002_iqt.nxs')
            self.assertTrue(True)
            # self.ida.parent().close()

    # run_test(TestFitPropertyBrowser, method='all')
    TestFitPropertyBrowser().run_test(method='test_stuff', close_on_finish=False)

threadsafe_call(test)
