#!/usr/bin/env python3

import py_trees
from py_trees.common import Status

class FindTheLineBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Find The Line"):
        super().__init__(name)
        self.blackboard.register_key("cache_linemet", read=True)
        self.previous_command_sent = None

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        if not self.blackboard.cache_linemet:
            new_command = "DRIVE:[\"up\"]"
            if new_command != self.previous_command_sent:
                self.previous_command_sent = new_command
                self.brain.robot.write_message(f"COMMAND: {new_command}")
            return Status.RUNNING
        else:
            new_command = "STOP"
            self.brain.robot.write_message(f"COMMAND: {new_command}")
            return Status.SUCCESS

    def terminate(self, new_status):
        pass

class FollowTheLine1Behaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Follow The Line 1"):
        super().__init__(name)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        return Status.FAILURE

    def terminate(self, new_status):
        pass

class TakeShortcutBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Take Shortcut"):
        super().__init__(name)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        return Status.FAILURE

    def terminate(self, new_status):
        pass

class FollowTheLine2Behaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Follow The Line 2"):
        super().__init__(name)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        return Status.FAILURE

    def terminate(self, new_status):
        pass

def create_the_cache_subtree(brain):
    the_cache = py_trees.composites.Sequence("The Cache")
    find_the_line = FindTheLineBehaviour()
    find_the_line.setup(0, brain)
    follow_the_line1 = FollowTheLine1Behaviour()
    follow_the_line1.setup(0, brain)
    take_shortcut = TakeShortcutBehaviour()
    take_shortcut.setup(0, brain)
    follow_the_line2 = FollowTheLine2Behaviour()
    follow_the_line2.setup(0, brain)
    the_cache.add_children([find_the_line, follow_the_line1, take_shortcut, follow_the_line2])
    return the_cache
