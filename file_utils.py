import os


class FileUtils:
    @staticmethod
    def clear_audio(music_list_path):
        ls = os.listdir(music_list_path)
        for i in ls:
            f_path = os.path.join(music_list_path, i)
            # 判断是否是一个目录,若是,则递归删除
            if os.path.isdir(f_path):
                FileUtils.clear_audio(f_path)
            else:
                os.remove(f_path)

    @staticmethod
    def clear_image(image_list_path):
        ls = os.listdir(image_list_path)
        for i in ls:
            f_path = os.path.join(image_list_path, i)
            # 判断是否是一个目录,若是,则递归删除
            if os.path.isdir(f_path):
                FileUtils.clear_audio(f_path)
            else:
                os.remove(f_path)

    @staticmethod
    def clear_image_dir(image_list_path):
        ls = os.listdir(image_list_path)
        for i in ls:
            f_path = os.path.join(image_list_path, i)
            # 判断是否是一个目录,若是,则递归删除
            if (f_path.endswith(".jpeg")) or (f_path.endswith(".jpg")) or (f_path.endswith(".png")):
                pass
            else:
                os.remove(f_path)

    @staticmethod
    def rename_audio(music_list_path, rename):
        music_file_list = os.listdir(music_list_path)
        for music_file_path in music_file_list:
            src = os.path.join(os.path.abspath(music_list_path), music_file_path)  # 原先的名字
            dst = os.path.join(os.path.abspath(music_list_path), rename)  # 根据自己的需要重新命名
            os.rename(src, dst)  # 重命名,覆盖原先的名字
