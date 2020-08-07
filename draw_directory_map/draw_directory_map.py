from draw_directory_map_config import *
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont


class File:
    def __init__(self, path, type, layer, len, parent_node):
        self.name = os.path.basename(path)
        self.path = path
        self.type = type
        self.layer = layer
        self.len = len
        self.file_names = []
        self.parent_node = parent_node
        self.readme_path = None
        if self.type is "file_pack":
            self.file_names.append(self.name)

        self.sx = self.layer * (WB_WIDTH_BETWEEN_CELLS + WIDTH) + WB_LEFT_PADDING
        self.sy = 0
        self.ex = self.sx + WIDTH
        self.ey = 0

        self.tsx = self.sx
        self.tsy = 0
        self.tex = self.ex
        self.tey = 0

        self.bsx = self.sx
        self.bsy = 0
        self.bex = self.ex
        self.bey = 0

        self.psy = 0
        self.pey = 0

    def set_position(self, parent_sy, parent_ey):
        self.psy = parent_sy
        self.pey = parent_ey

        self.sy = self.pey + WB_HEIGHT_BETWEEN_CELLS
        if self.type is "dir":
            self.ey = self.sy + STANDARD_HEIGHT
        elif self.type is "file_pack":
            self.ey = self.sy + max(STANDARD_HEIGHT,
                                    TITLE_HEIGHT + len(self.file_names) * BODY_TEXT_INTERVAL + BODY_UPPER_PADDING * 2)
        self.tsy = self.sy
        self.tey = self.tsy + TITLE_HEIGHT
        self.bsy = self.tey
        self.bey = self.bsy
        return self.sy, self.ey

    def draw(self, white_board):
        # 직선 먼저 연결
        if self.parent_node is None:
            cv2.line(white_board, (self.tsx + LINE_PADDING_X, self.tsy + LINE_PADDING_Y),
                     (self.tsx + LINE_PADDING_X - WB_WIDTH_BETWEEN_CELLS, self.tsy + LINE_PADDING_Y),
                     (0, 0, 0), 2)
        else:
            if self.parent_node.return_len() == self.len:  # 부모 파일과 같은 len
                cv2.line(white_board, (self.tsx+LINE_PADDING_X, self.tsy+LINE_PADDING_Y),
                         (self.tsx + LINE_PADDING_X - WB_WIDTH_BETWEEN_CELLS, self.tsy+LINE_PADDING_Y),
                         (0, 0, 0), 2)
            else:  # 부모 파일 아래로 떨어져있다.
                curve_x_point = self.tsx + LINE_PADDING_X - int(WB_WIDTH_BETWEEN_CELLS/2)
                cv2.line(white_board, (self.tsx + LINE_PADDING_X, self.tsy + LINE_PADDING_Y),
                         (curve_x_point, self.tsy + LINE_PADDING_Y),
                         (0, 0, 0), 2)

                cv2.line(white_board, (curve_x_point, self.tsy + LINE_PADDING_Y - (self.sy - self.psy)),
                         (curve_x_point, self.tsy + LINE_PADDING_Y),
                         (0, 0, 0), 2)

        title_text_position = [self.tsx+TITLE_TEXT_LEFT_PADDING,
                              self.tsy+TITLE_TEXT_UPPER_PADDING,
                              self.tex-TITLE_TEXT_LEFT_PADDING,
                              None]
        body_text_position = [self.bsx + BODY_LEFT_PADDING*4,
                              self.bsy + BODY_UPPER_PADDING,
                              self.bex - BODY_LEFT_PADDING*4,
                              self.bey]
        if self.type is "dir":
            color = DIR_COLOR
            cv2.rectangle(white_board, (self.sx, self.sy), (self.ex, self.ey), color, -1)
            color = TITLE_COLOR
            cv2.rectangle(white_board, (self.tsx, self.tsy), (self.tex, self.tey), color, -1)
            white_board, wr = write_text_to_image(white_board, self.name, title_text_position, TITLE_HEIGHT_BETWEEN_TEXT,
                                              TITLE_TEXT_MAXLEN, TITLE_TEXT_MAXLINE,
                                              TITLE_FONT, TITLE_FONT_SIZE, TITLE_TEXT_COLOR)
            if self.readme_path is not None:  # readme 가 있으면 바디에 적어준다.
                wrote_counter = 0
                f = open(self.readme_path, encoding="UTF-8")
                titles = ["", ""]
                for line in f:
                    if line.startswith("# "):
                        wrote_counter += 1
                        titles[0] = line
                    elif line.startswith("## "):
                        titles[1] = line
                        wrote_counter += 1
                    if wrote_counter < 2 and titles[0] == "":
                        titles[0] = line
                        wrote_counter += 1
                name = "from " + os.path.basename(self.readme_path)
                form = "{:>"+str(BODY_TEXT_MAXLEN)+"}"
                titles.append(form.format(name))
                interval = 0
                body_text_position_copy = body_text_position.copy()
                for i in range(3):
                    white_board, wr = write_text_to_image(white_board, titles[i], body_text_position_copy,
                                                      BODY_TEXT_INTERVAL, BODY_TEXT_MAXLEN, README_TEXT_MAXLINE,
                                                      BODY_FONT, BODY_FONT_SIZE, BODY_TEXT_COLOR)
                    interval = interval + wr
                    body_text_position_copy[1] = body_text_position[1] + interval * BODY_TEXT_INTERVAL
        elif self.type is "file":
            color = FILE_COLOR
            cv2.rectangle(white_board, (self.sx, self.sy), (self.ex, self.ey), color, -1)
            color = TITLE_COLOR
            cv2.rectangle(white_board, (self.tsx, self.tsy), (self.tex, self.tey), color, -1)
            white_board, wr = write_text_to_image(white_board, self.name, title_text_position, TITLE_HEIGHT_BETWEEN_TEXT,
                                TITLE_TEXT_MAXLEN, TITLE_TEXT_MAXLINE,
                                TITLE_FONT, TITLE_FONT_SIZE, TITLE_TEXT_COLOR)

        elif self.type is "file_pack":
            color = FILE_PACK_COLOR
            cv2.rectangle(white_board, (self.sx, self.sy), (self.ex, self.ey), color, -1)
            color = TITLE_COLOR
            cv2.rectangle(white_board, (self.tsx, self.tsy), (self.tex, self.tey), color, -1)
            white_board, wr = write_text_to_image(white_board, "source", title_text_position, TITLE_HEIGHT_BETWEEN_TEXT,
                                TITLE_TEXT_MAXLEN, TITLE_TEXT_MAXLINE,
                                TITLE_FONT, TITLE_FONT_SIZE, TITLE_TEXT_COLOR)
            interval=0
            body_text_position_copy = body_text_position.copy()
            for i in range(len(self.file_names)):
                white_board, wr = write_text_to_image(white_board, "* " + self.file_names[i], body_text_position_copy,
                                                      BODY_TEXT_INTERVAL, BODY_TEXT_MAXLEN,
                                    BODY_TEXT_MAXLINE, BODY_FONT, BODY_FONT_SIZE, BODY_TEXT_COLOR, True)
                interval = interval + wr
                body_text_position_copy[1] = body_text_position[1] + interval * BODY_TEXT_INTERVAL
        return white_board

    def add_file(self, file):
        self.file_names.append(file)

    def return_layer_file_list(self):
        return self.layer, len(self.file_names)

    def return_long_layer(self):
        return self.len, self.layer

    def return_pos(self):
        return self.sx

    def return_len(self):
        return self.len

    def append_readme_path(self, abs_path):
        self.readme_path = abs_path

    def return_name(self):
        return self.name

    def return_path(self):
        return self.path


