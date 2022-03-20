import math
from airena.components.ai_base import AiBase
from airena.components import Transform
from airena.typing import IGameObject
from collections import deque


ZIG = math.pi / 4
ZAG = -math.pi / 4
ZIG_BCK = ZIG+(math.pi/2)
ZAG_BCK = ZAG+(-math.pi/2)

class IanBot1(AiBase):

    _do_action = None
    _zig_or_zag = False

    color = (255, 0, 255)
    target = None
    target_position = None
    target_history: deque = None
    dist_to_target = None

    def initialize(self):
        self.target_history = deque()
        self.aquire_target()
        self.set_action(self.act_approach_target)

    def think(self):
        self.track_target()
        self.execute_action()
        self.fire()

    def aquire_target(self):
        if self.target: return
        self.target = self.enemies[0]

    def act_approach_target(self):
        if self.dist_to_target <= 400:
            self.set_action(self.act_engange_target)
        elif not self.has_move_to_target():
            self._zig_or_zag = not self._zig_or_zag
            if self._zig_or_zag:
                self.move_toword_ex(self.rotation+ZIG, 300)
            else:
                self.move_toword_ex(self.rotation+ZAG, 300)

    def act_engange_target(self):
        if self.dist_to_target >= 600:
            self.set_action(self.act_approach_target)
            print("switch")
        elif not self.has_move_to_target():
            self._zig_or_zag = not self._zig_or_zag
            if self._zig_or_zag:
                self.move_toword_ex(self.rotation+ZIG_BCK, 200)
            else:
                self.move_toword_ex(self.rotation+ZAG_BCK, 200)


    def act_dance(self):
        self.move_forward()

    def track_target(self):
        if not self.target.alive:
            self.set_focus(self.facing)
            self.set_action(self.act_dance)
            self.track_target = lambda *a: 1
            self.fire = lambda *a: 1
        else:
            self.target_position = self.target[Transform].position
            self.set_focus(self.target_position)
            self.dist_to_target = self.position.dist(self.target_position)
            self.target_history.appendleft(self.target_position)

        #print(self.target_history)

    def set_action(self, action):
        self._do_action = action

    def execute_action(self):
        if self._do_action:
            self._do_action()
        else:
            print(self.__class__.__name__, ": im dead")
