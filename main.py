import tkinter.filedialog as tkdialog
import tkinter.messagebox
from tkinter import *

from cv2 import cv2
import moviepy
import moviepy.video.io.ImageSequenceClip
from PIL import Image, ImageTk
from moviepy.audio.fx.volumex import volumex
from moviepy.editor import *

from file_utils import FileUtils
from img_utils import ImgUtils
from tts.restful.tts_ali import TTS

file_dir = None
text_title = None
text_edit = None
text_select = None
text_submit = None


class MovieEditor:
    win = Tk()

    # 重现环境 conda env create -f environment.yml
    @staticmethod
    def pics2video(source_dir, resized_dir, audio_path_dub, audio_path_bg, output_path, resize_dim):
        frames_name = sorted(os.listdir(source_dir))
        for img_name in frames_name:  # resize视频 moviepy要求所有图片统一尺寸
            if img_name.endswith(".jpeg") or img_name.endswith(".jpg") or img_name.endswith(".png"):
                img = ImgUtils.resize_blur(cv2.imread(source_dir + img_name), resize_dim)
                cv2.imwrite(resized_dir + img_name, img)
        resized_path = [resized_dir + frame_name for frame_name in frames_name if
                        frame_name.endswith(".jpeg") or frame_name.endswith(".jpg") or frame_name.endswith(".png")]

        audio_dub = AudioFileClip(audio_path_dub)  # 台词配音
        dur = int(audio_dub.duration) + 7  # 台词总时长
        audio_bg = AudioFileClip(audio_path_bg).subclip(3, 3 + dur)  # 背景音总时长
        audio_bg_minus = volumex(audio_bg, [0.2, 0.2])  # 背景音音量降低
        audio_final = CompositeAudioClip([audio_dub, audio_bg_minus])  # 合并音频(注意 此处不是音频拼接 属于音频叠加)

        fps_count = len(resized_path) / dur  # 根据时长计算每张图片帧率

        video_clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(resized_path, fps=fps_count)
        # video_clip2 = video_clip.fl_time(lambda t: 1 + sin(t))
        # video_clip2 = video_clip.fl(MovieEditor.scroll)
        video = video_clip.set_audio(audio_final)  # 设置音频
        video.write_videofile(output_path,
                              codec='libx264',
                              rewrite_audio=True,
                              audio=True,
                              audio_codec='aac',
                              temp_audiofile='temp/temp-audio.m4a',
                              remove_temp=False)  # 导出合成好的视频

    @staticmethod
    def start_img_to_video(title, text_dub, img_list_dir):
        # 音频(因语音合成缺陷 所以部分文字需要调整读音)
        text_audio = "<speak><break time=\"1600ms\"/> <break time=\"700ms\"/>" + text_dub + " <break time=\"200ms\"/></speak>"
        # 字幕
        token_path = 'tts/restful/token/token_json.txt'

        img_src_dir = img_list_dir
        img_rsd_dir = 'res/img/resized/'

        audio_dub_dir = 'res/music/dub/'
        audio_dub_mp3_file_path = 'res/music/dub/audio.mp3'
        audio_dub_mp3_name = 'audio.mp3'
        audio_bg_mp3_file_path = 'res/music/bg/huankuai01.mp3'

        video_output_mp4_file_path = img_list_dir + title + '.mp4'
        video_output_mp4_dim = (640, 360)  # 视频尺寸

        # FileUtils.clear_image(src_dir)
        # Spider.start("https://www.huxiu.com/article/569468.html", src_dir)

        FileUtils.clear_image(img_rsd_dir)  # 删除之前resize后的图片文件
        FileUtils.clear_audio(audio_dub_dir)  # 删除之前生成的配音
        print("配音生成中...")
        TTS.create_audio(text_audio, audio_dub_dir, token_file_path=token_path)
        print("配音生成完成")
        FileUtils.rename_audio(audio_dub_dir, audio_dub_mp3_name)
        print("图片配音合成中...")
        MovieEditor.pics2video(img_src_dir,
                               img_rsd_dir,
                               audio_dub_mp3_file_path,
                               audio_bg_mp3_file_path,
                               video_output_mp4_file_path,
                               video_output_mp4_dim
                               )
        print("图片配音合成完成")
        print("视频生成完成\n" + ">>>>>>" + title)
        tkinter.messagebox.showwarning(title='成功', message='视频合成完成:\n' + video_output_mp4_file_path)

    @staticmethod
    def init():
        sw = MovieEditor.win.winfo_screenwidth()
        # 得到屏幕宽度
        sh = MovieEditor.win.winfo_screenheight()
        # 得到屏幕高度
        ww = 200
        wh = 600
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        # win.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        MovieEditor.win.title("视频生成")
        global text_title
        global text_edit
        global text_select
        global text_submit
        text_title = Entry(MovieEditor.win, bd=1, width=46)
        text_title.grid(row=0, column=0, columnspan=4)
        text_edit = Text(MovieEditor.win, width=60, height=10)
        text_edit.grid(row=1, column=0, columnspan=4)
        text_select = Button(MovieEditor.win, text="选择图片", command=MovieEditor.call)
        text_select.grid(row=2, column=0, columnspan=2)
        text_submit = Button(MovieEditor.win, text="生成视频", command=MovieEditor.submit)
        text_submit.grid(row=2, column=2, columnspan=2)
        MovieEditor.win.mainloop()

    @staticmethod
    def load_img(row_index, column_index, item):
        # 打开图片
        # resize()：示例图片太大，这里缩小一些。
        img = Image.open(item).resize((100, 56))

        # 引用：添加一个Label，用来存储图片。使用PanedWindow也行。
        panel = Label(master=MovieEditor.win)
        panel.photo = ImageTk.PhotoImage(img)  # 将原本的变量photo改为panel.photo

        # 图片用Label来显示，参数master改不改为panel都行，这里就不改了。
        # 注意：参数image改为panel.photo
        print("row_index:" + str(row_index) + ",column_index:" + str(column_index))
        Label(master=MovieEditor.win, image=panel.photo).grid(row=row_index, column=column_index)

    @staticmethod
    def call():
        global file_dir
        file_dir = tkdialog.askdirectory() + "/"

        # 使用for循环添加图片，enumerate：获取元素与其索引值
        ls = os.listdir(file_dir)
        FileUtils.clear_image_dir(file_dir)
        for index, f_name in enumerate(ls):
            if f_name.endswith(".jpeg") or f_name.endswith(".jpg") or f_name.endswith(".png"):
                f_path = os.path.join(file_dir, f_name)
                print("index:" + str(index) + ",f_path:" + str(f_path))
                MovieEditor.load_img(int(index / 4 + 3), int(index % 4), f_path)  # 执行函数

    @staticmethod
    def submit():
        global file_dir
        global text_title
        global text_edit
        global text_select
        global text_submit
        title = text_title.get()
        dub = text_edit.get("1.0", "end")
        if len(title.strip()) != 0 and len(dub.strip()) != 0:
            print(title.strip())
            print(dub.strip())
            tkinter.messagebox.showwarning(title='视频合成', message='点击OK 开始合成')
            MovieEditor.start_img_to_video(title.strip(), dub.strip(), file_dir)
        else:
            tkinter.messagebox.showwarning(title='错误', message='请填写标题或内容')


MovieEditor.init()
