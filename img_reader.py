from PIL import Image
from pytesseract import pytesseract as ptess
import os
import re

img_ext = ['jpg, png']
classtype = ['전선', '전필', '일선', '교양', '논문']

def img2str(img):
    txt = ptess.image_to_string(img, lang="Hangul")
    txt = txt.replace(" ", "")
    class_list = txt.split('\n')
    class_list = [i for i in class_list if len(i) > 1]
    # 스샷에 별과 다른 숫자가 안나오는게 중요
    return class_list

def str2

def process_img(file_path):
    for filename in os.listdir(file_path):
        if any(x in filename for x in img_ext):
            img = Image.open(filename)
            text = img2str(img)

def main():
    #file_path = './table_images'
    img = Image.open("./table_images/linetable3.png")
    result = img2str(img)
    for line in result:
        print(line)

if __name__ == '__main__':
    main()