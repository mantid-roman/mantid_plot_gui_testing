from __future__ import print_function
from utils import *
import _qti


class TestBase(object):

    def runTest(self, method=None):
        pass

    @classmethod
    def run_test(cls, test_name, do_finish=False):
        test = cls()
        getattr(test, test_name)()
        if do_finish:
            test.finish()

    @classmethod
    def run_all_tests(cls):
        for test in inspect.getmembers(cls, is_test_method):
            name = test[0]
            cls.run_test(name, do_finish=True)

    def create_widget(self):
        aw = _qti.app
        return aw

