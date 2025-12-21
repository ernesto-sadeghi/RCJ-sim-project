# rcj_soccer_player controller - ROBOT B3

# Feel free to import built-in libraries
import math  # noqa: F401

# You can also import scripts that you put into the folder with controller
import utils
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP


class MyRobot3(RCJSoccerRobot):
   def run(self):
        state=1
        utils.definitions(self)
        while self.robot.step(TIME_STEP) !=-1:
            if self.is_new_data():
                utils.readData(self)

                if self.is_ball:
                    if self.ball_stop_time >3 and not self.nearest_to_ball:
                        # utils.stop(self)
                        utils.move_to(self,self.nearest_ns[2],self.nearest_ns[3],s=True)
                        state=2
                    elif state == 1:
                        utils.move_to(self,self.xb,self.yb+0.15)
                        if abs(self.xb-self.xr) <0.01 and abs((self.yb+0.15)-self.yr) < 0.05 :
                            state=2
                    elif state ==2:
                        utils.move_to(self,self.xb,self.yb)
                        if abs(self.xb-self.xr) > 0.2 and abs(self.yb-self.yr) > 0.2 :
                            state=2
                else:

                   utils.move_to(self,-0.3,0.2,s=True)
