import requests
from json import JSONDecoder

import cv2
import numpy as np

import os
import glob
import platform
if platform.system()=='Windows':
    SplitSym = '\\'
else:
    SplitSym = '/'

def getFaces(image_path):
    http_url ="https://api-cn.faceplusplus.com/facepp/v3/detect"
    key ="hTP7lwfruByyRkRrUd7qFpiLJCL1ZSaJ"
    secret ="pZwT-RQufpkNz0h5iaZp--PadtGxh9kC"
    data = {"api_key":key,"api_secret": secret,"return_gesture": "1","return_landmark":"1","return_attributes":"emotion,gender,age,eyestatus,headpose,smiling"}
    files = {"image_file": open(image_path, "rb")}
    response = requests.post(http_url, data=data, files=files)
    req_con = response.content.decode('utf-8')
    req_dict = JSONDecoder().decode(req_con)
    return req_dict
def getInfos(req_dict):
    infos = []
    for face_id in range(len(req_dict['faces'])):
        info = []
        face_dict = req_dict['faces'][face_id]

        print('get landmarks...')
        landmark = []
        landmark_dict = face_dict['landmark']
        for landmark_name in landmark_dict.keys():
            landmark.append(int(landmark_dict[landmark_name]['x']))
            landmark.append(int(landmark_dict[landmark_name]['y']))
        info.append(landmark)

        print('get emotions...')
        emotion = []
        emotion_dict = face_dict['attributes']['emotion']
        for emotion_name in emotion_dict.keys():
            emotion.append(float(emotion_dict[emotion_name]))
        info.append(emotion)

        print('get gender...')
        gender = face_dict['attributes']['gender']['value']
        info.append(gender)

        print('get age...')
        age = int(face_dict['attributes']['age']['value'])
        info.append(age)
        
        print('get eyestatus...')
        eyestatus = []
        eyestatus_dict = face_dict['attributes']['eyestatus']['left_eye_status']
        for eyestatus_name in eyestatus_dict.keys():
            eyestatus.append(float(eyestatus_dict[eyestatus_name]))
        info.append(eyestatus)
        eyestatus = []
        eyestatus_dict = face_dict['attributes']['eyestatus']['right_eye_status']
        for eyestatus_name in eyestatus_dict.keys():
            eyestatus.append(float(eyestatus_dict[eyestatus_name]))
        info.append(eyestatus)

        print('get headpose...')
        headpose = []
        headpose_dict = face_dict['attributes']['headpose']
        for headpose_name in headpose_dict.keys():
            headpose.append(float(headpose_dict[headpose_name]))
        info.append(headpose)

        print('get smile...')
        smile = int(face_dict['attributes']['smile']['value'])
        info.append(smile)

        infos.append(info)

    return infos
def parseInfos(infos,line):
    for infos_id in range(len(infos)):
        info = infos[infos_id]
        
        landmark = info[0]
        for landmark_id in range(len(landmark)):
            line = '{} {}'.format(line,landmark[landmark_id])

        emotion = info[1]
        for emotion_id in range(len(emotion)):
            line = '{} {}'.format(line,emotion[emotion_id])

        gender = info[2]
        line = '{} {}'.format(line,gender)
 
        age = info[3]
        line = '{} {}'.format(line,age)

        left_eyestatus = info[4]
        for left_eyestatus_id in range(len(left_eyestatus)):
            line = '{} {}'.format(line,left_eyestatus[left_eyestatus_id])

        right_eyestatus = info[5]
        for right_eyestatus_id in range(len(right_eyestatus)):
            line = '{} {}'.format(line,right_eyestatus[right_eyestatus_id])

        headpose = info[6]
        for headpose_id in range(len(headpose)):
            line = '{} {}'.format(line,headpose[headpose_id])

        smile = info[7]
        line = '{} {}'.format(line,smile)

    line = '{}\n'.format(line)
    return line

if __name__=='__main__':
    import shutil

    path_name = '2'
    easy_image_path = os.path.join(os.getcwd(),path_name+'easy')
    if not os.path.exists(easy_image_path):
        os.makedirs(easy_image_path)
    hard_image_path = os.path.join(os.getcwd(),path_name+'hard')
    if not os.path.exists(hard_image_path):
        os.makedirs(hard_image_path)

    f = open(os.path.join(os.getcwd(),'{}.txt'.format(path_name)),'w')

    for image_path in glob.glob(os.path.join(os.getcwd(),path_name,'*.jpg')):
        line = '{}'.format(image_path.split(SplitSym)[-1])
        print('processing image {}'.format(image_path.split(SplitSym)[-1]))

        try:
            faces_dict = getFaces(image_path)
            infos = getInfos(faces_dict)
            
            if len(infos)<1:
                os.remove(image_path)
                continue

            line = parseInfos(infos,line)
            f.write(line)

            shutil.copyfile(image_path,os.path.join(easy_image_path,image_path.split(SplitSym)[-1]))
            print('good image {}...'.format(image_path.split(SplitSym)[-1]))
            os.remove(image_path)
        except:
            shutil.copyfile(image_path,os.path.join(hard_image_path,image_path.split(SplitSym)[-1]))
            print('bad image {}...'.format(image_path.split(SplitSym)[-1]))
            os.remove(image_path)
    f.close()
        
        



