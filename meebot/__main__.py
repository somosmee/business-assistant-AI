import os
import docker
import subprocess
from meebot.env import setup_env
from meebot.chatbot import ChatBot
from meebot.evaluation import run_tests
from meebot.evaluation import intents_dataset

'''
 ENV VARIABLES
'''
os.environ['MONGO_URI'] = 'mongodb://localhost:27021/?readPreference=primary&appname=MongoDB%20Compass&ssl=false'
os.environ['USER_OID'] = '5d2c89e514b9f2001dcb059b'

if __name__ == '__main__':
    client = docker.from_env()
    setup_env(client)

    chatbot = ChatBot(intents_dataset)
    run_tests(chatbot)
