import argparse
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps

def get_args():
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.mp4", help="Path to input video")
    parser.add_argument("--output", type=str, default="data/output.mp4", help="Path to output video")
    parser.add_argument("--mode", type=str, default="complex", choices=["simple", "complex"],
                        help="10 or 70 different characters")
    parser.add_argument("--background", type=str, default="black", choices=["black", "white"],
                        help="background's color")
    parser.add_argument("--num_cols", type=int, default=100, help="number of character for output's width")
    parser.add_argument("--scale", type=int, default=1, help="upsize output")
    parser.add_argument("--fps", type=int, default=0, help="frame per second")
    parser.add_argument("--overlay_ratio", type=float, default=0.2, help="Overlay width ratio")
    args = parser.parse_args()
    return args

def get_char_list(mode):
    if mode == "simple":
        return '@%#*+=-:. '
    else:
        return "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def get_background_color(background):
    if background == "white":
        return (255, 255, 255)
    else:
        return (0, 0, 0)

def calculate_fps(cap, fps_input):
    if fps_input == 0:
        return int(cap.get(cv2.CAP_PROP_FPS))
    return fps_input

def process_frame(frame, num_cols, char_list, font, bg_color):
    height, width, _ = frame.shape
    cell_width = width / num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)

    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Using default settings.")
        cell_width = 6
        cell_height = 12
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)

    char_width, char_height = font.getsize("A")
    out_width = char_width * num_cols
    out_height = 2 * char_height * num_rows
    out_image = Image.new("RGB", (out_width, out_height), bg_color)
    draw = ImageDraw.Draw(out_image)

    num_chars = len(char_list)
    for i in range(num_rows):
        for j in range(num_cols):
            partial_image = frame[int(i * cell_height):min(int((i + 1) * cell_height), height),
                                  int(j * cell_width):min(int((j + 1) * cell_width), width), :]
            partial_avg_color = np.sum(np.sum(partial_image, axis=0), axis=0) / (cell_height * cell_width)
            partial_avg_color = tuple(partial_avg_color.astype(np.int32).tolist())
            char = char_list[min(int(np.mean(partial_image) * num_chars / 255), num_chars - 1)]
            draw.text((j * char_width, i * char_height), char, fill=partial_avg_color, font=font)

    return out_image

def main():
    opt = get_args()
    char_list = get_char_list(opt.mode)
    bg_color = get_background_color(opt.background)
    font = ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=int(10 * opt.scale))
    cap = cv2.VideoCapture(opt.input)
    fps = calculate_fps(cap, opt.fps)

    out = None
    while cap.isOpened():
        flag, frame = cap.read()
        if not flag:
            break

        out_image = process_frame(frame, opt.num_cols, char_list, font, bg_color)

        if opt.background == "white":
            cropped_image = ImageOps.invert(out_image).getbbox()
        else:
            cropped_image = out_image.getbbox()

        out_image = out_image.crop(cropped_image)
        out_image = np.array(out_image)

        if out is None:
            out = cv2.VideoWriter(opt.output, cv2.VideoWriter_fourcc(*"XVID"), fps,
                                  (out_image.shape[1], out_image.shape[0]))

        if opt.overlay_ratio:
            height, width, _ = out_image.shape
            overlay = cv2.resize(frame, (int(width * opt.overlay_ratio), int(height * opt.overlay_ratio)))
            out_image[height - int(height * opt.overlay_ratio):, width - int(width * opt.overlay_ratio):, :] = overlay

        out.write(out_image)

    cap.release()
    if out:
        out.release()

if __name__ == '__main__':
    main()