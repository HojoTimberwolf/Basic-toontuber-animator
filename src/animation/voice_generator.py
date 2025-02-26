# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F
import IPython

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice, load_voices

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap


###############################################################################
# functions
###############################################################################
def bubble_text(image,cycles):
    """
    turn text into bubble text

    Parameters
    ----------
    image : Pillow Image
        DESCRIPTION.
    cycles : size of boarder around text
        DESCRIPTION.

    Returns
    -------
    None.

    """
    for _ in range(cycles):
        dilate_image = image.filter(ImageFilter.MaxFilter(9))

    width = dilate_image.size[0] 
    height = dilate_image.size[1] 
    for i in range(0,width):# process all pixels
        for j in range(0,height):
            data = dilate_image.getpixel((i,j))
            #print(data) #(255, 255, 255)
            if (data[3]!=0):
                dilate_image.putpixel((i,j),(22, 22, 22))

    bubble_image = Image.alpha_composite(dilate_image,image)    
    return bubble_image

###############################################################################
# Text to be processed
###############################################################################
text_list = []
for text in open("script.txt"):
    text_list.append(text)


###############################################################################
# generate audio
###############################################################################
tts = TextToSpeech()
voice_samples, conditioning_latents = load_voice(CUSTOM_VOICE_NAME)

# Generate speech with the custotm voice.
for idx, text in enumerate(text_list):
    if idx <-1:
        continue
    gen = tts.tts_with_preset(text, voice_samples=voice_samples, conditioning_latents=conditioning_latents, 
                              preset=preset)
    torchaudio.save(f'generated-{idx}-{CUSTOM_VOICE_NAME}.wav', gen.squeeze(0).cpu(), 24000)
    IPython.display.Audio(f'generated-{idx}-{CUSTOM_VOICE_NAME}.wav')


###############################################################################
# generate Subtitles
###############################################################################
for idx, text in enumerate(text_list):
    lines = textwrap.wrap(text,width=tw_char_limit)
    lns = len(lines)
    con_line = ""
    for idl,line in enumerate(lines):
        if idl == 0:
            con_line = con_line + line
        else:
            con_line = con_line + "\n" + line
    
    img = Image.new("RGBA",(width,height),(0,0,0,0))
    ImageD = ImageDraw.Draw(img)
    
    _,_,mlx,mly = ImageD.multiline_textbbox((0,0),con_line,font=font,align="center")
    ImageD.multiline_text(((width-mlx)/2,nyloc),con_line,font=font,fill=(255,255,255),align="center")
    img = bubble_text(img,3)

    img.save(f"subtitles-{idx}.png")


