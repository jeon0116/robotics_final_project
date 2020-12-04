#!/home/pi/.pyenv/versions/rospy3/bin/python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
        self.count = 30

    def lds_callback(self, scan):
       
        print("scan[0]:", scan.ranges[0])
        print("scan[30]:", scan.ranges[30])
        print("scan[330]:", scan.ranges[330])
        turtle_vel = Twist()
         
        if scan.ranges[0] < 0.25 or scan.ranges[30] < 0.20:
            turtle_vel.linear.x = 0.0	
            turtle_vel.angular.z = -1.8
        elif scan.ranges[0] < 0.25 or scan.ranges[330] < 0.20:
            turtle_vel.linear.x = 0.0
            turtle_vel.angular.z = 1.8
        else:
            turtle_vel.linear.x = 0.18	
            turtle_vel.angular.z = 0.0
       
        
        self.publisher.publish(turtle_vel)

def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()
