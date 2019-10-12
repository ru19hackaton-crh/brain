#!/usr/bin/env python3

import py_trees
from py_trees.blackboard import BlackboardClient
from py_trees.common import Status

import logging
from tornado import websocket
import tornado.ioloop
from tornado.log import enable_pretty_logging
enable_pretty_logging()

import json

from behaviours.manual_drive import ManualDriveBehaviour

def create_tree(brain):
    root = py_trees.composites.Selector(name="POC root")
    manual = ManualDriveBehaviour()
    manual.setup(0, brain)
    root.add_children([manual])
    return root

class Brain:
    def __init__(self):
        self._monitor = None
        self._robot = None

        self.tree = create_tree(self)
        self.behaviour_tree = py_trees.trees.BehaviourTree(self.tree)

        self.bb = BlackboardClient(name="Brain", write={"manual", "keys", "robot_response"})
        self.bb.manual = False
        self.bb.keys = set()
        self.bb.robot_response = None

    def operate(self):
        if not self.monitor:
            return
        py_trees.blackboard.Blackboard.enable_activity_stream(maximum_size=100)
        self.behaviour_tree.tick()
        self.monitor.write_message(f"TREE:{py_trees.display.ascii_tree(self.tree, show_status=True)}")
        self.monitor.write_message(f"ACTIVITY:{py_trees.display.unicode_blackboard_activity_stream()}")
        py_trees.blackboard.Blackboard.activity_stream.clear()

    @property
    def monitor(self):
        return self._monitor
    @monitor.setter
    def monitor(self, monitor):
        self._monitor = monitor
        logging.info("new monitor set")

    @property
    def robot(self):
        return self._robot
    @robot.setter
    def robot(self, robot):
        self._robot = robot
        logging.info("new robot set")

    @property
    def manual(self):
        return self.bb.manual
    @manual.setter
    def manual(self, state):
        self.bb.manual = state

    def parse_robot(self, message):
        if message == "DONE":
            self.bb.robot_response = True
        else:
            self.robot.write_message(u"Robot said: %s" % message)

    def parse_monitor(self, message):
        if message == "manual on":
            self.manual = True
        elif message == "manual off":
            self.manual = False
        elif message.endswith("up"):
            key = message.split(" ")[0]
            self.bb.keys.remove(key)
        elif message.endswith("down"):
            key = message.split(" ")[0]
            self.bb.keys.add(key)
        else:
            self.monitor.write_message(f"message: {message}")
        return

class CommonBrainHandler(websocket.WebSocketHandler):

    def initialize(self, brain):
        self.brain = brain

    def check_origin(self, origin):
        return True

    def open(self):
        logging.info("Websocket Opened")

    def on_close(self):
        logging.info("Websocket closed")

class MonitorHandler(CommonBrainHandler):
    def open(self):
        self.brain.monitor = self

    def on_message(self, message):
        self.brain.parse_monitor(message)

class RobotHandler(CommonBrainHandler):
    def open(self):
        self.brain.robot = self

    def on_message(self, message):
        self.brain.parse_robot(message)


if __name__ == "__main__":
    brain = Brain()

    brain_operating = tornado.ioloop.PeriodicCallback(brain.operate, 100)
    application = tornado.web.Application([
        (r"/monitor", MonitorHandler, dict(brain=brain)),
        (r"/robot", RobotHandler, dict(brain=brain)),
        ])
    application.listen(9000)

    brain_operating.start()
    tornado.ioloop.IOLoop.current().start()
