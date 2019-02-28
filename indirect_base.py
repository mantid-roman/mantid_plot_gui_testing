from __future__ import print_function
from qtpy.QtWidgets import QPushButton

from mantid import mtd

from base import TestBase
from utils import *


class TestIDAFit(TestBase):

    def __init__(self, tab_index, tab_name='tabIqtFit'):
        self.app_window = self.create_widget()
        mfit_action = self.app_window.findChildren(QAction, 'Data Analysis')[-1]
        mfit_action.trigger()
        self.ida = get_child(self.app_window, 'Data Analysis')
        self.ida_tab_widget = get_child(self.ida, 'twIDATabs')
        change_current_tab(self.ida_tab_widget, tab_index)
        self.tab_widget = get_child(self.ida_tab_widget, tab_name)
        self.fit_browser = get_child(self.tab_widget, 'fitPropertyBrowser')
        # print(self.fit_browser)
        self.data_view = get_child(self.tab_widget, 'fitDataView')
        self.single_input = get_child(self.data_view, 'loSingleInput')
        self.sample_input = get_child(get_child(self.single_input, 'dsSample'), 'rfFileInput')
        self.resolution_input = get_child(get_child(self.single_input, 'dsResolution'), 'rfFileInput')
        self.start_x = get_child(self.single_input, 'dsbStartX')
        self.end_x = get_child(self.single_input, 'dsbEndX')
        self.run_button = get_child(self.tab_widget, 'pbRun', QPushButton)
        self.fit_single_button = get_child(self.tab_widget, 'pbFitSingle', QPushButton)
        self.plot_spec_index = get_child(self.tab_widget, 'spPlotSpectrum')
        self.plot_current_preview = get_child(self.tab_widget, 'pbPlotPreview')

    def finish(self):
        invoke(self.ida.parent(), 'close')
        self.ida = None
        wait()
        mtd.clear()
        wait(0.1)

    def set_function(self, fun):
        QMetaObject.invokeMethod(self.fit_browser, 'setFunction', Qt.QueuedConnection, Q_ARG('QString', fun))

    def get_number_datasets(self):
        return QMetaObject.invokeMethod(self.fit_browser, 'getNumberOfDatasets', Qt.DirectConnection,
                                        Q_RETURN_ARG('int'))

    def get_single_function_str(self):
        return QMetaObject.invokeMethod(self.fit_browser, 'getSingleFunctionStr', Qt.DirectConnection,
                                        Q_RETURN_ARG('QString'))

    def get_single_function(self):
        return create_function(self.get_single_function_str())

    def set_single_input_sample(self, path):
        QMetaObject.invokeMethod(self.sample_input, 'setFileTextWithSearch', Qt.QueuedConnection, Q_ARG('QString', path))

    def set_single_input_resolution(self, path):
        QMetaObject.invokeMethod(self.resolution_input, 'setFileTextWithSearch', Qt.QueuedConnection, Q_ARG('QString', path))

    def plot_spectrum(self, index):
        QMetaObject.invokeMethod(self.plot_spec_index, 'setValue', Qt.QueuedConnection, Q_ARG('int', index))

    def set_start_x(self, value):
        QMetaObject.invokeMethod(self.start_x, 'setValue', Qt.QueuedConnection, Q_ARG('double', value))

    def set_end_x(self, value):
        QMetaObject.invokeMethod(self.end_x, 'setValue', Qt.QueuedConnection, Q_ARG('double', value))

    def fit_single(self):
        click_button(self.fit_single_button)

    def run_fit(self):
        click_button(self.run_button)
