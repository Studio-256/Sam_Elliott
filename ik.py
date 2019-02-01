import math
import tkinter
import random
import time

life = 4
yeti_life = 4
hit_life = 6
moving = [(-60, 0), (0, -60), (60, 0), (0, 60)]
busy = False


def do_nothing(x):
    return


def ouch():
    global life
    life -= 1
    if life:
        label.config(text="Здоровье: " + str(life * 25))
    if not life and canvas.coords(bullet) == canvas.coords(player):
        label.config(text="Вы застрелили себя!")


def ai():
    if yeti_life:
        if canvas.coords(yeti) != canvas.coords(player):
            way = [(0, (canvas.coords(yeti)[0] - canvas.coords(player)[0] + 60 * N_X) % (60 * N_X)),
                   (1, (canvas.coords(yeti)[1] - canvas.coords(player)[1] + 60 * N_Y) % (60 * N_Y)),
                   (2, (canvas.coords(player)[0] - canvas.coords(yeti)[0] + 60 * N_X) % (60 * N_X)),
                   (3, (canvas.coords(player)[1] - canvas.coords(yeti)[1] + 60 * N_Y) % (60 * N_Y))]
            way.sort(key=lambda x: x[1])
            i = 0
            while i < 3 and (way[i][1] == 0 or [
                (canvas.coords(yeti)[0] + moving[way[i][0]][0] + 60 * N_X) % (60 * N_X),
                (canvas.coords(yeti)[1] + moving[way[i][0]][1] + 60 * N_Y) % (
                        60 * N_Y)] in [canvas.coords(yeti)] + [canvas.coords(exit)[:2]]):
                i += 1
            move_wrap(canvas, yeti, moving[way[i][0]])
    if hit_life:
        if canvas.coords(hit) != canvas.coords(player):
            way = [(0, (canvas.coords(hit)[0] - canvas.coords(player)[0] + 60 * N_X) % (60 * N_X)),
                   (1, (canvas.coords(hit)[1] - canvas.coords(player)[1] + 60 * N_Y) % (60 * N_Y)),
                   (2, (canvas.coords(player)[0] - canvas.coords(hit)[0] + 60 * N_X) % (60 * N_X)),
                   (3, (canvas.coords(player)[1] - canvas.coords(hit)[1] + 60 * N_Y) % (60 * N_Y))]
            way.sort(key=lambda x: x[1])
            i = 0
            while i < 3 and (way[i][1] == 0 or
                             ((canvas.coords(hit)[0] + moving[way[i][0]][0]
                               + 60 * N_X) % (60 * N_X),
                              (canvas.coords(hit)[1] + moving[way[i][0]][1] + 60 * N_Y) % (60 * N_Y)) in fires_pos + [tuple(canvas.coords(yeti))] + [tuple(canvas.coords(exit)[:2])]):
                i += 1
            move_wrap(canvas, hit, moving[way[i][0]])


def move_wrap(canvas, obj, move):
    c = list(canvas.coords(obj))
    canvas.move(obj, move[0], move[1])
    if canvas.coords(obj)[0] < 0:
        canvas.coords(obj, [60 * N_X - 60, canvas.coords(obj)[1]])
    elif canvas.coords(obj)[0] >= 60 * N_X:
        canvas.coords(obj, [0, canvas.coords(obj)[1]])
    elif canvas.coords(obj)[1] < 0:
        canvas.coords(obj, [canvas.coords(obj)[0], 60 * N_Y - 60])
    elif canvas.coords(obj)[1] >= 60 * N_Y:
        canvas.coords(obj, [canvas.coords(obj)[0], 0])
    if canvas.coords(obj) == canvas.coords(exit)[:2] and yeti_life and hit_life and obj == player:
        canvas.coords(player, c)
        return False
    return True


def check_move():
    global life
    if canvas.coords(player) == canvas.coords(exit)[:2]:
        if hit_life:
            label.config(text="Вы не убили Гитлера")
        elif yeti_life:
            label.config(text="Вы не убили снежного человека")
        else:
            label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    if canvas.coords(player) == canvas.coords(yeti):
        life = 0
        label.config(text="Снежный человек оказался проворнее вас!")
    elif canvas.coords(player) == canvas.coords(hit):
        life = 0
        label.config(text="Гитлер оказался проворнее вас!")
    elif tuple(canvas.coords(player)) in fires_pos:
        if yeti_life:
            ouch()
            if life == 0:
                label.config(text="Вы слишком часто были в Канаде!")
        else:
            life = 0
            label.config(text="Вы арестованы за убийство снежного человека!")
    if life == 0:
        master.bind("<KeyPress>", do_nothing)


