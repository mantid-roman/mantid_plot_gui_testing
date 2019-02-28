from __future__ import print_function
import unittest

from mantid import mtd

from indirect_base import TestIDAFit
from utils import *


class TestIqtFit(unittest.TestCase, TestIDAFit):

    def __init__(self):
        unittest.TestCase.__init__(self)
        TestIDAFit.__init__(self, tab_index=3, tab_name='tabIqtFit')

    def test_stuff(self):
        self.set_function('name=LinearBackground;name=ExpDecay')
        self.set_single_input_sample('iris26176_graphite002_iqt.nxs')
        wait_for(lambda: self.get_number_datasets() == 17)
        self.set_end_x(0.2)

    def test_single_fit(self):
        self.set_function('name=LinearBackground;name=ExpDecay')
        self.set_single_input_sample('iris26176_graphite002_iqt.nxs')
        wait_for(lambda: self.get_number_datasets() == 17)
        self.set_end_x(0.2)
        self.fit_single()
        wait_for(lambda: mtd.doesExist('iris26176_graphite002_iqtFit__s0_Workspaces'), timeout=10)
        self.assertTrue(mtd.doesExist('iris26176_graphite002_iqtFit__s0_Parameters'))
        self.assertTrue(mtd.doesExist('iris26176_graphite002_iqtFit__s0_Workspaces'))
        self.assertTrue(mtd.doesExist('iris26176_graphite002_iqtFit__s0'))
        wait(1)
        f = self.get_single_function()
        self.assertAlmostEqual(f[0].A0, -0.014, 3)
        self.assertAlmostEqual(f[0].A1, 0.211, 3)
        self.assertAlmostEqual(f[1].Height, 0.782, 3)
        self.assertAlmostEqual(f[1].Lifetime, 0.039, 3)

    def test_single_fit_another_spectrum(self):
        self.set_function('name=LinearBackground;name=ExpDecay')
        self.set_single_input_sample('iris26176_graphite002_iqt.nxs')
        wait_for(lambda: self.get_number_datasets() == 17)
        self.set_end_x(0.06)
        self.plot_spectrum(3)
        self.fit_single()
        wait_for(lambda: mtd.doesExist('iris26176_graphite002_iqtFit__s3_Workspaces'), timeout=2)
        self.assertTrue(mtd.doesExist('iris26176_graphite002_iqtFit__s3_Parameters'))
        self.assertTrue(mtd.doesExist('iris26176_graphite002_iqtFit__s3_Workspaces'))
        self.assertTrue(mtd.doesExist('iris26176_graphite002_iqtFit__s3'))
        wait(1)
        f = self.get_single_function()
        self.assertAlmostEqual(f[0].A0, 0.043, 3)
        self.assertAlmostEqual(f[0].A1, -0.35495, 3)
        self.assertAlmostEqual(f[1].Height, 0.878448, 3)
        self.assertAlmostEqual(f[1].Lifetime, 0.010, 3)

    def test_plot_current_preview(self):
        self.set_function('name=LinearBackground;name=ExpDecay')
        self.set_single_input_sample('iris26176_graphite002_iqt.nxs')
        wait_for(lambda: self.get_number_datasets() == 17)
        self.set_end_x(0.2)
        self.fit_single()
        wait_for(lambda: mtd.doesExist('iris26176_graphite002_iqtFit__s0_Workspaces'), timeout=10)
        click_button(self.plot_current_preview)
