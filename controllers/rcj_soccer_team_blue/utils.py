

import math 
import time

NEUTRAL_SPOTS =[
 [0, 0,0,-0.1],
 [-0.3, -0.3,-0.4,-0.4],
 [0, -0.2,0,-0.4],
 [0.3, -0.3,0.4,-0.4],
 [0.3, 0.3,0.4,0.3],
 [0, 0.2,0,0],
 [-0.3, 0.3,-0.4,0.2],
]
# this able robots to cummunicate
def definitions(robot):
    """
    heading=0

    xr=0
    yr=0

    xb=0
    yb=0

    is_ball=False

    lxb=0
    lyb=0

    ball_stop_time = 0

    last_time = time.time()

    nearest_ns = [0,0,0,0]

    ball_distance =0

    robot_poses  =[[0,0,0],[0,0,0],[0,0,0]]
    
    nearest_to_ball = False


    """
    robot.heading=0

    robot.xr=0
    robot.yr=0

    robot.xb=0
    robot.yb=0

    robot.is_ball=False

    robot.lxb=0
    robot.lyb=0

    robot.ball_stop_time = 0
    robot.last_time = time.time()
    robot.nearest_ns = [0,0,0,0]
    robot.ball_distance =0
    robot.robot_poses  =[[0,0,0],[0,0,0],[0,0,0]]
    robot.nearest_to_ball = False

def move_to (robot,x,y,s=False):
    """
    move to somewhere
    """
#  head angle
    heading = math.degrees(robot.get_compass_heading())

# difference angle of head and ball 
    a = math.degrees(math.atan2((robot.xr-x),(robot.yr-y)))
    #e =>  how much the robot must rotate to face the target.
    e= heading + a



    # if you find it hard to understand , un-commnet these codes
    # print("h:",heading)
    # print('a:',a)
    # print('e:',e)
  
    if e > 180: e -= 360
    if e < -180: e += 360


    if e> -90 and e < 90 :
        right_speed =10+e*0.3
        left_speed = 10-e*0.3
    else:
        if e> 0 :e -=180
        else: e += 180
        right_speed =-10+e*0.3
        left_speed = -10-e*0.3

    if right_speed > 10 : right_speed = 10    
    if right_speed < -10 : right_speed = -10
    if left_speed > 10 : left_speed = 10
    if left_speed < -10 : left_speed = -10

    if abs(robot.xr-x) < 0.01 and abs(robot.yr-y) < 0.01 and s :
        stop(robot)
    else:
            
        robot.right_motor.setVelocity(right_speed)
        robot.left_motor.setVelocity(left_speed)

def stop(robot):
    """
    robot.right_motor.setVelocity(0)
    <br>
    <br>
    robot.left_motor.setVelocity(0)

    
    """
    robot.right_motor.setVelocity(0)
    robot.left_motor.setVelocity(0)

def readData(robot):
    """
    <h2>this function is for robots communication.</h2>
    <br>
    <mark>To notfy all robots whenever the ball is detected by any robot.</mark>
    """
    # robot exact location
    gps =robot.get_gps_coordinates()

    robot.heading = math.degrees(robot.get_compass_heading())

    robot.xr = gps[0]
    robot.yr = gps[1]

    # reverse the x and y axis for yellow team
    if robot.team =="Y":
        robot.xr *= -1
        robot.yr *= -1


    # update ball location if detected or keep the last data if it wasnt detected  
    if robot.is_new_ball_data():

        ball_data = robot.get_new_ball_data()
        
        ball_angle = math.degrees(  math.atan2(ball_data["direction"][1]  ,   ball_data["direction"][0]) )

        robot.ball_distance= abs(                      0.01666666   /  
                                     (    abs(ball_data["direction"][2]) / math.sqrt(1-ball_data["direction"][2]**2)    )  
                                )


        # FINDING BALL LOCATION  (X,Y) 
        robot.xb = math.sin(math.radians(ball_angle+robot.heading))*robot.ball_distance +robot.xr
        robot.yb = -math.cos(math.radians(ball_angle+robot.heading))*robot.ball_distance +robot.yr
        
        robot.is_ball =True
    else:
        robot.is_ball =False
    # send last data 
    robot.send_data_to_team({
        'is_ball':robot.is_ball,
        'xr':robot.xr,
        'yr':robot.yr,
        'xb':robot.xb,
        'yb':robot.yb,
        'ball_dis' :robot.ball_distance,
        'id':robot.player_id
    })
        
    # To update robot ball location from team data
    while robot.is_new_team_data():

        # print(robot.get_new_team_data())    //==>  {'robot_id': {'is_ball': True, 'xr': -0.25333272879690055, 'yr': 0.26441205057572287, 'xb': -0.14169967192514168, 'yb': 0.14789680353410498, 'id': 2}}

        team_data = robot.get_new_team_data()['robot_id']

        if not robot.is_ball and team_data["is_ball"]:
            robot.is_ball =True
            robot.xb = team_data["xb"]
            robot.yb = team_data["yb"]
            robot.ball_distance = math.sqrt((robot.xb-robot.xr)**2+(robot.yb-robot.yr)**2)


        robot.robot_poses[team_data["id"]-1] = [team_data["xr"],team_data["yr"],team_data["ball_dis"]]
    
    # update robot location based on himself if he didnt have team data
    robot.robot_poses[robot.player_id-1] = [robot.xr,robot.yr,robot.ball_distance]



    # finding nearest robot
    min_distance = robot.robot_poses[0][2]
    index = 0 
    for i in range(3):
        if robot.robot_poses[i][2] < min_distance:
            min_distance =robot.robot_poses[i][2]
            index =i
    if robot.player_id == index+1 :
        robot.nearest_to_ball = True
        # print(robot.player_id)
    else:
        robot.nearest_to_ball = False





    #  computing ball stop duration
    if time.time() - robot.last_time >1 :
        v = math.sqrt((robot.xb-robot.lxb)**2+(robot.yb-robot.lyb)**2)
        if v <0.1:
            robot.ball_stop_time +=1
        else:
            robot.ball_stop_time =0

        robot.last_time =time.time()

        robot.lxb = robot.xb
        robot.lyb = robot.yb



    # setting nearest neutral spot
    m = math.sqrt((NEUTRAL_SPOTS[0][0] -robot.xb)**2+(NEUTRAL_SPOTS[0][1]-robot.yb)**2)
    robot.nearest_ns = NEUTRAL_SPOTS[0]
    for pos in NEUTRAL_SPOTS:
        d =math.sqrt((pos[0]-robot.xb)**2+(pos[1]-robot.yb)**2) 
        if d <m :
            m=d
            robot.nearest_ns = pos