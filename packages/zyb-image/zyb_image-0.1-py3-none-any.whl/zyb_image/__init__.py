from PIL import Image, ImageFilter, ImageTk

open = Image.open

# 降噪滤波
EMBOSS = ImageFilter.EMBOSS
BLUR = ImageFilter.BLUR
CONTOUR = ImageFilter.CONTOUR
GaussianBlur = ImageFilter.GaussianBlur
SMOOTH = ImageFilter.SMOOTH
FIND_EDGES = ImageFilter.FIND_EDGES

# 冲采样滤波
BICUBIC = Image.BICUBIC
LANCZOS = Image.LANCZOS
NEAREST = Image.NEAREST
BILINEAR = Image.BILINEAR

# 图像翻转形式
FLIP_LEFT_RIGHT = Image.FLIP_LEFT_RIGHT
FLIP_TOP_BOTTOM = Image.FLIP_TOP_BOTTOM
ROTATE_90 = Image.ROTATE_90
ROTATE_180 = Image.ROTATE_180
ROTATE_270 = Image.ROTATE_270
TRANSPOSE = Image.TRANSPOSE
TRANSVERSE = Image.TRANSVERSE

# 图片变化方式
EXTENT = Image.EXTENT


def change(img):
    """
    转换图像为tk可用格式
    :param img: Image对象
    :return:
    """
    return ImageTk.PhotoImage(img)


__all__ = ["open",
           "EMBOSS", "BLUR", "CONTOUR", "GaussianBlur", "SMOOTH", "FIND_EDGES",
           "BICUBIC", "LANCZOS", "NEAREST", "BILINEAR",
           "FLIP_LEFT_RIGHT", "FLIP_TOP_BOTTOM", "ROTATE_90", "ROTATE_180", "ROTATE_270", "TRANSPOSE", "TRANSVERSE",
           "EXTENT"]



