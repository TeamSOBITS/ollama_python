#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy

import actionlib
from ollama_python.msg import ChatOllamaAction
from ollama_python.msg import ChatOllamaGoal

def ollama_client():
    print(1)
    action_client = actionlib.SimpleActionClient("/ollama_action", ChatOllamaAction)
    print(2)
    action_client.wait_for_server()
    print(3)
    goal = ChatOllamaGoal()
    goal.room_name = "hello"
    goal.request = "Do you know my name?"

    action_client.send_goal(goal)
    # action_client.wait_for_result()
    while not rospy.is_shutdown():
    #     print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    #     feedback = action_client.get_feedback()
    #     print(feedback)
    result = action_client.get_result()
    print(result)

if __name__ ==  '__main__':
    try:
        rospy.init_node('ollama_client')
        ollama_client()
    except rospy.ROSInterruptException:
        pass