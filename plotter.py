import plotly.express as px
import pandas as pd

HR_NANO = 3600000
DEFAULT_DATE = "1970-01-01 "
DATE_DICT = {"월":1, "화":2, "수":3, "목":4, "금":5}
SUB_DATE = {"월":' ', "화":'  ', "수":'   ', "목":'    ', "금":'     '}

def make_new_class(name, _class):
    new_dict = dict(Task=_class["day"], Start=DEFAULT_DATE+_class["start"]+":00",
        End=DEFAULT_DATE+_class["end"]+":00", Participants=name, ClassName=_class["class_name"])
    return new_dict

def remove_duplicate_task(txt_schedule):
    day = ''
    for _class in txt_schedule:
        if _class['Task'] == day:
            _class['Task'] = SUB_DATE[_class['Task']]
        else:
            day = _class['Task']
    return txt_schedule

def process_dictlist(dl):
    txt_schedule = []
    exist_classlist = []
    for student in dl:
        for _class in student["classes"]:
            name = student["name"]
            classname = _class["class_name"]
            if len(txt_schedule) < 1:
                new_class = make_new_class(name, _class)
                txt_schedule.append(new_class)
                exist_classlist.append(classname)
            elif classname in exist_classlist:
                for exist_class in txt_schedule:
                    if exist_class["ClassName"] == classname:
                        exist_class["Participants"] = exist_class["Participants"] + " " + name
            else:
                new_class = make_new_class(name, _class)
                txt_schedule.append(new_class)
                exist_classlist.append(classname)
    txt_schedule.sort(key=lambda x:x['Task'], reverse=True)
    txt_schedule = remove_duplicate_task(txt_schedule)
    return txt_schedule 

def calc_time(_class):
    hour = (int(_class["Start"][-8:-6])*60 + int(_class["End"][-8:-6])*60)
    minute = int(_class["Start"][-5:-3]) + int(_class["End"][-5:-3])
    total = (hour + minute) // 2
    new_hour = total // 60
    new_minute = total % 60
    return DEFAULT_DATE + str(new_hour) + ":" + str(new_minute) + ":" + "00"

def create_annotations(txt_schedule):
    annotations = []
    for _class in txt_schedule:
        time = calc_time(_class)
        anot_class = dict(x=time, y=_class["Task"], text=_class["Participants"], showarrow=False)
        annotations.append(anot_class)
    print(annotations)
    return annotations

def draw_schedule(txt_schedule):
    df = pd.DataFrame(txt_schedule)

    fig = px.timeline(df, x_start="Start", x_end="End", y="Task", range_x=[0, 39600000])
    fig.update_xaxes(tickformat="%H:%M", dtick=3600000)
    fig.update_yaxes(autorange="reversed")

    annotations = create_annotations(txt_schedule)
    fig.update_layout(annotations=annotations)

    fig.show()

if __name__ == '__main__':

    
    df = pd.DataFrame([
        dict(Task="월", Start="1970-01-01 10:00:00", End="1970-01-01 12:00:00", Participants="KDY, LCH", ClassName="시설원예최신과제"),
        dict(Task=" ", Start="1970-01-01 10:00:00", End="1970-01-01 12:00:00", Participants="KSY")
        ])

    fig = px.timeline(df, x_start="Start", x_end="End", y="Task", range_x=[0, 39600000])
    fig.update_xaxes(tickformat="%H:%M", dtick=3600000)
    fig.update_yaxes(autorange="reversed")

    annotations = []
    annotations.append(dict(x="1970-01-01 11:00:00", y="월", text="김대영, 이창협", showarrow=False))
    fig.update_layout(annotations=annotations)
    fig.show()
    