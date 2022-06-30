import cv2


class ImgUtils:
    @staticmethod
    def center_crop(img, dim):
        """Returns center cropped image
        Args:
        img: image to be center cropped
        dim: dimensions (width, height) to be cropped
        """
        img_blur = cv2.GaussianBlur(img, (85, 85), 0)
        width, height = img_blur.shape[1], img_blur.shape[0]

        # process crop width and height for max available dimension
        crop_width = dim[0] if dim[0] < img_blur.shape[1] else img_blur.shape[1]
        crop_height = dim[1] if dim[1] < img_blur.shape[0] else img_blur.shape[0]
        mid_x, mid_y = int(width / 2), int(height / 2)
        cw2, ch2 = int(crop_width / 2), int(crop_height / 2)
        crop_img = img_blur[mid_y - ch2:mid_y + ch2, mid_x - cw2:mid_x + cw2]
        # 设置画布绘制区域并复制
        crop_img[0: mid_y, 0:mid_x] = img
        return crop_img

    @staticmethod
    def resize_blur(img, dim):  # 居中填充高斯模糊背景
        width, height = img.shape[1], img.shape[0]
        # 设置新的图片分辨率框架
        width_new = dim[0]
        height_new = dim[1]
        # 判断图片的长宽比率
        if width / height >= width_new / height_new:
            img_resize = cv2.resize(img, (width_new, int(height * width_new / width)))
        else:
            img_resize = cv2.resize(img, (int(width * height_new / height), height_new))
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        img_blur_bg = cv2.GaussianBlur(resized, (0, 0), 40)
        img_resize_width = img_resize.shape[1]
        img_blur_bg_width = img_blur_bg.shape[1]
        img_resize_height = img_resize.shape[0]
        img_blur_bg_height = img_blur_bg.shape[0]
        diff_width = int((img_blur_bg_width - img_resize_width) / 2)
        diff_height = int((img_blur_bg_height - img_resize_height) / 2)
        img_blur_bg[diff_height:img_resize_height + diff_height, diff_width:img_resize_width + diff_width] = img_resize
        return img_blur_bg

    @staticmethod
    def resize_keep_aspectratio(image_src, dst_size):
        src_h, src_w = image_src.shape[:2]
        print(src_h, src_w)
        dst_h, dst_w = dst_size

        # 判断应该按哪个边做等比缩放
        h = dst_w * (float(src_h) / src_w)  # 按照ｗ做等比缩放
        w = dst_h * (float(src_w) / src_h)  # 按照h做等比缩放

        h = int(h)
        w = int(w)

        if h <= dst_h:
            image_dst = cv2.resize(image_src, (dst_w, int(h)))
        else:
            image_dst = cv2.resize(image_src, (int(w), dst_h))

        h_, w_ = image_dst.shape[:2]
        print(h_, w_)

        top = int((dst_h - h_) / 2)
        down = int((dst_h - h_ + 1) / 2)
        left = int((dst_w - w_) / 2)
        right = int((dst_w - w_ + 1) / 2)

        value = [0, 0, 0]
        border_type = cv2.BORDER_CONSTANT
        image_dst = cv2.copyMakeBorder(image_dst, top, down, left, right, border_type, None, value)
        return image_dst

# image_src = cv2.imread("res/img/img_2.png")
# dst_size = (360, 640)
# img = ImgUtils.resize_keep_aspectratio(image_src, dst_size)
# cv2.imwrite("222.jpg", image_dst)

# crop_img = ImgUtils.resize_blur(cv2.imread("res/img/source/img_2.png"), (640, 360))
# cv2.imwrite("crop_img.jpg", crop_img)