def write_text_to_image(image, text, position_list, dy, text_max_len, text_max_line, font, size, color, under_line=False):
    sx, sy, ex, ey = position_list
    pill_image = Image.fromarray(image)
    draw_image = ImageDraw.Draw(pill_image)
    left_c = text_max_len
    wrote_line = 0
    temp = []
    wrote = False
    for i in range(len(text)):
        if wrote_line >= text_max_line:
            break
        if i == len(text)-1:
            wrote = True
        c = text[i]
        if ord('가') <= ord(c) <= ord('힣'):
            c_size = 2
        else:
            c_size = 1
        if left_c - c_size >= 0:
            temp.append(c)
            left_c -= c_size
        else:
            draw_image.text((sx, sy + wrote_line * dy), ''.join(temp),
                            font=ImageFont.truetype(font, size), fill=color)
            if under_line:
                draw_image.line([sx,
                                 sy + wrote_line * dy + BODY_UNDERLINE_PADDING,
                                 ex,
                                 sy + wrote_line * dy + BODY_UNDERLINE_PADDING],
                                fill=BODY_UNDERLINE_COLOR, width=1)
            temp = [c]
            left_c = text_max_len - c_size
            wrote_line += 1
        if wrote:  # 줄 못줄이나
            draw_image.text((sx, sy + wrote_line * dy), ''.join(temp),
                            font=ImageFont.truetype(font, size), fill=color)
            if under_line:
                draw_image.line([sx,
                                 sy + wrote_line * dy + BODY_UNDERLINE_PADDING,
                                 ex,
                                 sy + wrote_line * dy + BODY_UNDERLINE_PADDING],
                                fill=BODY_UNDERLINE_COLOR, width=1)
            wrote_line += 1
    return np.array(pill_image), wrote_line


