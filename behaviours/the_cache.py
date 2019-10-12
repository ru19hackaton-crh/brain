#!/usr/bin/env python3

import py_trees
from py_trees.common import Status

import json

def colour_is_whitish(colour):
    return abs(colour - 20) < 5

def colour_is_yellow(colour):
    return abs(colour - 14) < 2

class FindTheLineBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Find The Line"):
        super().__init__(name)
        self.blackboard.register_key("colour", read=True)
        self.previous_command_sent = None

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        if self.blackboard.colour and colour_is_whitish(self.blackboard.colour):
            new_command = "STOP"
            self.brain.robot.write_message(f"COMMAND: {new_command}")
            return Status.SUCCESS
        else:
            new_command = "DRIVE:[\"up\"]"
            if new_command != self.previous_command_sent:
                self.previous_command_sent = new_command
                self.brain.robot.write_message(f"COMMAND: {new_command}")
            return Status.RUNNING

    def terminate(self, new_status):
        self.previous_command_sent = None
        pass

class FollowTheLine1Behaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Follow The Line 1"):
        super().__init__(name)
        self.blackboard.register_key("colour", read=True)
        self.previous_command_sent = None
        self.previous_direction = None
        self.iters = 0

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        if self.blackboard.colour:
            if colour_is_yellow(self.blackboard.colour):
                self.brain.robot.write_message(f"COMMAND: STOP")
                return Status.SUCCESS
            elif colour_is_whitish(self.blackboard.colour):
                direction = "right"
            else:
                direction = "left"
            if self.previous_direction == direction:
                self.iters += 1
            else:
                self.previous_direction = direction
                self.iters = 0

            if self.iters > 180:
                new_command = f"TURN:{direction}"
            else:
                new_command = f"LINE:{direction}"

            if self.previous_command_sent != new_command:
                self.previous_command_sent = new_command
                self.brain.robot.write_message(f"COMMAND: {new_command}")
                self.brain.monitor.write_message(f"ROBOT:{new_command}")
            return Status.RUNNING
        return Status.FAILURE

    def terminate(self, new_status):
        pass

class YellowButtonForwardBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Never gonna give you up"):
        super().__init__(name)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        return Status.RUNNING

    def terminate(self, new_status):
        pass

class YellowButtonTurnAroundBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Never gonna run around and desert you"):
        super().__init__(name)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        return Status.RUNNING

    def terminate(self, new_status):
        pass

class YellowButtonBackToWhiteBehaviour(py_trees.behaviour.Behaviour):
    def __init__(self, name="Never gonna tell a lie and hurt you"):
        super().__init__(name)

    def setup(self, timeout, brain=None):
        if brain:
            self.brain = brain
        return True

    def update(self):
        return Status.RUNNING

    def terminate(self, new_status):
        pass

def create_yellow_button_subtree(brain):
    yellow_button = py_trees.composites.Sequence("Yellow Button")
    go_forward = YellowButtonForwardBehaviour()
    go_forward.setup(0, brain)
    turn_around = YellowButtonTurnAroundBehaviour()
    turn_around.setup(0, brain)
    white_line = YellowButtonBackToWhiteBehaviour()
    white_line.setup(0, brain)
    yellow_button.add_children([go_forward, turn_around, white_line])
    return yellow_button

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
    yellow_button = create_yellow_button_subtree(brain)
    follow_the_line2 = FollowTheLine2Behaviour()
    follow_the_line2.setup(0, brain)
    the_cache.add_children([find_the_line, follow_the_line1, yellow_button, follow_the_line2])
    return the_cache
