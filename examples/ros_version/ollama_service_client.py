#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import actionlib
from ollama_python.msg import ChatOllamaAction
from ollama_python.msg import ChatOllamaGoal
from ollama_python.msg import ChatOllamaActionFeedback


def ollama_client():
    global feedback_msg
    action_client = actionlib.SimpleActionClient("/ollama_action", ChatOllamaAction)
    action_client.wait_for_server()
    goal = ChatOllamaGoal()
    goal.room_name = "introduce"
    goal.request = "My team name is SOBITS"
    goal.is_service = True
    action_client.send_goal(goal)
    action_client.wait_for_result()
    result = action_client.get_result()

    print("\n------------------RESULT--------------------")
    print("Result: ",result.result)
    print("\t\t\t\t\t(Elapsed Time: ", result.elapsed_time, ")")
    print("--------------------------------------------")


if __name__ ==  '__main__':
    try:
        rospy.init_node('ollama_action_client')
        ollama_client()
    except rospy.ROSInterruptException:
        pass