#!/usr/bin/env python3

# Importing the libraries that we will need

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time

epsilon = 0.2
l_r = rospy.get_param("/l_r")
l_f = rospy.get_param("/l_f")
theta = 0

# Defining the callback function that will get the value of epsi form the turtle

def pose_callback(data):

	global theta
	theta = data.theta


# Main controller code/function	

def go():

	# Initializing the ros node

	global theta, l_r, l_f
	pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
	rospy.init_node('veloctiy', anonymous=True)
	rate = rospy.Rate(10)
	f = 0 
	rospy.Subscriber("/turtle1/pose", Pose, pose_callback)
	print("Controller has been initialized")

	while not rospy.is_shutdown():																				# While loop that last until ros is terminated or Ctrl + c/z is pressed

		# First we get the parameter for our experiment from the user

		vel = Twist()
		speed = float(input('Enter desired speed  '))
		steering = float(input('Enter desired steering angle in degrees ')) * math.pi/180

		if f > 1:																								# For first run it takes these parameters from .yaml file then for the next runs the user inputs them

			l_r = float(input('Enter distance between center of gravity and rear wheel  '))
			l_f = float(input('Enter distance between center of gravity and front wheel  '))

		f = 2
		drive = (input('choose between front (f) steering or rear (r) steering  '))
		t = float(input('Enter in seconds how long you want the turtle to run for '))
		t_end = time.time() + t
		map = steering / t																						# Calculating coefficient of steering decay
		epsi = theta 

		while time.time() < t_end:																				# Loop until time specified runs out
			
			if drive == 'f':																					# For front steering option

				sample_time = t_end - time.time()																# Getting the time left in our trial
				steering = map * sample_time																	# Applying steering decay
				beta = math.atan(l_r  * math.tan(steering) / (l_f + l_r))
				vel_x = speed * math.cos((beta + epsi))															# Vx calculation
				vel_y = speed * math.sin((beta + epsi))															# Vy calculation
				vel_z = speed * math.cos(beta) * math.tan(steering) / (l_f + l_r)								# Epsi dot calculation
				vel.linear.x = vel_x
				vel.linear.y = vel_y
				vel.angular.z = vel_z

				if t_end - time.time() < 0.1 or abs(steering) < epsilon:										# Stopping the turtle when the steering gets lower than a specified threashold or when the time runs out
					
					vel.linear.x = 0
					vel.linear.y = 0
					vel.angular.z = 0
					t_end = time.time()

				pub.publish(vel)																				# Publishing the calculated speeds
				rate.sleep()

			elif drive == 'r':																					# For rear steering option

				sample_time = t_end - time.time()																# Getting the time left in our trial
				steering = map * sample_time																	# Applying steering decay
				beta = math.atan(l_r  * -math.tan(steering) / l_f + l_r)
				vel_x = speed * math.cos (beta + epsi)															# Vx calculation
				vel_y = speed * math.sin (beta + epsi)															# Vy calculation
				vel_z = (speed / (l_f + l_r)) * math.cos(beta) * -math.tan(steering)							# Epsi dot calculation
				vel.linear.x = vel_x
				vel.linear.y = vel_y
				vel.angular.z = vel_z

				if t_end - time.time() < 0.1 or abs(steering) < epsilon:										# Stopping the turtle when the steering gets lower than a specified threashold or when the time runs out

					vel.linear.x = 0
					vel.linear.y = 0
					vel.angular.z = 0
					t_end = time.time()

				pub.publish(vel)																				# Publishing the calculated speeds
				rate.sleep()


if __name__ == '__main__':																						# Checking if we are running this code from the fie itself and not being called from another code
	try:
		go()
	except rospy.ROSInterruptException:
		pass


