# datasets structure:
```
CurveLanes
    |----test
           |----images
           |----labels
    |----train
           |----images
           |----labels
           |----train.json                            
    |----valid
           |----images
           |----labels
           |----valid.json
```
# parse_CurveLanes
for parsing and converting dataset CurveLanes.

- parse_curvelanes.py：generate segmentation mask.
- vis_curvelanes.py: visualize datasets on original image.
- curvelanes2tusimples.py: convert datasets to tusimple format.
- vis_converted.py: visualize converted tusimple-like format.

the scripts above have tested on wsl/linux.

# reference
[CurveLanes](https://github.com/SoulmateB/CurveLanes)
