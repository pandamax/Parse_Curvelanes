'''
解析curvaLanes数据集
数据集格式：
train/valid
    │  train/valid.txt
    │  
    ├─images
    │      00022953ff37d3174cff99833df8799e.jpg
    │      ...
    │      
    └─labels
            00022953ff37d3174cff99833df8799e.lines.json
            ...
            
label:
{
  "Lines":[
    # A lane marking
    [
      # The x, y coordinates for key points of a lane marking that has at least two key points.
      {
        "y":"1439.0",
        "x":"2079.41"
      },
      {
        "y":"1438.08",
        "x":"2078.19"
      },
      ...
    ]
    ...
  ]
}

train/valid.txt
    images/c105ddad0167f20c619121e28a2c573c.jpg
    images/ea52bafd2bcb4fd886e1d8d0d4c3c6a9.jpg
    ...
'''

import os 
import cv2
import numpy as np
import json

# choose vis_mode between point and curves
# vis_mod = 'points' # curves
vis_mod = 'curves'

color = [(218,112,214), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255),
     (100, 255, 0), (100, 0, 255), (255, 100, 0), (0, 100, 255), (255, 0, 100), (0, 255, 100)]

def get_points(mask, label):
    # read label
    label_content = open(label)
   
    label_info = json.load(label_content)
    
    # label_info = eval(label_info)
    for index, line in enumerate(label_info['Lines']):
        # print(line)
        points_x = []
        points_y = []
        # get points
        for point in line:
            points_x.append(int(float(point['x'])))
            points_y.append(int(float(point['y'])))
        
        ptStart = 0
    
        points = list(zip(points_x, points_y))
        # sort along y
        sorted(points , key=lambda k: (k[1], k[0]))
        
        # print(points)
        while ptStart < len(points_x):
            image = cv2.circle(mask, points[ptStart], 5, color[index], -1)
            ptStart += 1
            
    return image
 
 
 
def get_curves(mask, label):
    # read label
    label_content = open(label)
   
    label_info = json.load(label_content)
    
    # label_info = eval(label_info)
    for index, line in enumerate(label_info['Lines']):
        # print(line)
        points_x = []
        points_y = []
        # get points
        for point in line:
            points_x.append(int(float(point['x'])))
            points_y.append(int(float(point['y'])))
        
        ptStart = 0
        ptEnd =  1
        
        points = list(zip(points_x, points_y))
        # sort along y
        sorted(points , key=lambda k: (k[1], k[0]))
        
        # print(points)
        while ptEnd < len(points_x):
            image = cv2.line(mask, points[ptStart], points[ptEnd], color[index], 4, lineType = 8)
            ptStart += 1
            ptEnd +=  1
            
    return image      
# datasets dir
dataset_dir = r'E:/Curvelanes/Curvelanes/valid/'

# save label dir(mask)
save_mask_dir = dataset_dir + 'vis_datasets'
if not os.path.exists(save_mask_dir):
    os.makedirs(save_mask_dir)
    
    
# read file from txt
txt_file = dataset_dir  + 'valid.txt'
file_list = open(txt_file)
for file in file_list:
    print("Now dealing with:", file)
    file_name = os.path.splitext(file.strip().split('/')[-1])[0] 
    json_file = dataset_dir + 'labels/'+ file_name + '.lines.json'
    
    # get img shape,h and w. 
    full_img_path = dataset_dir + file.strip()
    
    # print("full_img_path:", full_img_path)
    img = cv2.imread(full_img_path)
    
    # datasets have different height and width.
    h = img.shape[0]
    w = img.shape[1]
    # print("h, w",h,w)
    mask =  np.zeros([h,w,3],dtype=np.uint8)
    
    # parse label
    # print("json_file:", json_file)
    # visulize points
    if vis_mod == 'points':
        label_mask = get_points(img, json_file)
    else:
        # visulize curves
        label_mask = get_curves(img, json_file)
    
    cv2.imencode('.png',label_mask)[1].tofile('{}\{}.png'.format(save_mask_dir,file_name))
    
    
    
print("finished~~")

    
    
    
    
    
    
    
    



