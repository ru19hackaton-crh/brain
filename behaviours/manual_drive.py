#!/usr/bin/env python3

import py_trees
from py_trees.blackboard import BlackboardClient
from py_trees.common import Status

import json

class ManualDriveBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Manual Drive"):
        super().__init__(name)
        self.blackboard.register_key("manual", read=True)
        self.blackboard.register_key("keys", read=True)
        self.previous_command_sent = None

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        if self.blackboard.manual:
            if self.blackboard.keys:
                new_command = f"DRIVE:{json.dumps(list(self.blackboard.keys))}"
            else:
                new_command = "STOP"
            if new_command != self.previous_command_sent:
                self.previous_command_sent = new_command
                self.brain.robot.write_message(f"COMMAND: {new_command}")
            return Status.RUNNING
        elif self.status == Status.RUNNING:
            # inform robot that manual is off
            new_command = "IDLE"
            self.brain.robot.write_message(f"COMMAND: {new_command}")
            return Status.SUCCESS
        else:
            return py_trees.common.Status.INVALID

    def terminate(self, new_status):
        pass
