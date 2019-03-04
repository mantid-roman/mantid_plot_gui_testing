from __future__ import absolute_import, print_function
import inspect
import sys

from qtpy.QtCore import QTime
# local imports
from mantidqt.utils.qt.test.gui_test_runner import open_in_window
from mantidplot import threadsafe_call


class MultiTestRunner(object):

    dots_per_line = 70

    def __init__(self, methods):
        self.methods = methods

    def __call__(self, w):
        time = QTime()
        time.start()
        count = 0
        for method in self.methods:
            yield method
            count += 1
            end = '\n' if count % self.dots_per_line == 0 else ''
            print('.', end=end, file=sys.stderr)
        print('', file=sys.stderr)
        print('-'*self.dots_per_line, file=sys.stderr)
        print('Ran {num} tests in {time}s'.format(num=len(self.methods), time=time.elapsed()*0.001), file=sys.stderr)


class RunTests(object):

    def __init__(self, test_method=None, close_on_finish=True, pause=0):
        self.test_method = test_method
        self.close_on_finish = close_on_finish
        self.pause = pause

    @staticmethod
    def _get_all_tests(selftest_case):
        return inspect.getmembers(selftest_case, lambda x: (inspect.ismethod(x) or inspect.isfunction(x)) and
                                  x.__name__.startswith('test_'))

    def __call__(self, classname):
        def dummy(self):
            pass

        def test():
            classname.runTest = dummy
            test_case = classname()
            if self.test_method is None or self.test_method == 'all':
                test_methods = [test[0] for test in self._get_all_tests(test_case)]
            else:
                test_methods = self.test_method if isinstance(self.test_method, list) else [self.test_method]
            print(test_methods)
            runner = MultiTestRunner([getattr(test_case, name) for name in test_methods])
            try:
                return open_in_window(test_case.create_widget, runner, pause=self.pause,
                                      close_on_finish=self.close_on_finish, attach_debugger=False,
                                      in_workbench=True)
            except:
                return 1
        return threadsafe_call(test)
        # sys.exit(res)


def run_test(classname, method=None, close_on_finish=False, pause=0):
    runner = RunTests(test_method=method, close_on_finish=close_on_finish, pause=pause)
    runner(classname)
