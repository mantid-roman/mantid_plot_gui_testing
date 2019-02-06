from __future__ import print_function
import inspect
from qtpy.QtWidgets import (QAction, QWidget, QTabWidget, QApplication)
from qtpy.QtCore import Qt, QMetaObject, Q_ARG, QTime


qapp = QApplication.instance()


def is_test_method(value):
    if not (inspect.ismethod(value) or inspect.isfunction(value)):
        return False
    return value.__name__.startswith('test_')


def discover_children(widget, child_type=QWidget):
    print('Children widgets of ', widget.objectName(), type(widget))
    for w in widget.findChildren(child_type):
        text = '({})'.format(w.text()) if hasattr(w, 'text') else ''
        print(w, w.objectName(), text)


def get_child(widget, name, child_type=QWidget, timeout=3):
    t = QTime()
    t.start()
    timeout *= 1000
    children = []
    while len(children) == 0 and t.elapsed() < timeout:
        children = widget.findChildren(child_type, name)
        qapp.processEvents()
    if len(children) == 0:
        raise RuntimeError("Widget doesn't have child with name {}".format(name))
    if len(children) > 1:
        print('Widget has more than 1 child with name {}'.format(name))
    return children[0]


def wait_for(seconds=3):
    t = QTime()
    t.start()
    seconds *= 1000
    while t.elapsed() < seconds:
        qapp.processEvents()


def get_active_modal_widget(timeout=3):
    t = QTime()
    t.start()
    timeout *= 1000
    while not QApplication.activeModalWidget() and t.elapsed() < timeout:
        qapp.processEvents()
    return QApplication.activeModalWidget()


def wait_for_active_modal_to_change(modal, timeout=3):
    t = QTime()
    t.start()
    timeout *= 1000
    am = QApplication.activeModalWidget()
    if am is None or modal is None or am != modal:
        return
    while am == modal and t.elapsed() < timeout:
        qapp.processEvents()
        am = QApplication.activeModalWidget()
    if am == modal:
        raise RuntimeError('Action timed out')


def find_action_with_text(widget, text):
    for a in widget.findChildren(QAction):
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
    qapp.processEvents()


def trigger_action(action):
    QMetaObject.invokeMethod(action, 'trigger', Qt.QueuedConnection)
    qapp.processEvents()


def invoke(obj, method):
    QMetaObject.invokeMethod(obj, method, Qt.QueuedConnection)
    qapp.processEvents()


def change_current_tab(tab_widget, index):
    if not isinstance(tab_widget, QTabWidget):
        raise RuntimeError('Widget must be a QTabWidget, found {t}, {n}'.format(t=type(tab_widget),
                                                                                n=tab_widget.objectName()))
    QMetaObject.invokeMethod(tab_widget, 'setCurrentIndex', Qt.QueuedConnection, Q_ARG('int', index))
    qapp.processEvents()


