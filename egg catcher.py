from itertools import cycle
from random import randrange,choice
from tkinter import *
from tkinter import messagebox

canvas_width = 800
canvas_height = 500

win = Tk()
#canvas
c = Canvas(win,width = canvas_width,height = canvas_height,background = "blue")
c.create_rectangle(-5,canvas_height-100,canvas_width+5,canvas_height+5,fill = "green",width=0)
c.create_oval(-80,-80,120,120,fill = "red",width=0)
c.pack()

#text
score = 0
score_text = c.create_text(10,10,anchor='nw',font=('Arial',10,'bold'),fill='darkblue',text='Score : '+str(score))
lives = 2
lives_text = c.create_text(canvas_width-10,10,anchor='ne',font=('Arial',10,'bold'),fill='darkblue',text='Lives : '+str(lives))

#egg
colors = ["light blue","light pink","light yellow","light green","red","blue","green","black","white","yellow"]
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 300
egg_interval = 4000
difficulty_factor = 0.95


#catcher
catcher_color = "black"
catcher_width = 100
catcher_height = 100
catcher_start_x1 = canvas_width/2-catcher_width/2
catcher_start_y1 = canvas_height-catcher_height-100
catcher_start_x2 = catcher_start_x1+catcher_width+20
catcher_start_y2 = catcher_start_x2+catcher_height-100
catcher = c.create_arc(catcher_start_x1,catcher_start_y1,catcher_start_x2,catcher_start_y2,start=200,extent = 140,style="arc",outline = catcher_color,width = 3)

eggs = []



def create_eggs():
    x = randrange(10,750)
    y = 40
    new_egg = c.create_oval(x,y,x+egg_width,y+egg_height,fill=choice(colors),width=0)
    eggs.append(new_egg)
    win.after(egg_interval,create_eggs)


def move_eggs():
    for egg in eggs:
        (egg_x1,egg_y1,egg_x2,egg_y2) = c.coords(egg)
        c.move(egg,0,10)
        if egg_y2 > canvas_height:
            egg_dropped(egg)
    win.after(egg_speed,move_eggs)


def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_live()
    if lives == 0:
        messagebox.showinfo('GAME OVER!' , 'Final Score : ' + str(score))
        win.destroy()

def lose_a_live():
    global lives
    lives-=1
    c.itemconfigure(lives_text,text="Lives : "+str(lives))


def check_catch():
    (catcher_x1,catcher_y1,catcher_x2,catcher_y2) = c.coords(catcher)
    for egg in eggs:
        (egg_x1,egg_y1,egg_x2,egg_y2) = c.coords(egg)
        if catcher_x1 < egg_x1 and egg_x2 < catcher_x2 and catcher_y2-egg_y2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            score_increase()
    win.after(100,check_catch)

def score_increase():
    global score,egg_speed,egg_interval
    score+=10
    egg_speed = int(egg_speed*difficulty_factor)
    egg_interval = int(egg_interval*difficulty_factor)
    c.itemconfigure(score_text,text="Score : "+str(score))

def move_left(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x1>0:
        c.move(catcher,-20,0)

def move_right(event):
    (x1,y1,x2,y2) = c.coords(catcher)
    if x2<canvas_width:
        c.move(catcher,+20,0)
    
win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,check_catch)



c.bind('<Left>',move_left)
c.bind('<Right>',move_right)
c.focus_set()


win.mainloop()