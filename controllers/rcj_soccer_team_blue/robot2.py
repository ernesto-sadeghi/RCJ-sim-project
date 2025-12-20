# rcj_soccer_player controller - ROBOT B2

# Feel free to import built-in libraries
import math  # noqa: F401

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP


class MyRobot2(RCJSoccerRobot):
    def run(self):
        state=1
        utils.definitions(self)
        while self.robot.step(TIME_STEP) !=-1:
            if self.is_new_data():
                utils.readData(self)

                if self.is_ball:
                    if state == 1:
                        utils.move_to(self,self.xb,self.yb+0.15)
                        if abs(self.xb-self.xr) <0.01 and abs((self.yb+0.15)-self.yr) < 0.05 :
                            state=2
                    elif state ==2:
                        utils.move_to(self,self.xb,self.yb)
                        if abs(self.xb-self.xr) > 0.2 and abs(self.yb-self.yr) > 0.2 :
                            state=2
                else:

                   utils.move_to(self,0.3,0.2,s=True)