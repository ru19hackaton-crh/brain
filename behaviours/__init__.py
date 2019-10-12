#!/usr/bin/env python3

import py_trees
from py_trees.common import Status

from .manual_drive import ManualDriveBehaviour

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
    automation.add_children([starting])
    return automation

def create_tree(brain):
    root = py_trees.composites.Selector(name="POC root")
    manual = create_manual_subtree(brain)
    automation = create_automation_subtree(brain)
    root.add_children([manual, automation])
    return root
