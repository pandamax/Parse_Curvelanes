'''
convert to Tusimple json/txt format.
'''

import cv2
import json
import numpy as np
import os

'''
separate the whole dataset 150K into three parts: train:100K, val: 20K and testing: 30K. 
The resolution of most images in this dataset is 2650×1440.

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


def get_mask(mask, label, instance_gap):
    # read label
    label_content = open(label)
   
    label_info = json.load(label_content)
    lanes_num = 0
    
    for index, line in enumerate(label_info['Lines']):
        lanes_num += 1
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
            image = cv2.line(mask, points[ptStart], points[ptEnd], [instance_gap * (index+1)]*3, 4, lineType = 8)
            ptStart += 1
            ptEnd +=  1
        
        max_val = lanes_num * 30
            
    return image, max_val

def lane_instance(label_gray,pix_value, hstart, hend, hdis):
    lane = []
    for hstep in range(hstart, hend, hdis): # 
        # h_samples.append(hstep)
        # print(img.shape)# 720*1280 hw
        wids = np.where(label_gray[hstep][:] == pix_value)
        for ele in list(wids):
            # print(list(ele))
            if len(ele) == 0:
                val = -2
            else:
                val = int(sum(ele)/(len(ele))) # get average x_value.
            # if val != 1:
            lane.append(val)
    return lane      
     
# choose datasets category from:'train','test' or 'valid'
datasets_category = 'train'  
path_to_datasets = r'E:/Curvelanes/Curvelanes'   
# datasets dir
dataset_dir = '{}/{}/'.format(path_to_datasets, datasets_category)
# write ground truth in json or txt.
save_gt = dataset_dir + '{}.json'.format(datasets_category)
# save_gt = dataset_dir + '{}.txt'.format(datasets_category)

# read file from txt
txt_file = dataset_dir  + '{}.txt'.format(datasets_category)

file_list = open(txt_file)
for file in file_list:
    print("Now dealing with:", file)
    file_name = os.path.splitext(file.strip().split('/')[-1])[0] 
    json_file = dataset_dir + 'labels/'+ file_name + '.lines.json'
    
    # get img shape,h and w. 
    full_img_path = dataset_dir + file.strip()
    
    # print("full_img_path:", full_img_path)
    if os.path.exists(full_img_path):
        img = cv2.imread(full_img_path)
        
        h = img.shape[0]
        w = img.shape[1]
        
        # set param.
        points_num = 56
        instance_gap = 20
        hstart = 0
        hend   = h
        hdis   = h // points_num
        
        img_dict = {}
        h_samples = [] # height
        lanes = []
        
        mask = np.zeros([h,w,3],dtype=np.uint8)
        
        # parse label
        label_mask, max_value = get_mask(mask, json_file,instance_gap)
        
        # convert to grayscale.
        label_gray = label_mask[:,:,1]
        
        for hstep in range(hstart, hend, hdis):
            h_samples.append(hstep)
            
        # neg samples.   
        if  max_value == 0:
            lanes.append([-2]*points_num)
            
        # value:pix_value
        else:
            for value in range(instance_gap, max_value + 1, instance_gap):
                # print("value", value)
                lane = lane_instance(label_gray,value, hstart, hend, hdis)
                
                if max(lane) == -2:
                    lanes.append([-2]*points_num)
                else:
                    lanes.append(lane)

        img_dict["lanes"] = lanes
        img_dict["h_samples"] = h_samples
        img_dict["raw_file"] = f'{"images/"}{file_name}{".jpg"}' # img_path
        
        img_dict_str = str(img_dict)
        # print(img_dict_str)
        img_dict = eval(img_dict_str)
        
        # write to txt
        # with open("save_gt","a+") as f:
        #     f.writelines(img_dict_str + '\n')
        #     f.close()

        # write to json
        with open(save_gt,"a+") as out:
            string = json.dumps(img_dict)
            string += '\n'
            out.write(string)
            out.close()

        # cv2.imencode('.png',label_mask)[1].tofile('{}\{}.png'.format(save_mask_dir,file_name))
    
    
print("finished~~")



