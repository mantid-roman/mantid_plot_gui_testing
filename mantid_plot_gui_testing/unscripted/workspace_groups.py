from __future__ import print_function, unicode_literals
# import unittest

from mantid.simpleapi import CreateSampleWorkspace, GroupWorkspaces, RenameWorkspace
from mantid import mtd
from mantid_plot_gui_testing.utils import *


def test_simple():
    ws1 = CreateSampleWorkspace()
    ws2 = CreateSampleWorkspace()
    ws3 = CreateSampleWorkspace()
    # Create a group workpace
    wsList = [ws1,ws2,ws3]
    wsGroup = GroupWorkspaces(wsList)
    # or
    wsGroup1 = GroupWorkspaces("ws1,ws2,ws3")


def test_rename_crash():
    ws = CreateSampleWorkspace()
    ws_group = GroupWorkspaces([ws])
    RenameWorkspace(ws_group, 'ws')
    print(mtd.size())
    print(mtd['ws'])
    sorts = get_children_with_text(app_window, 'Sort')[0]
    click_button(sorts)


def test_rename():
    ws = CreateSampleWorkspace()
    ws_group = GroupWorkspaces([ws])
    RenameWorkspace(ws, 'ws_group')
    print(mtd.size())
    print(mtd['ws_group'])


def test_replace():
    from qtpy.QtCore import QTimer
    ws1 = CreateSampleWorkspace()
    ws2 = CreateSampleWorkspace()
    ws3 = CreateSampleWorkspace()
    wsGroup = GroupWorkspaces([ws1, ws2, ws3])

    def stuff():
        ws1 = CreateSampleWorkspace()

    t1 = QTimer()
    t1.timeout.connect(stuff)
    t1.start(1000)
    while True:
        qapp.processEvents()


def test_stuff():
    wss = []
    for i in range(300):
        name = 'ws_{}'.format(i)
        wss.append(CreateSampleWorkspace(OutputWorkspace=name))
    ws_group = GroupWorkspaces(wss)


test_stuff()
