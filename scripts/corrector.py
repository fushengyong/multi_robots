#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import *
from multi_robots.msg import *

def getTheta( q ):
    t = math.atan2( 2*(q.w*q.z+q.y*q.x) , 1-2*(q.y**2+q.z**2) )
    return t

def getX( x ):
    A1 = 0.065087
    A2 = 0.000243
    A3 = 0.019206
    error = A3*(x**3)+A2*(x**2)+A1*(x)
    return x-error

def getY( y ):

    A1 = 0.043623
    A2 = 0.001636
    error = A2*(y**2)+A1*(y)
    return y-error

def callback(data):
    pub = rospy.Publisher('robot_pose', RobotPose, queue_size=10)
    for i in data.markers:
        p = i.pose.pose.position
        q = i.pose.pose.orientation
        pose = Pose2D( getX( p.x ), getY( p.y ), getTheta( q ) )
        pub.publish( RobotPose( i.id, pose, rospy.Time.now() ) )

def corrector():

    rospy.init_node('corrector', anonymous=False)
    rospy.Subscriber( 'ar_pose_marker', AlvarMarkers, callback )
    rospy.spin()

if __name__ == '__main__':
    try:
        corrector()
    except rospy.ROSInterruptException:
        pass