def key_pressed(event):
    global busy
    if busy:
        return
    busy = True
    global hit_life, yeti_life, exit
    if event.keysym in ['Up', 'Down', 'Left', 'Right'] or event.keycode in [87, 65, 83, 68]:
        fl = True
        if event.keysym == 'Up':
            fl = move_wrap(canvas, player, (0, -step))
        elif event.keysym == 'Down':
            fl = move_wrap(canvas, player, (0, step))
        elif event.keysym == 'Left':
            fl = move_wrap(canvas, player, (-step, 0))
        elif event.keysym == 'Right':
            fl = move_wrap(canvas, player, (step, 0))
        else:
            if event.keycode == 68:
                canvas.coords(bullet, canvas.coords(player))
                move_wrap(canvas, bullet, (40, 0))
                while canvas.coords(bullet) not in (canvas.coords(player), canvas.coords(yeti), canvas.coords(hit)):
                    canvas.update()
                    time.sleep(0.001)
                    move_wrap(canvas, bullet, (2, 0))
            elif event.keycode == 65:
                canvas.coords(bullet, canvas.coords(player))
                move_wrap(canvas, bullet, (-2, 0))
                while canvas.coords(bullet) not in (canvas.coords(player), canvas.coords(yeti), canvas.coords(hit)):
                    canvas.update()
                    time.sleep(0.001)
                    move_wrap(canvas, bullet, (-2, 0))
            elif event.keycode == 87:
                canvas.coords(bullet, canvas.coords(player))
                move_wrap(canvas, bullet, (0, -2))
                while canvas.coords(bullet) not in (canvas.coords(player), canvas.coords(yeti), canvas.coords(hit)):
                    canvas.update()
                    time.sleep(0.001)
                    move_wrap(canvas, bullet, (0, -2))
            elif event.keycode == 83:
                canvas.coords(bullet, canvas.coords(player))
                move_wrap(canvas, bullet, (0, 2))
                while canvas.coords(bullet) not in (canvas.coords(player), canvas.coords(yeti), canvas.coords(hit)):
                    canvas.update()
                    time.sleep(0.001)
                    move_wrap(canvas, bullet, (0, 2))
            if canvas.coords(bullet) == canvas.coords(player):
                ouch()
            if canvas.coords(bullet) == canvas.coords(yeti):
                yeti_life -= 1
                if not yeti_life:
                    if hit_life:
                        exit = canvas.create_oval(canvas.coords(exit), fill='yellow')
                    else:
                        exit = canvas.create_oval(canvas.coords(exit), fill='green')
                    canvas.coords(yeti, (-60, -60))
            if canvas.coords(bullet) == canvas.coords(hit):
                hit_life -= 1
                if not hit_life:
                    if yeti_life:
                        exit = canvas.create_oval(canvas.coords(exit), fill='yellow')
                    else:
                        exit = canvas.create_oval(canvas.coords(exit), fill='green')
                    canvas.coords(hit, (-60, -60))
            canvas.coords(bullet, (-60, -60))
        if fl:
            ai()
            check_move()
    busy = False


def prepare_and_start():
    global player, exit, fires, yeti, hit, fires_pos, bullet, life, hit_life, yeti_life
    life, yeti_life, hit_life = 4, 5, 3
    canvas.delete("all")
    player_pos = (random.randint(0, N_X - 1) * step,
                  random.randint(0, N_Y - 1) * step)
    exit_pos = (random.randint(0, N_X - 1) * step,
                random.randint(0, N_Y - 1) * step)
    while exit_pos == player_pos:
        exit_pos = (random.randint(0, N_X - 1) * step,
                    random.randint(0, N_Y - 1) * step)
    N_FIRES = random.randint(8, min(64, int(4 * math.sqrt(N_X * N_Y))))
    fires = []
    fires_pos = []
    for i in range(N_FIRES):
        fire_pos = (random.randint(0, N_X - 1) * step,
                    random.randint(0, N_Y - 1) * step)
        while fire_pos in fires + [player_pos] + [exit_pos]:
            fire_pos = (random.randint(0, N_X - 1) * step,
                        random.randint(0, N_Y - 1) * step)
        fire = canvas.create_image(fire_pos, image=canada_pic, anchor='nw')
        fires.append(fire)
        fires_pos.append(fire_pos)
    exit = canvas.create_oval(
        (exit_pos[0], exit_pos[1]),
        (exit_pos[0] + step, exit_pos[1] + step),
        fill='red'
    )
    player = canvas.create_image(player_pos, image=zigmund_pic, anchor='nw')
    bullet = canvas.create_image((-60, -60), image=bullet_pic)
    hit_pos = (random.randint(0, N_X - 1) * step,
               random.randint(0, N_Y - 1) * step)
    while hit_pos in fires_pos + [player_pos] + [exit_pos]:
        hit_pos = (random.randint(0, N_X - 1) * step,
                   random.randint(0, N_Y - 1) * step)
    hit = canvas.create_image(hit_pos, image=hit_pic, anchor='nw')
    yeti_pos = (random.randint(0, N_X - 1) * step,
                random.randint(0, N_Y - 1) * step)
    while yeti_pos in fires_pos + [player_pos] + [exit_pos] + [hit_pos]:
        yeti_pos = (random.randint(0, N_X - 1) * step,
                    random.randint(0, N_Y - 1) * step)
    yeti = canvas.create_image(yeti_pos, image=yeti_pic, anchor='nw')
    label.config(text="Здоровье: 100")
    master.bind("<KeyPress>", key_pressed)


def close_window():
    master.quit()
    master.destroy()


master = tkinter.Tk()
master.overrideredirect(1)
master.state('zoomed')
hit_pic = tkinter.PhotoImage(file='hit.gif')
yeti_pic = tkinter.PhotoImage(file='yeti.gif')
zigmund_pic = tkinter.PhotoImage(file='Zigmund.gif')
canada_pic = tkinter.PhotoImage(file='Canada.gif')
bullet_pic = tkinter.PhotoImage(file='bullet.gif')
step = 60  # Размер клетки
N_X = master.winfo_screenwidth() // 60
N_Y = (master.winfo_screenheight() - 25) // 60
label = tkinter.Label(master, text="Найди выход")
label.pack()
canvas = tkinter.Canvas(
    master, bg='blue', height=N_Y * step, width=N_X * step)
canvas.pack()
restart = tkinter.Button(master, text="Начать заново", command=prepare_and_start)
close = tkinter.Button(master, text="Закрыть", command=close_window)
close.place(x=master.winfo_screenwidth() - 55, y=-2)
restart.place(x=master.winfo_screenwidth() - 200, y=-2)
prepare_and_start()
master.mainloop()
