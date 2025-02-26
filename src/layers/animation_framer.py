# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 22:16:30 2025

@author: drag0
"""

class AnimationFramer:
    def __init__(self, img_size = (1583, 1776), bkgd_color = (0, 204, 0), keyframe_loc = None):

        # variables
        if keyframe_loc is None:            
            self.keyframe_loc = {
                "tail":{
                        "length" : 1,
                        "directory" : r".\animation_builder\Key_frames\{emotion}\Additional",
                        "file_names" : "FX_Tail.png"
                        },
                "body":{
                        "length" : 1,
                        "directory" : r".\animation_builder\Key_frames\{emotion}\Poses",
                        "file_names" : "FX_pose_{stance}.png"
                        },
                "eyes":{
                        "length" : 1,
                        "directory" : r".\animation_builder\Key_frames\{emotion}\Additional",
                        "file_names" : "FX_eyes.png"
                        },
                "VR":{
                        "length" : 1,
                        "directory" : r".\animation_builder\Key_frames\{emotion}\Additional",
                        "file_names" : "FX_VR.png"
                        },
                "VR_eyes":{
                        "length" : 1,
                        "directory" : r".\animation_builder\Key_frames\{emotion}\Additional",
                        "file_names" : "FX_VR_eyes.png"
                        }
                }
        else:
            self.keyframe_loc = keyframe_loc

        self.img_size = img_size
        self.bkgd_color = bkgd_color    