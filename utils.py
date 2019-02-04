from qtpy.QtWidgets import (QAction, QWidget, QTabWidget)
from qtpy.QtCore import Qt, QMetaObject, Q_ARG


def discover_children(widget, child_type=QWidget):
    print('Children widgets of ', widget.objectName(), type(widget))
    for w in widget.findChildren(child_type):
        print(w, w.objectName())


def get_child(widget, name, child_type=QWidget):
    children = widget.findChildren(child_type, name)
    if len(children) == 0:
        raise RuntimeError("Widget doesn't have child with name {}".format(name))
    if len(children) > 1:
        print('Widget has more than 1 child with name {}'.format(name))
    return children[0]


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


def trigger_action(action):
    QMetaObject.invokeMethod(action, 'trigger', Qt.QueuedConnection)


def change_current_tab(tab_widget, index):
    if not isinstance(tab_widget, QTabWidget):
        raise RuntimeError('Widget must be a QTabWidget, found {t}, {n}'.format(t=type(tab_widget),
                                                                                n=tab_widget.objectName()))
    QMetaObject.invokeMethod(tab_widget, 'setCurrentIndex', Qt.QueuedConnection, Q_ARG('int', index))


