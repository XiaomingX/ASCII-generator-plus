import argparse
import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps

def get_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser("Image to ASCII")
    parser.add_argument("--input", type=str, default="data/input.mp4", help="Path to input video")
    parser.add_argument("--output", type=str, default="data/output.mp4", help="Path to output video")
    parser.add_argument("--mode", type=str, default="simple", choices=["simple", "complex"],
                        help="10 or 70 different characters")
    parser.add_argument("--background", type=str, default="white", choices=["black", "white"],
                        help="Background color")
    parser.add_argument("--num_cols", type=int, default=100, help="Number of characters for output width")
    parser.add_argument("--scale", type=int, default=1, help="Scale factor for output size")
    parser.add_argument("--fps", type=int, default=0, help="Frames per second for output video")
    parser.add_argument("--overlay_ratio", type=float, default=0.2, help="Overlay width ratio")
    return parser.parse_args()

def get_char_list(mode):
    """
    Return character list based on mode.
    """
    if mode == "simple":
        return '@%#*+=-:. '
    else:
        return "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def initialize_font(scale):
    """
    Initialize font for ASCII drawing.
    """
    return ImageFont.truetype("fonts/DejaVuSansMono-Bold.ttf", size=int(10 * scale))

def get_video_properties(video_path, fps):
    """
    Capture video and get video properties like FPS and frame dimensions.
    """
    cap = cv2.VideoCapture(video_path)
    if fps == 0:
        fps = int(cap.get(cv2.CAP_PROP_FPS))
    return cap, fps

def calculate_cells(image, num_cols):
    """
    Calculate the dimensions of each ASCII cell.
    """
    height, width = image.shape
    cell_width = width / num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    return cell_width, cell_height, num_rows

def create_ascii_image(image, char_list, font, num_cols, cell_width, cell_height, bg_code):
    """
    Create an ASCII representation of the image.
    """
    height, width = image.shape
    num_chars = len(char_list)
    char_width, char_height = font.getsize("A")
    num_rows = int(height / cell_height)

    out_width = char_width * num_cols
    out_height = char_height * num_rows
    out_image = Image.new("L", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)

    for i in range(num_rows):
        line = ""
        for j in range(num_cols):
            x1, y1 = int(j * cell_width), int(i * cell_height)
            x2, y2 = min(int((j + 1) * cell_width), width), min(int((i + 1) * cell_height), height)
            avg_color = int(np.mean(image[y1:y2, x1:x2]))
            char_idx = min(avg_color * num_chars // 255, num_chars - 1)
            line += char_list[char_idx]
        draw.text((0, i * char_height), line, fill=255 - bg_code, font=font)

    cropped_image = out_image.getbbox()
    return out_image.crop(cropped_image)

def overlay_original_frame(ascii_frame, original_frame, overlay_ratio):
    """
    Overlay the original video frame on the ASCII image.
    """
    height, width, _ = ascii_frame.shape
    overlay = cv2.resize(original_frame, (int(width * overlay_ratio), int(height * overlay_ratio)))
    ascii_frame[height - overlay.shape[0]:, width - overlay.shape[1]:, :] = overlay
    return ascii_frame

def process_video(input_path, output_path, char_list, font, num_cols, scale, fps, overlay_ratio, bg_code):
    """
    Process video frame by frame and convert each frame to ASCII.
    """
    cap, fps = get_video_properties(input_path, fps)
    out = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cell_width, cell_height, num_rows = calculate_cells(gray_image, num_cols)

        ascii_image = create_ascii_image(gray_image, char_list, font, num_cols, cell_width, cell_height, bg_code)
        ascii_image = cv2.cvtColor(np.array(ascii_image), cv2.COLOR_GRAY2BGR)

        if out is None:
            out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"XVID"), fps,
                                  (ascii_image.shape[1], ascii_image.shape[0]))

        if overlay_ratio:
            ascii_image = overlay_original_frame(ascii_image, frame, overlay_ratio)

        out.write(ascii_image)

    cap.release()
    out.release()

def main():
    """
    Main function to execute the video conversion.
    """
    args = get_args()
    char_list = get_char_list(args.mode)
    font = initialize_font(args.scale)
    bg_code = 255 if args.background == "white" else 0
    process_video(args.input, args.output, char_list, font, args.num_cols, args.scale, args.fps, args.overlay_ratio, bg_code)

if __name__ == "__main__":
    main()