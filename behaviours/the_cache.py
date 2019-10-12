#!/usr/bin/env python3

import logging

import py_trees
from py_trees.common import Status

import json

class EntryRunBehaviour(py_trees.behaviour.Behaviour):

    def __init__(self, name="Entry Run"):
        super().__init__(name)
        self.blackboard.register_key("robot_response", read=True, write=True)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        if not self.blackboard.robot_response:
            if self.status != Status.RUNNING:
                self.brain.robot.write_message("COMMAND: DRIVE_TO_MAZE")
            return Status.RUNNING
        else:
            return Status.SUCCESS

    def terminate(self, new_status):
        if new_status == Status.SUCCESS:
            self.blackboard.robot_response = False
        self.previous_command_sent = None

class ActivateYellowBehaviour(py_trees.behaviour.Behaviour):

    def __init__(self, name="Yellow finder"):
        super().__init__(name)
        self.blackboard.register_key("robot_response", read=True, write=True)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        return Status.FAILURE

    def terminate(self, new_status):
        pass

class FollowTheLineBehaviour(py_trees.behaviour.Behaviour):

    def __init__(self, name="Line Following"):
        super().__init__(name)
        self.blackboard.register_key("robot_response", read=True, write=True)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        if self.status != Status.RUNNING:
            self.brain.robot.write_message("COMMAND: FOLLOWLINE")
        return Status.RUNNING

    def terminate(self, new_status):
        if new_status == Status.SUCCESS:
            self.brain.robot.write_message("COMMAND: STOPFOLLOWLINE")

def create_the_cache_subtree(brain):
    the_cache = py_trees.composites.Sequence("The Cache")
    entry_run = EntryRunBehaviour()
    entry_run.setup(0, brain)
    entry_run_oneshot = py_trees.decorators.OneShot(entry_run)
    follow_the_line = py_trees.composites.Selector("Follow the line")
    activate_yellow = ActivateYellowBehaviour()
    activate_yellow.setup(0, brain)
    activate_yellow_oneshot = py_trees.decorators.OneShot(activate_yellow)
    the_line = FollowTheLineBehaviour()
    the_line.setup(0, brain)
    follow_the_line.add_children([activate_yellow_oneshot, the_line])
    the_cache.add_children([entry_run_oneshot, follow_the_line])
    return the_cache
