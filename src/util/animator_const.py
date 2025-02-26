# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 22:47:18 2025

@author: drag0
"""

from PIL import ImageFont

###############################################################################
# Variables
###############################################################################
# Video
IMG_WIDTH = 1080
IMG_HEIGHT = 1920
IMG_FONT=ImageFont.truetype("arial.ttf",size=65)

# Audio
# Pick a "preset mode" to determine quality. Options: {"ultra_fast", "fast" (default), "standard", "high_quality"}. See docs in api.py
preset = "high_quality"
CUSTOM_VOICE_NAME = "hojo_normal"
custom_voice_folder = f"tortoise/voices/{CUSTOM_VOICE_NAME}"

# text
tw_char_limit = 32
nxloc = 15
nyloc = (IMG_HEIGHT)/1.8
