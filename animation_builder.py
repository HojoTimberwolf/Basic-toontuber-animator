# -*- coding: utf-8 -*-
"""
Purpose of code is to streamline the process of generating animations for the toontuber setup
Ideally, sets of images will compile into videos and overlapping images will be used for transitions,
idles, peaks, and others. The code is designed to take advantage of this overlap and auto-generate all
required videos for the toontuber setup. PNG images all of the same dimensions are required for the
system to work.

Created on Wed Nov 29 00:38:39 2023

@author: Hojo
"""
from PIL import Image
import cv2
import os
import numpy as np

class animation_framer():
    def __init__(self,img_size=(1583,1776), bkgd_color = (0,204,0)):
        # variables
        self.keyframe_loc = {
            "tail":{"length":1,"directory":r".\animation_builder\Key_frames\{emotion}\Additional","file_names":"FX_Tail.png"},
            "body":{"length":1,"directory":r".\animation_builder\Key_frames\{emotion}\Poses","file_names":"FX_pose_{stance}.png"},
            "eyes":{"length":1,"directory":r".\animation_builder\Key_frames\{emotion}\Additional","file_names":"FX_eyes.png"},
            "VR":{"length":1,"directory":r".\animation_builder\Key_frames\{emotion}\Additional","file_names":"FX_VR.png"},
            "VR_eyes":{"length":1,"directory":r".\animation_builder\Key_frames\{emotion}\Additional","file_names":"FX_VR_eyes.png"}
            }

        self.img_size = img_size
        self.bkgd_color = bkgd_color    

class animator_class():
        
    ####
    # Functions
    ####
    def find_coeffs(self,pa, pb):
        """
        Code copied from StackOverflow that finds coefficients for transforamtion
    
        Parameters
        ----------
        pa : MATRIX
            Defined points of the image
        pb : MATRIX
            Transformation points of new image
    
        Returns
        -------
        MATRIX
            transforms image based on selected points
    
        """
        matrix = []
        for p1, p2 in zip(pa, pb):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
    
        A = np.matrix(matrix, dtype=float)
        B = np.array(pb).reshape(8)
    
        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)
    
    def generate_video(self,img_list,video_name):
        """
        Converts a list of still images into an mp4
    
        Parameters
        ----------
        img_list : LIST
            List of images to be converted into an mp4
            
        video_name : STRING
            Name of output file
    
        Returns
        -------
        None.
    
        """
        
        fourcc = cv2.VideoWriter_fourcc(*'divx')
        width,height = img_list[0].size
        video = cv2.VideoWriter(video_name,fourcc,24,(width,height))
        
        for image in img_list:
            arrImg = np.array(image)
            video.write(cv2.cvtColor(arrImg,cv2.COLOR_RGB2BGR))
                
        cv2.destroyAllWindows()
        video.release()

    def compile_frames(self, animation_length, bkgd_color, img_size, layering = None, bounce = None):
        """
        

        Parameters
        ----------
        
        img_size : TYPE, Array
            the Height and Width of the image to be compiled
            
        bkgd_color : TYPE, Array
            The RGB colors for the background frame
        
        layering : TYPE, DICT
            The default is None.
            
            A Dictionary containing the layers to be concatonated
            The layers are overlaryed based on order so the 1st in the list is on the bottom
            
            example:
            
            layering = {
                "tail":{"length":len(tail_idle_animation), # the overall length of the animation layer
                        "directory":tail_loc, # the location of the frames for the animation layer
                        "file_names":tail_idle_animation, # a list of the frame file names
                        "current_frame":0} # the frame to start on (usually 0)
                }
        bounce : LIST
            Warping of frames to simulate talking
            [0,2,4] : :a good default for a 3 frame talking animation

        Returns
        -------
        frames : TYPE
            DESCRIPTION.

        """
        if layering is None:
            raise ValueError("A layering dictionary needs to be input")

        width,height = img_size
        def_height = height/4

        img_list = []        
        for n in range(0,animation_length):
            bkgd = Image.new("RGB",img_size, bkgd_color)
            for layer in layering:
                if layering[layer]["length"] == 1:
                    im_overlay = Image.open(os.path.join(layering[layer]["directory"],layering[layer]["file_names"]))
                else:
                    if layering[layer]["current_frame"] > layering[layer]["length"]:
                        layering[layer].update({"current_frame":0})
                    
                    im_overlay = Image.open(os.path.join(layering[layer]["directory"],layering[layer]["file_names"][layering[layer]["current_frame"]]))
                    layering[layer].update({"current_frame":layering[layer]["current_frame"] + 1})
                bkgd.paste(im_overlay,(0,0),im_overlay)

            if bounce != None:
                coeffs = self.find_coeffs(
                    [(0, def_height), (width, def_height), (width, height), (0, height)],
                    [(0+bounce[n], def_height+bounce[n]), (width-bounce[n], def_height+bounce[n]), (width, height), (0, height)])
                
                bkgd = bkgd.transform((bkgd.size),Image.PERSPECTIVE,coeffs)
        
            img_list.append(bkgd)        
        
        return img_list
    

