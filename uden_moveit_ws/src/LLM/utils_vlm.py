# This is based on the TommyZihao (github)
# Chen Li 2024-7-28

import time
import cv2
import numpy as np
from PIL import Image
from PIL import ImageFont, ImageDraw
import requests
import json
import base64

# import font type
font = ImageFont.truetype('asset/Times_New_Roman.ttf', 26)

# Define the VLM models
vlm_model = ['llava:7b']


# Define the URL of OLLAMA (VLM and LLM)
url = "http://130.225.39.157:11434/api/generate"

# change the image to base 64 encode
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        # Read the image file as binary
        encoded_string = base64.b64encode(image_file.read())
        # Decode the bytes to a string
        return encoded_string.decode('utf-8')


# extract the json string from the response
def extract_between_braces(input_string):
    start = input_string.find('{')
    end = input_string.find('}', start) + 1
    if start > 0 and end > start:
        return input_string[start:end]
    else:
        return None


# system prompt
SYSTEM_PROMPT = '''
I'm about to give an instruction for a robotic arm. Please help me extract the start object and end object from this sentence, and then find the pixel coordinates of the top-left and bottom-right corners of these two objects from this image. Output the data in a JSON structure.

For example, if my instruction is: Please help me put the red block on the house sketch.
You should only output the following data structure. It should be a pure text not Json string.
{
"start":"red block",
"start_xyxy":[[102,505],[324,860]],
"end":"house sketch",
"end_xyxy":[[300,150],[476,310]]
}

My instruction is:
'''


def vlm_crd(PROMPT='Help me put the yellow block on deadpool', img_path='temp/vl_now.jpg'):
    response = ''
    
    # prompt
    message = SYSTEM_PROMPT + PROMPT

    # Convert the image to base64
    base64_image = image_to_base64(img_path)

    # VLM
    payload = {
        "model": vlm_model[0],
        "prompt": message,
        "stream": False,
        "images": [base64_image],
    }

    # Perform the POST request with data
    response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        try:
            # Attempt to parse the JSON response
            response = response.json()
            response = extract_between_braces(response['response'])
            print("Max: ", response)
        except requests.exceptions.JSONDecodeError as e:
            print("JSON Decode Error:", e)
    else:
        print("Error:", response.status_code, response.text)

    return eval(response)

def post_processing_viz(result, img_path, check=False):
    
    '''
    Visual Large Model Output Post-processing and Visualization
    Check: Whether human screen confirmation is needed for successful visualization, press key to continue or exit
    '''

    # post-process
    img_bgr = cv2.imread(img_path)
    img_h = img_bgr.shape[0]
    img_w = img_bgr.shape[1]
    # scale factor
    FACTOR = 500
    # start object
    START_NAME = result['start']
    # destination object
    END_NAME = result['end']
    # Starting point, top-left pixel coordinates
    START_X_MIN = int((result['start_xyxy'][0][0]) * img_w / FACTOR)
    START_Y_MIN = int((result['start_xyxy'][0][1]) * img_h / FACTOR)
    # Starting point, top-right pixel coordinates
    START_X_MAX = int((result['start_xyxy'][1][0]) * img_w / FACTOR)
    START_Y_MAX = int((result['start_xyxy'][1][1]) * img_h / FACTOR)
    # Starting point, center pixel coordinates
    START_X_CENTER = int((START_X_MIN + START_X_MAX) / 2)
    START_Y_CENTER = int((START_Y_MIN + START_Y_MAX) / 2)
    # Target point, top-left pixel coordinates
    END_X_MIN = int((result['end_xyxy'][0][0]) * img_w / FACTOR)
    END_Y_MIN = int((result['end_xyxy'][0][1]) * img_h / FACTOR)
    # Target point, top-right pixel coordinates
    END_X_MAX = int((result['end_xyxy'][1][0]) * img_w / FACTOR)
    END_Y_MAX = int((result['end_xyxy'][1][1]) * img_h / FACTOR)
    # Target point, center pixel coordinates
    END_X_CENTER = int((END_X_MIN + END_X_MAX) / 2)
    END_Y_CENTER = int((END_Y_MIN + END_Y_MAX) / 2)
    
    # Visualization
    # Start object: Draw the bounding box of the starting point object
    img_bgr = cv2.rectangle(img_bgr, (START_X_MIN, START_Y_MIN), (START_X_MAX, START_Y_MAX), [0, 0, 255], thickness=3)
    # Start object: Draw the bounding box of the center point object 
    img_bgr = cv2.circle(img_bgr, [START_X_CENTER, START_Y_CENTER], 6, [0, 0, 255], thickness=-1)
    # Target object: Draw the bounding box of the target point object
    img_bgr = cv2.rectangle(img_bgr, (END_X_MIN, END_Y_MIN), (END_X_MAX, END_Y_MAX), [255, 0, 0], thickness=3)
    # Target object: Draw the bounding box of the center point object
    img_bgr = cv2.circle(img_bgr, [END_X_CENTER, END_Y_CENTER], 6, [255, 0, 0], thickness=-1)
    # Write the name
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # BGR to RGB
    img_pil = Image.fromarray(img_rgb) # array to pil
    draw = ImageDraw.Draw(img_pil)
    # write start object name
    draw.text((START_X_MIN, START_Y_MIN-32), START_NAME, font=font, fill=(255, 0, 0, 1)) # Text coordinates, Chinese string, font, RGBA color
    # write target object name
    draw.text((END_X_MIN, END_Y_MIN-32), END_NAME, font=font, fill=(0, 0, 255, 1)) # Text coordinates, Chinese string, font, RGBA color
    img_bgr = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) # RGB to BGR
    # save image
    cv2.imwrite('temp/vl_now_viz.jpg', img_bgr)

    formatted_time = time.strftime("%Y%m%d%H%M", time.localtime())
    cv2.imwrite('visualizations/{}.jpg'.format(formatted_time), img_bgr)

    # display on screen
    cv2.imshow('vlm_AI', img_bgr) 

    if check:
        print("Please confirm successful visualization. Press 'c' to continue, or 'q' to exit.")
        key = cv2.waitKey(10) & 0xFF
        if key == ord('c'): # press c to continue
            pass
        if key == ord('q'): # press q to quit
            # exit()
            cv2.destroyAllWindows()   # close all opencv windows
            raise NameError('press q to quit')



        # while(True):
        #     key = cv2.waitKey(10) & 0xFF
        #     if key == ord('c'): # press c to continue
        #         break
        #     if key == ord('q'): # press q to quit
        #         # exit()
        #         cv2.destroyAllWindows()   # close all opencv windows
        #         raise NameError('press q to quit')
    else:
        if cv2.waitKey(1) & 0xFF == None:
            pass

    return START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER

# result = {
# "start": "yellow brick",
# "start_xyxy": [[70, 300], [150, 380]],
# "end": "deadpool",
# "end_xyxy": [[430, 80], [530, 180]]
# }

# img_path = 'temp/vl_now.jpg'

# START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER = post_processing_viz(result, img_path, check=False)
# print (START_X_CENTER, START_Y_CENTER, END_X_CENTER, END_Y_CENTER)


# start object: x -70; y + 30
# target object: x - 20
