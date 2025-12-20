# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math  # noqa: F401

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP


class MyRobot1(RCJSoccerRobot):
    """
   <mark>GK</mark>: Goal-Keeper
    """
    def run (self) :
        utils.definitions(self)
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                utils.readData(self)
                if self.is_ball:
                    utils.move_to(self,self.xb,0.55)
                else:
                    utils.move_to(self,0,0.55,s=True)