class animation_builder(animator_class):
    def __init__(self,animation_framer):
        # variables
        self.animation_framer = animation_framer
            
    
    def build_idle_animation(self,emotion="happy",stance="normal",layering = None,idle_delay = 165):
        """
        

        Parameters
        ----------
        emotion : TYPE, optional
            DESCRIPTION. The default is "happy".
        stance : TYPE, optional
            DESCRIPTION. The default is "normal".
        layering : TYPE, DICT
            The default is None.
            
            A Dictionary containing the layers to be concatonated
            The layers are overlaryed based on order so the 1st in the list is on the bottom
            
            example:
                
            layering = {
                "tail":{"length":len(tail_idle_animation), # the overall length of the animation layer
                        "directory":tail_loc, # the location of the frames for the animation layer
                        "file_names":tail_idle_animation, # a list of the frame file names
                        "current_frame":0} # the frame to start on (usually 0)
                }
        idle_delay : TYPE, optional
            DESCRIPTION. The default is 165.

        Returns
        -------
        None.

        """
        
        if layering is None:
            tail_loc = r".\animation_builder\Idle_animation\{emotion}\Tail".format(emotion=emotion)
            tail_idle_animation = os.listdir(tail_loc)
            vreyes_loc = r".\animation_builder\Idle_animation\{emotion}\VR_Eyes".format(emotion=emotion)
            vr_eye_animation = os.listdir(vreyes_loc)                    
            body_frame = self.animation_framer.keyframe_loc["body"]
            body_frame.update({"directory":body_frame["directory"].format(emotion=emotion)})
            body_frame.update({"file_names":body_frame["file_names"].format(stance=stance)})
            vr_frame = self.animation_framer.keyframe_loc["VR"]
            vr_frame.update({"directory":vr_frame["directory"].format(emotion=emotion)})
            layering = {"tail":{"length":len(tail_idle_animation),"directory":tail_loc,"file_names":tail_idle_animation,"current_frame":0},
                       "body":body_frame,
                       "VR":vr_frame,
                       "VR_eyes":{"length":len(vr_eye_animation),"directory":vreyes_loc,"file_names":vr_eye_animation,"current_frame":0}
                       }
        
        output_frames = self.compile_frames(animation_length = len(vr_eye_animation),
                                            bkgd_color = self.animation_framer.bkgd_color,
                                            img_size = self.animation_framer.img_size, 
                                            layering = layering)
       
        last_frame = output_frames[-1]    
        for x in range(0,idle_delay,1):
            output_frames.append(last_frame)
            
        # img_list[0].save("an.gif",format="gif",append_images=img_list[1:],optimize=False,save_all=True,duration=64,loop=0)
        self.generate_video(output_frames,"idle_{stance}_{emotion}.mp4".format(stance=stance,emotion=emotion))
        
        return -1

    def build_talking_animation(self,emotion="happy",stance="normal",layering = None, bounce=[0,2,4]):
        """
        Build talking and peak animation files

        Parameters
        ----------
        emotion : STR, optional
            DESCRIPTION. The default is "happy".
        stance : STR, optional
            DESCRIPTION. The default is "normal".
        layering : DICT, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        
        if layering is None:
            vreyes_loc = r".\animation_builder\talk_animation\{emotion}\VR_Eyes".format(emotion=emotion)
            vr_eye_animation = os.listdir(vreyes_loc)            
            
            body_frame = self.animation_framer.keyframe_loc["body"]
            body_frame.update({"directory":body_frame["directory"].format(emotion=emotion)})
            body_frame.update({"file_names":body_frame["file_names"].format(stance=stance)})
            vr_frame = self.animation_framer.keyframe_loc["VR"]
            vr_frame.update({"directory":vr_frame["directory"].format(emotion=emotion)})
            tail_frame = self.animation_framer.keyframe_loc["tail"]
            tail_frame.update({"directory":tail_frame["directory"].format(emotion=emotion)})
            layering = {"tail":tail_frame,
                       "body":body_frame,
                       "VR":vr_frame,
                       "VR_eyes":{"length":len(vr_eye_animation),"directory":vreyes_loc,"file_names":vr_eye_animation,"current_frame":0}
                       }
        
        output_frames = self.compile_frames(animation_length = len(vr_eye_animation), 
                                            img_size = self.animation_framer.img_size,
                                            bkgd_color = self.animation_framer.bkgd_color,
                                            layering = layering,
                                            bounce = bounce)

        img_list_anim = [output_frames[2],output_frames[2],output_frames[1],output_frames[1],
                    output_frames[2],output_frames[2],output_frames[1],output_frames[1],
                    output_frames[0]]
        
        #img_list[0].save("an.gif",format="gif",append_images=img_list[1:],optimize=False,save_all=True,duration=64,loop=0)
        self.generate_video(img_list_anim,"talk_{stance}_{emotion}.mp4".format(stance=stance,emotion=emotion))
        self.generate_video([output_frames[2]],"peak_{stance}_{emotion}.mp4".format(stance=stance,emotion=emotion))

    def build_set_animation(self,emotion="happy",stance="normal",layering = None):
        """
        Build the set animation

        Parameters
        ----------
        emotion : TYPE, optional
            DESCRIPTION. The default is "happy".
        stance : TYPE, optional
            DESCRIPTION. The default is "normal".
        layering : TYPE, optional
            DESCRIPTION. The default is None.

        Returns
        -------
        None.

        """
        if layering is None:
            pass
        vreyes_loc = r".\animation_builder\set_animation\{stance}\VR_Eyes".format(stance=stance)
        vr_loc = r".\animation_builder\set_animation\{stance}\VR".format(stance=stance)
        tail_loc = r".\animation_builder\set_animation\{stance}\Tail".format(stance=stance)
        frames_loc = r".\animation_builder\set_animation\{stance}\frames".format(stance=stance)
        
        if os.path.exists(frames_loc):
            frames_loc = r".\animation_builder\set_animation\{stance}\frames".format(stance=stance)
        else:
            frames_loc = r".\animation_builder\set_animation\{stance}\frames".format(stance="Normal")
        
        stance_code = "pose_{stance}".format(stance=stance)
        filename = "{Frame}_{item}_{emotion}.png"
        frame_list = ["F01","F02","F03","F04"]
        item_list_order = {"tail":tail_loc,stance_code:frames_loc,"VR":vr_loc,"VR_Eyes":vreyes_loc}        
        key_item_list_order={"tail":os.path.join(self.animation_framer.keyframe_loc["tail"]["directory"].format(emotion=emotion),
                                                 self.animation_framer.keyframe_loc["tail"]["file_names"]),
                             "body":os.path.join(self.animation_framer.keyframe_loc["body"]["directory"].format(emotion=emotion),
                                                 self.animation_framer.keyframe_loc["body"]["file_names"].format(stance=stance)),
                             "VR":os.path.join(self.animation_framer.keyframe_loc["VR"]["directory"].format(emotion=emotion),
                                               self.animation_framer.keyframe_loc["VR"]["file_names"]),
                             "VR_Eyes":os.path.join(self.animation_framer.keyframe_loc["VR_eyes"]["directory"].format(emotion=emotion),
                                                    self.animation_framer.keyframe_loc["VR_eyes"]["file_names"])}
        
        img_list = []
        for frame_number in frame_list:
            bkgd = Image.new("RGB",self.animation_framer.img_size, self.animation_framer.bkgd_color)
            file_name = os.path.join(item_list_order[stance_code],filename.format(Frame=frame_number,item=stance_code,emotion=emotion))
            if os.path.isfile(file_name):
                for item in item_list_order:
                    # load Item
                    file_name = os.path.join(item_list_order[item],filename.format(Frame=frame_number,item=item,emotion=emotion))
                    if os.path.isfile(file_name):
                        for_overlay = Image.open(file_name)
                    else:
                        file_name = os.path.join(item_list_order[item],filename.format(Frame=frame_number,item=item,emotion="Default"))
                        for_overlay = Image.open(file_name)
                    
                    bkgd.paste(for_overlay,(0,0),for_overlay)
                    
            elif os.path.isfile(os.path.join(item_list_order[stance_code],filename.format(
                    Frame=frame_number,item=list(item_list_order.keys())[1],emotion="Default"))):        
                for item in item_list_order:
                    # load Item
                    file_name = os.path.join(item_list_order[item],filename.format(Frame=frame_number,item=item,emotion=emotion))
                    if os.path.isfile(file_name):
                        for_overlay = Image.open(file_name)
                    else:
                        file_name = os.path.join(item_list_order[item],filename.format(Frame=frame_number,item=item,emotion="Default"))
                        for_overlay = Image.open(file_name)
                    
                    bkgd.paste(for_overlay,(0,0),for_overlay)
            else:
                # load key frames
                for item in key_item_list_order:
                    # load Item
                    file_name = os.path.join(key_item_list_order[item])
                    if os.path.isfile(file_name):
                        for_overlay = Image.open(file_name)
                
                    bkgd.paste(for_overlay,(0,0),for_overlay)
                    
            img_list.append(bkgd)
            img_list.append(bkgd)
        #img_list[0].save("an.gif",format="gif",append_images=img_list[1:],optimize=False,save_all=True,duration=64,loop=0)
        self.generate_video(img_list,"set_{stance}_{emotion}.mp4".format(stance=stance,emotion=emotion))



if __name__ == "__main__":
    
    # emotion_list = ["angry","derp","happy","jolly","sigh","surprised","think"]
    # stance_list = ["normal","game","casual"]
    
    emotion_list = ["angry"]
    stance_list = ["normal"]
    
    ac = animation_framer()
    ab = animation_builder(ac)    
    for emotion in emotion_list:
        for stance in stance_list:
            ab.build_idle_animation(emotion=emotion,stance=stance)    
            ab.build_talking_animation(emotion=emotion,stance=stance)
            ab.build_set_animation(emotion=emotion,stance=stance)


