# APM_Human

## **pipeline**
Run pipeline.py\
`python pipeline.py  --video_file=test_video/4.mp4 --region_type=horizontal --do_entrance_counting --draw_center_traj
`

### cfg_utils:
control the parameters


### Pipeline structure:
Main -> class pipeline(object)\
multi_camera -> default (False) 
-> change False to True (if using two cameras) [APM train need to use two cameras for on car]

**_Settings before run the detection/infer program_**

### PipePredictor structure:
The pipeline for video input:\
        1. Tracking\
        2. Tracking -> Attribute\
        3. Tracking -> KeyPoint -> SkeletonAction Recognition\
        4. VideoAction Recognition
