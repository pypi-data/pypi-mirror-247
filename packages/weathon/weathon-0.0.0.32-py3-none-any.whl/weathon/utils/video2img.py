import os
import ffmpeg

# 每隔一秒提取一张图片
# ffmpeg -i xxx.mp4 -r 1 yyy_%04d.jpg -y

# str = 'ffmpeg -i {} -r 1 {}'
#
# input_dir = "/Users/lizhen/pythonProject/weathon_package/data/input_videos"
# output_dir = '/Users/lizhen/pythonProject/weathon_package/data/out_imgs'
#
# for name in os.listdir(input_dir):
#     input_video_path = os.path.join(input_dir, name)
#     output_img_path = os.path.join(output_dir, 'image-%4d.jpg')
#     str_cmd = str.format(input_video_path, output_img_path)
#     print(str_cmd)
#
#     os.popen(str_cmd)

import cv2
import os


class Video2Img:
    def __init__(self, video_dir, img_dir, img_num=20, img_expand_name=".bmp", skip_frame=50):
        self.video_dir = video_dir
        self.img_dir = img_dir
        self.skip_frame = skip_frame
        self.img_num = img_num
        self.img_expand_name = img_expand_name

    def write_imgs(self):
        for video_name in os.listdir(self.video_dir):
            self.process_video(video_name)

    def process_video(self, video_name):
        video_path = os.path.join(self.video_dir, video_name)
        img_sub_dir = os.path.join(self.img_dir, video_name.split(".")[0])
        if not os.path.exists(img_sub_dir):
            os.mkdir(img_sub_dir)

        print(f"开始处理视频{video_name}...")
        cap = cv2.VideoCapture(video_path)
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        video_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        video_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        print(f"该视频的fps:{video_fps}\tsize:{video_size}\tframe:{video_frame}")
        if not cap.isOpened():
            print("检查路径名")
        cnt = 0
        img_count = 0
        while 1:
            ret, frame = cap.read()
            cnt += 1
            if cnt % self.skip_frame == 0:
                img_count += 1
                img_name = f"{img_count:0>5d}" + self.img_expand_name
                img_path = os.path.join(img_sub_dir, img_name)
                cv2.imwrite(img_path, frame)

            if not ret:
                break
        print(f"{video_name} 处理结束")


if __name__ == '__main__':
    video_dir = "/Users/lizhen/pythonProject/weathon_package/data/input_videos"
    img_dir = '/Users/lizhen/pythonProject/weathon_package/data/out_imgs'
    vi = Video2Img(video_dir, img_dir)
    vi.write_imgs()
