#!/usr/bin/env python3

import py_trees
from py_trees.common import Status

from .manual_drive import ManualDriveBehaviour
from .the_cache import create_the_cache_subtree
from .the_calibrator import create_the_calibrator_subtree
from .the_monolith import create_the_monolith_subtree
from .the_root import create_the_root_subtree
from .tricentrifuge import create_tricentrifuge_subtree
from .the_terminal import create_the_terminal_subtree

class StartingBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Started"):
        super().__init__(name)
        self.blackboard.register_key("started", read=True)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        if self.blackboard.started:
            return Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

    def terminate(self, new_status):
        pass

def create_manual_subtree(brain):
    manual = ManualDriveBehaviour()
    manual.setup(0, brain)
    return manual

def create_automation_subtree(brain):
    automation = py_trees.composites.Sequence("Automation")
    starting = StartingBehaviour()
    starting.setup(0, brain)
    the_cache = create_the_cache_subtree(brain)
    the_calibrator = create_the_calibrator_subtree(brain)
    the_monolith = create_the_monolith_subtree(brain)
    the_root = create_the_root_subtree(brain)
    tricentrifuge = create_tricentrifuge_subtree(brain)
    the_terminal = create_the_terminal_subtree(brain)
    automation.add_children([starting, the_cache, the_calibrator, the_monolith, the_root, tricentrifuge, the_terminal])
    return automation

def create_tree(brain):
    root = py_trees.composites.Selector(name="POC root")
    manual = create_manual_subtree(brain)
    automation = create_automation_subtree(brain)
    root.add_children([manual, automation])
    return root
