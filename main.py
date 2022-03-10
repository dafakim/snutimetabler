import img_reader as ir
import plotter
import os
import time
import json

img_ext = ['jpg', 'png']

def create_dictlist(dirpath):
    payload = []
    for filename in os.listdir(dirpath):
        if any(x in filename for x in img_ext):
            filepath = dirpath + '/' + filename
            class_list = ir.process_img(filepath)
            user_data = {"name":filename[0:3],"classes":class_list}
            payload.append(user_data)
    return payload


def main():
    dirpath = "./table_images"
    dict_list = create_dictlist(dirpath)
    txt_sched = plotter.process_dictlist(dict_list)
    plotter.draw_schedule(txt_sched)
    for _class in txt_sched:
        print(_class)
    
if __name__ == '__main__':
    main()