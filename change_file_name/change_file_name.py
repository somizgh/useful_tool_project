import os
import re
subtitles = ['psb','srt', 'ssa', 'ass', 'sub', 'sami', 'smil', 'smi', 'usf','vtt']
videos = ['mkv','avi','mp4','mpg','flv','wmv','asf','asx','ogm', 'ogv','mov']
images = ['ai','bmp','gif','jpg','jpeg','jpe','jfif','jp2','j2p','pcx','png','psd','tga','taga','tif']

def fill_number(file_list):
    num_size = len(str(len(file_list)))
    print(num_size)
    """
    for i in range(len(file_list)):
        file_list[i].

    """

    return file_list

def make_pattern(file_name):
    pattern = ""
    num_series = False
    for c in file_name:
        if '0'<= c <='9':
            if not num_series:
                pattern = pattern + "[0-9]+"
                num_series = True

        elif 'A' <= c <='z' or '가' <= c <= '힇':
            pattern = pattern + c
            num_series = False
        else:
            pattern = pattern + '\\'+ c
            print(pattern)
            num_series = False
    p = re.compile(pattern)
    return p

def find_pattern(path, option):
    files = os.listdir(path)
    files = fill_number(files)
    patterns=[]
    print(files)
    for i in range(len(files)):
        if len(patterns) == 0:
            patterns.append(make_pattern(files[i]))
        for j in range(len(patterns)):
            if patterns[j].match(files[i]) != None:
                break
            if j == len(patterns)-1:
                patterns.append(make_pattern(files[i]))
    print(patterns)


def change_file(path):
    return 0


if __name__ == "__main__":
    path = "E:/Ai_projects_data/atom_data/full_images/chrome_images"
    change_file(path)
    find_pattern(path,1)

