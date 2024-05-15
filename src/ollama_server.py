#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
import time

import asyncio
import ollama


# async def main():
#     client = ollama.AsyncClient()

#     chat_messages = {}

#     while True:
#         mode_name = input("mode name >>> ")
#         if content_in := input('>>> '):
#             starting_time = time.time()
#             if ((mode_name in chat_messages.keys()) != True):
#                 chat_messages[mode_name] = []
#             chat_messages[mode_name].append({'role': 'user', 'content': content_in})

#             message = {'role': 'assistant', 'content': ''}
#             async for response in await client.chat(model='llama3', messages=chat_messages[mode_name], stream=True):
#                 if response['done']:
#                     chat_messages[mode_name].append(message)

#                 content = response['message']['content']
#                 print(content, end='', flush=True)

#                 message['content'] += content

#             print()
#             elapsed_time = time.time() - starting_time


# if __name__ == '__main__':
#     # rospy.init_node("ollama_server")
#     try:
#         asyncio.run(main())
#     except (KeyboardInterrupt, EOFError):
#         ...



import actionlib
from ollama_python.msg import ChatOllamaAction        
from ollama_python.msg import ChatOllamaResult
from ollama_python.msg import ChatOllamaFeedback


class ChatAction:
    def __init__(self):
        self.model_ = rospy.get_param("/model_name", "llama3")
        self.ollama_client_ = ollama.AsyncClient()
        self.chat_messages_ = {}
        self.action_server_ = actionlib.SimpleActionServer("/ollama_action", ChatOllamaAction, execute_cb=self.chat_ollama_callback, auto_start=False)
        self.action_server_.start()
    
    async def dynamic_chat(self, mode_name):
        starting_time = time.time()

        message = {'role': 'assistant', 'content': ''}
        async for response in await self.ollama_client_.chat(model=self.model_, messages=self.chat_messages_[mode_name], stream=True):
            if response['done']:
                self.chat_messages_[mode_name].append(message)
                elapsed_time = time.time() - starting_time
                return elapsed_time, message['content']

            content = response['message']['content']
            print(content, end='', flush=True)
            feedback = ChatOllamaFeedback(wip_result=message['content'], end_flag=False)
            self.action_server_.publish_feedback(feedback)

            message['content'] += content


    def chat_ollama_callback(self, goal):
        if ((goal.room_name in self.chat_messages_.keys()) != True):
            self.chat_messages_[goal.room_name] = []
        self.chat_messages_[goal.room_name].append({'role': 'user', 'content': goal.request})
        t, res = asyncio.run(self.dynamic_chat(goal.room_name))
        feedback = ChatOllamaFeedback(wip_result=res, end_flag=True)
        self.action_server_.publish_feedback(feedback)
        result = ChatOllamaResult(result=res, elapsed_time=t)
        self.action_server_.set_succeeded(result)
        print()
        print(self.chat_messages_)


if __name__ == '__main__':
    rospy.init_node('ollama_server')
    chat_action = ChatAction()
    rospy.spin()