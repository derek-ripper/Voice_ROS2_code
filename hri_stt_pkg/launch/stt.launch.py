# Name  : sst.launch.py
# Author: Derek Ripper
# Date  : 12 Jan 2022
#
# Purpose: To lauch Speech to text package
###################################################################################################
from launch             import LaunchDescription
from launch_ros.actions import Node
from launch.actions     import ExecuteProcess

def generate_launch_description():
    ld =  LaunchDescription ([
        Node(
        package    ="hri_stt_pkg",
        executable ="stt_v2.py",
        name       ="stt_node",
        #prefix     = ['stdbuf -o L'],
        output     ="screen",
        parameters =[
        {"SR_SPEECH_ENGINE" : "google_cloud"}
        ])
    ])
    return ld
