#encoding:utf-8

import tkinter,time,random
from math import*

root=tkinter.Tk(className='按左键改变位置，右键改变类型，中键退出')
cv=tkinter.Canvas(root,width=640,height=480,bg='black')
x,y=int(cv['width'])/2,int(cv['height'])/2
running=1
star_color=['#fcffc8','#d0f4ff','#d8ffd0','#fad8fe']
star_width=1
s_d=[[x,y,random.randrange(i*5,i*5+5),random.uniform(3,6),random.choice(star_color),star_width] for i in range(72)]
star=[cv.create_oval(s_d[i][0]-s_d[i][5]/2.0,s_d[i][1]-s_d[i][5]/2.0,
                     s_d[i][0]+s_d[i][5]/2.0,s_d[i][1]+s_d[i][5]/2.0,
                     fill=s_d[i][4],outline=s_d[i][4])
                     for i in range(len(s_d))]
s_type=5
def quit(event):
    global running
    running=0
    root.destroy()
root.bind('<Button-2>',quit)
def new_pos(event):
    global x,y
    x,y=event.x,event.y
root.bind('<Button-1>',new_pos)
def new_type(event):
    global s_type
    s_type+=1
    if s_type==len(type_):
        s_type=0
root.bind('<Button-3>',new_type)
def move_type(i,s_type):
    global type_
    type_=[[s_d[i][3]*cos(s_d[i][2]),s_d[i][3]*sin(s_d[i][2])],
           [s_d[i][3]*cos(s_d[i][2]),s_d[i][3]*cos(s_d[i][2])],
           [-s_d[i][3]*sin(s_d[i][2]),s_d[i][3]*sin(s_d[i][2])],
           [s_d[i][3]*tan(s_d[i][2]),s_d[i][3]*sin(s_d[i][2])],
           [s_d[i][3]*sin(s_d[i][2]),s_d[i][3]*tanh(s_d[i][2])],
           [s_d[i][3]*tanh(s_d[i][2]),s_d[i][3]*tan(s_d[i][2])]]
    cv.move(star[i],type_[s_type][0],type_[s_type][1])

def star_sky():
    for i in range(len(star)):
        move_type(i,s_type)
        if cv.bbox(star[i])[0]>int(cv['width']) or cv.bbox(star[i])[1]>int(cv['height']) or cv.bbox(star[i])[2]<0 or cv.bbox(star[i])[3]<0:
            cv.delete(star[i])
            s_d[i]=[x,y,random.randrange(i*10,i*10+10),random.uniform(3,6),random.choice(star_color),star_width]
            star[i]=cv.create_oval(s_d[i][0]-s_d[i][5]/2.0,s_d[i][1]-s_d[i][5]/2.0,s_d[i][0]+s_d[i][5]/2.0,s_d[i][1]+s_d[i][5]/2.0,fill=s_d[i][4],outline=s_d[i][4])
while running:
    cv.pack()
    star_sky()
    time.sleep(0.01)
    cv.update()
