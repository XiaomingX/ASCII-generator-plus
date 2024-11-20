import argparse
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps
from utils import get_data


def get_args():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="Path to input image")
    parser.add_argument("--output", type=str, default="data/output.jpg", help="Path to output image file")
    parser.add_argument("--language", type=str, default="english", help="Language for ASCII characters")
    parser.add_argument("--mode", type=str, default="standard", help="Mode for ASCII conversion")
    parser.add_argument("--background", type=str, default="black", choices=["black", "white"],
                        help="Background color for the output image")
    parser.add_argument("--num_cols", type=int, default=300, help="Number of characters for output's width")
    return parser.parse_args()


def preprocess_image(image_path, num_cols):
    """
    读取和预处理图像，将其转换为灰度图像。
    """
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray_image.shape
    cell_width = width / num_cols
    return gray_image, cell_width, height, width


def calculate_num_rows(height, cell_width, scale):
    """
    根据图像高度和单元格宽度计算行数。
    """
    cell_height = scale * cell_width
    num_rows = int(height / cell_height)
    return num_rows, cell_height


def create_output_image(char_list, font, sample_character, num_cols, num_rows, image, cell_width, cell_height, bg_code):
    """
    创建 ASCII 艺术图像。
    """
    num_chars = len(char_list)
    char_width, char_height = font.getsize(sample_character)
    out_width = char_width * num_cols
    out_height = char_height * num_rows
    out_image = Image.new("L", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    for i in range(num_rows):
        line = ""
        for j in range(num_cols):
            cell = image[int(i * cell_height):min(int((i + 1) * cell_height), image.shape[0]),
                         int(j * cell_width):min(int((j + 1) * cell_width), image.shape[1])]
            avg_brightness = np.mean(cell)
            char_index = min(int(avg_brightness / 255 * num_chars), num_chars - 1)
            line += char_list[char_index]
        draw.text((0, i * char_height), line, fill=255 - bg_code, font=font)

    return out_image


def crop_output_image(out_image, background):
    """
    根据背景颜色裁剪输出图像。
    """
    if background == "white":
        cropped_image = ImageOps.invert(out_image).getbbox()
    else:
        cropped_image = out_image.getbbox()
    return out_image.crop(cropped_image)


def main():
    # 获取参数
    args = get_args()

    # 设置背景颜色代码
    bg_code = 255 if args.background == "white" else 0

    # 获取字符列表、字体和缩放参数
    char_list, font, sample_character, scale = get_data(args.language, args.mode)

    # 预处理图像
    gray_image, cell_width, height, width = preprocess_image(args.input, args.num_cols)

    # 计算行数
    num_rows, cell_height = calculate_num_rows(height, cell_width, scale)

    # 如果列数或行数超出图像尺寸，使用默认设置
    if args.num_cols > width or num_rows > height:
        print("Too many columns or rows. Using default settings.")
        cell_width, cell_height = 6, 12
        args.num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    # 创建输出图像
    out_image = create_output_image(char_list, font, sample_character, args.num_cols, num_rows,
                                    gray_image, cell_width, cell_height, bg_code)

    # 裁剪输出图像
    cropped_image = crop_output_image(out_image, args.background)

    # 保存输出图像
    cropped_image.save(args.output)


if __name__ == "__main__":
    main()