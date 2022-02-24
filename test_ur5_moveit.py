# coding=utf-8
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import sys
sys.path.append('../../source/pyHand_API')
import pyHand_api as hand
import time

###
# ur5初始化
print "============ Starting tutorial setup"  #初始化moveit_commander和rospy
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)
robot = moveit_commander.RobotCommander()  #实例化RobotCommander对象，这个接口是机器人总入口
scene = moveit_commander.PlanningSceneInterface()  #实例化PlanningSceneInterface对象，这个接口围绕机器人的世界
group = moveit_commander.MoveGroupCommander("manipulator")  #实例化MoveGroupCommander对象，这个接口应用与一组关节。以规划和执行动作
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)  #创建DisplayTrajectory发布器，可以得到轨迹在Rviz总实现可视化
###
# ur5获得基本信息

print "============ Reference frame: %s" % group.get_planning_frame()  #打印参考系的名称
print "============ Reference frame: %s" % group.get_end_effector_link()  #打印这个组的末端执行器的连接名称
print "============ Robot Groups:"  #获得机器人的所有组
print robot.get_group_names()
print "============ Printing robot state"  #用于调式，打印机器人的状态
print robot.get_current_state()
print "============"

###
# bh初始化

# hand.initialize()
# hand.init_hand()

###
# bh设置常量

MODE = 8
MODE_IDLE= 0
M = 58			# Position move command
MODE_VEL = 4
V = 44
TSTOP = 78

MIN_ENC = 0 		# The closed position for each motor.
MAX_ENC = 105000	# The open position for each motor.

FINGER1 = 11	# Puck ID for F1
FINGER2 = 12	# Puck ID for F2
FINGER3 = 13	# Puck ID for F3
SPREAD  = 14	# Puck ID for SP
HAND_GROUP = 0x405 	# Refers to all motors that respond to group ID 5.

###
# 抓取物体
hand.set_property(FINGER1, V, 70)  #速度设置
hand.set_property(FINGER2, V, 70)
hand.set_property(FINGER3, V, 70)
hand.set_property(HAND_GROUP, MODE, MODE_VEL)
time.sleep(1.5)

hand.set_property(HAND_GROUP, M, MAX_ENC)  #抓取闭合程度
# ... and don't forget to stop the spread quickly.
hand.set_property(SPREAD, MODE, MODE_IDLE)
# Now we wait for the fingers to stop moving so that fingers and spread don't
# run into one another.
time.sleep(1.5)

###
# 移动到某处
joint_positions = [0, 0, -1.5, -0.5, 0.5, -1]  #此处采用改变关节角数值的方法
group.set_joint_value_target(joint_positions)
group.go()

###
# 放下物体
hand.set_property(HAND_GROUP, M, MIN_ENC)
hand.set_property(SPREAD, MODE, MODE_IDLE)
time.sleep(1.5)