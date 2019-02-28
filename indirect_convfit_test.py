from __future__ import print_function
import unittest

from mantid import mtd

from indirect_base import TestIDAFit
from utils import *


class TestConvFit(unittest.TestCase, TestIDAFit):

    def __init__(self):
        unittest.TestCase.__init__(self)
        TestIDAFit.__init__(self, tab_index=4, tab_name='tabConvFit')

    def test_stuff(self):
        self.set_single_input_sample('irs26173_graphite002_red.nxs')
        self.set_single_input_resolution('irs26173_graphite002_res.nxs')
        wait_for(lambda: mtd.doesExist('irs26173_graphite002_res'))
        wait(1)
        self.set_function('composite=Convolution;name=Resolution,Workspace="irs26173_graphite002_res";'
                          'name=Lorentzian,FWHM=0.01')
        wait_for(lambda: self.get_number_datasets() == 10)
        self.assertEqual(self.get_number_datasets(), 10)
        self.set_start_x(-0.2)
        self.set_end_x(0.2)
        wait(1)
        self.fit_single()
        wait_for(lambda: mtd.doesExist('irs26173_graphite002_conv__s0_Workspaces'), timeout=2)
        self.assertTrue(mtd.doesExist('irs26173_graphite002_conv__s0_Workspaces'))
        self.run_button.setText('Hello')
        wait(1)
        self.run_fit()