def go_to_dir(path, file_list, root_len, root_layer, parent):
    long = 0
    child_max_layer = root_layer
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)) and file not in DIRECTORY_IGNORED:
            child_dir = File(os.path.join(path, file), "dir", root_layer+1, root_len + long, parent)
            file_list.append(child_dir)
            _, child_long, child_layer = go_to_dir(os.path.join(path, file),
                                                   file_list, root_len + long, root_layer+1, child_dir)
            child_max_layer = max(child_max_layer, child_layer)
            long = long + child_long

    make_pack = False
    pack = 0
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            child_max_layer = max(child_max_layer, root_layer+1)
            if file.lower()[:7] == "readme.":
                parent.append_readme_path(os.path.join(path, file))
            if DISPLAY_ALL_SOURCE_CODE:
                py = File(os.path.join(path, file), "file", root_layer+1, root_len + long, parent)
                file_list.append(py)
                long = long + 1
            elif not make_pack:
                pack = File(os.path.join(path, file), "file_pack", root_layer + 1, root_len + long, parent)
                file_list.append(pack)
                long = long + 1
                make_pack = True
            else:
                pack.add_file(file)
    if long < 1:
        return file_list, 1, child_max_layer
    return file_list, long, child_max_layer


def draw(tree_map, long, total_layer):
    sy_ey_list = [[0, 0] for _ in range(total_layer)]  # psy, pey, long_count
    if DRAW_DENSE_MAP:  # 미제작
        white_board_size = (long * STANDARD_HEIGHT + WB_UPPER_PADDING * 2,
                            total_layer * (WIDTH + WB_WIDTH_BETWEEN_CELLS) + WB_LEFT_PADDING * 2, 3)
        white_board = np.zeros(white_board_size, np.uint8)
        white_board.fill(255)
        for i in range(len(tree_map)):
            c = tree_map[i]
            long, layer = c.return_long_layer()
            psy, pey = sy_ey_list[layer]
            psy, pey = c.set_position(psy, pey)
            sy_ey_list[layer] = [psy, pey]
            white_board = c.draw(white_board)
    else:
        long_previous = 0
        for i in range(len(tree_map)):
            c = tree_map[i]
            long, layer = c.return_long_layer()
            if long_previous != long:
                max_previous = max([a[1] for a in sy_ey_list])
                for j in range(len(sy_ey_list)):
                    sy_ey_list[j][1] = max_previous
                    long_previous = long
            psy, pey = sy_ey_list[layer]
            psy, pey = c.set_position(psy, pey)
            sy_ey_list[layer] = [psy, pey]
        max_height = max([sy_ey[1] for sy_ey in sy_ey_list])
        white_board_size = (max_height + WB_UPPER_PADDING * 2,
                            total_layer * (WIDTH + WB_WIDTH_BETWEEN_CELLS) + WB_LEFT_PADDING * 2, 3)
        white_board = np.zeros(white_board_size, np.uint8)
        white_board.fill(255)
        for i in range(len(tree_map)):
            c = tree_map[i]
            white_board = c.draw(white_board)
    plt.imshow(white_board)
    plt.show()
    return white_board


def draw_directory_tree(root_path):
    root_path = os.path.abspath(root_path)
    root = File(root_path, "dir", 0, 0, None)
    file_list = [root]
    file_list, long, layer = go_to_dir(path, file_list, root_len=0, root_layer=0, parent=root)
    return draw(file_list, long, layer+1)


if __name__ == "__main__":
    path = "D:/atom"
    red_square = "image_to_tree"
    directory_tree = draw_directory_tree(path)
    cv2.imwrite(os.path.join(path, os.path.basename(os.path.abspath(path))+"_map.jpg"), directory_tree)
