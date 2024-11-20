import argparse
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from utils import get_data

# 获取命令行参数
def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.jpg", help="Path to output text file")
    parser.add_argument("--language", type=str, default="english", help="Language for ASCII characters")
    parser.add_argument("--mode", type=str, default="standard", help="Mode for ASCII character set")
    parser.add_argument("--background", type=str, default="black", choices=["black", "white"], help="Background color")
    parser.add_argument("--num_cols", type=int, default=300, help="Number of characters for output's width")
    parser.add_argument("--scale", type=int, default=2, help="Upsize output")
    return parser.parse_args()

# 获取背景颜色代码
def get_background_code(background):
    if background == "white":
        return (255, 255, 255)
    return (0, 0, 0)

# 计算图像分块尺寸
def calculate_cell_size(image_width, image_height, num_cols, scale):
    cell_width = image_width / num_cols
    cell_height = scale * cell_width
    num_rows = int(image_height / cell_height)
    return cell_width, cell_height, num_rows

# 处理分块数量超出图像尺寸的情况
def handle_excessive_cells(width, height, num_cols, num_rows):
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Using default settings.")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    return num_cols, num_rows

# 绘制ASCII字符图像
def draw_ascii_image(image, draw, char_list, num_chars, num_cols, num_rows, cell_width, cell_height, char_width, char_height, font):
    for i in range(num_rows):
        for j in range(num_cols):
            partial_image = image[int(i * cell_height):min(int((i + 1) * cell_height), image.shape[0]),
                                  int(j * cell_width):min(int((j + 1) * cell_width), image.shape[1]), :]
            partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
            partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
            char = char_list[min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
            draw.text((j * char_width, i * char_height), char, fill=partial_avg_color, font=font)

# 主函数
def main():
    # 获取参数
    opt = get_args()

    # 设置背景颜色代码
    bg_code = get_background_code(opt.background)

    # 获取字符集、字体等数据
    char_list, font, sample_character, scale = get_data(opt.language, opt.mode)
    num_chars = len(char_list)

    # 读取图像并转换为RGB格式
    image = cv2.imread(opt.input, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 计算图像分块尺寸
    cell_width, cell_height, num_rows = calculate_cell_size(image.shape[1], image.shape[0], opt.num_cols, scale)
    num_cols = opt.num_cols

    # 处理分块数量超出图像尺寸的情况
    num_cols, num_rows = handle_excessive_cells(image.shape[1], image.shape[0], num_cols, num_rows)

    # 计算输出图像尺寸
    char_width, char_height = font.getsize(sample_character)
    out_width = char_width * num_cols
    out_height = scale * char_height * num_rows

    # 创建输出图像并绘制ASCII字符
    out_image = Image.new("RGB", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)
    draw_ascii_image(image, draw, char_list, num_chars, num_cols, num_rows, cell_width, cell_height, char_width, char_height, font)

    # 剪裁输出图像并保存
    if opt.background == "white":
        cropped_image = ImageOps.invert(out_image).getbbox()
    else:
        cropped_image = out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image.save(opt.output)

# 启动程序
if __name__ == '__main__':
    main()
