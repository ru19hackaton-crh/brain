#!/usr/bin/env python3

import logging

import py_trees
from py_trees.common import Status

import json

def colour_is_whitish(colour):
    return abs(colour - 20) < 5

def colour_is_yellow(colour):
    return abs(colour - 14) < 2

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


def create_the_cache_subtree(brain):
    the_cache = py_trees.composites.Sequence("The Cache")
    entry_run = EntryRunBehaviour()
    entry_run.setup(0, brain)
    entry_run_oneshot = py_trees.decorators.OneShot(entry_run)
    the_cache.add_children([entry_run_oneshot, ])
    return the_cache
