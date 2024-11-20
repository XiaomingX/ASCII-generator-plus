import argparse
import cv2
import numpy as np

def get_args():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description="将图像转换为 ASCII 字符画")
    parser.add_argument("--input", type=str, default="data/input.jpg", help="输入图像的路径")
    parser.add_argument("--output", type=str, default="data/output.txt", help="输出文本文件的路径")
    parser.add_argument("--mode", type=str, default="complex", choices=["simple", "complex"],
                        help="字符集模式：简单模式(10个字符)或复杂模式(70个字符)")
    parser.add_argument("--num_cols", type=int, default=150, help="输出字符画的宽度(列数)")
    return parser.parse_args()

def get_char_list(mode):
    """
    根据模式返回字符列表
    """
    if mode == "simple":
        return '@%#*+=-:. '
    else:
        return "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def convert_image_to_ascii(image, char_list, num_cols):
    """
    将图像转换为 ASCII 字符画
    """
    # 将图像转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 计算每个单元格的宽度和高度
    height, width = gray_image.shape
    cell_width = width / num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)

    # 检查列数和行数是否合适
    if num_cols > width or num_rows > height:
        print("列数或行数过多，使用默认设置")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    
    # 将图像转换为 ASCII 字符
    ascii_art = []
    num_chars = len(char_list)
    for i in range(num_rows):
        row = ""
        for j in range(num_cols):
            # 计算当前单元格的平均灰度值
            cell = gray_image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                              int(j * cell_width):min(int((j + 1) * cell_width), width)]
            avg_brightness = np.mean(cell)
            char_index = min(int(avg_brightness * num_chars / 255), num_chars - 1)
            row += char_list[char_index]
        ascii_art.append(row)
    
    return ascii_art

def save_ascii_art(ascii_art, output_path):
    """
    将 ASCII 字符画保存到文本文件
    """
    with open(output_path, 'w') as output_file:
        for row in ascii_art:
            output_file.write(row + "\n")

def main():
    # 获取命令行参数
    args = get_args()
    
    # 获取字符列表
    char_list = get_char_list(args.mode)
    
    # 读取输入图像
    image = cv2.imread(args.input)
    if image is None:
        print(f"无法加载图像：{args.input}")
        return

    # 将图像转换为 ASCII 字符画
    ascii_art = convert_image_to_ascii(image, char_list, args.num_cols)
    
    # 保存 ASCII 字符画到输出文件
    save_ascii_art(ascii_art, args.output)
    print(f"ASCII 字符画已保存到 {args.output}")

if __name__ == '__main__':
    main()