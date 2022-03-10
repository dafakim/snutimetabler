from PIL import Image
from pytesseract import pytesseract as ptess
import os
import re

classtype = ['전선', '전필', '일선', '교양', '논문']

def img2str(img):
    txt = ptess.image_to_string(img, lang="Hangul")
    txt = txt.replace(" ", "")
    class_list = txt.split('\n')
    class_list = [i for i in class_list if len(i) > 1]
    # 스샷에 별과 다른 숫자가 안나오는게 중요
    return class_list

def str2dict(txt):
    cnt = 0
    payload = []
    #pattern = re.compile('^(0?[1-9]|1[0-2]):[0-5][0-9]$')
    for line in txt:
        if any(x in line for x in classtype):
            line = line.split("]")
            class_data = {
                "class_name": line[1]
            }
        elif '~' in line:
            day = line[0]
            match = re.findall('\d\d:\d\d', line)
            if len(match) < 2:
                return 0
            start = match[0]
            end = match[1]
            class_data["day"] = day
            class_data["start"] = start
            class_data["end"] = end
            payload.append(class_data)
        else:
            continue
    return payload

def process_img(file_path):
    img = Image.open(file_path)
    text = img2str(img)
    retdict = str2dict(text)
    return retdict

def main():
    filepath = "./table_images/linetable3.png"
    result = process_img(filepath)
    print(result)

if __name__ == '__main__':
    main()