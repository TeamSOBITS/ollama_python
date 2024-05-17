#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import actionlib
from ollama_python.msg import ChatOllamaAction
from ollama_python.msg import ChatOllamaGoal
from ollama_python.msg import ChatOllamaActionFeedback


feedback_msg = ChatOllamaActionFeedback()
def actionfeedback_callback(msg):
    global feedback_msg
    feedback_msg = msg


def ollama_client():
    global feedback_msg
    action_client = actionlib.SimpleActionClient("/ollama_action", ChatOllamaAction)
    rospy.Subscriber("/ollama_action/feedback", ChatOllamaActionFeedback, actionfeedback_callback)
    action_client.wait_for_server()
    goal = ChatOllamaGoal()
    goal.room_name = "introduce"
    goal.request = "My team name is SOBITS"
    goal.is_service = False
    action_client.send_goal(goal)
    wip_result = ""
    while not feedback_msg.feedback.end_flag:
        if ((len(wip_result) != len(feedback_msg.feedback.wip_result))):
            wip_result = feedback_msg.feedback.wip_result
            print(wip_result)
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