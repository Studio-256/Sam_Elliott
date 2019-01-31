import math
import tkinter
import random

life = 5
yeti_life = 3
hit_life = 2
moving = [(-60, 0), (0, -60), (60, 0), (0, 60)]


def do_nothing(x):
    return


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
                        60 * N_Y)] == canvas.coords(hit)):
                i += 1
            canvas.coords(yeti,
                          [(canvas.coords(yeti)[0] + moving[way[i][0]][0] + 60 * N_X) % (60 * N_X),
                           (canvas.coords(yeti)[1] + moving[way[i][0]][1] + 60 * N_Y) % (60 * N_Y)])
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
                              (canvas.coords(hit)[1] + moving[way[i][0]][1] + 60 * N_Y) % (
                                      60 * N_Y)) in fires_pos + [tuple(canvas.coords(hit))]):
                i += 1
            canvas.coords(hit,
                          [(canvas.coords(hit)[0] + moving[way[i][0]][0] + 60 * N_X) % (60 * N_X),
                           (canvas.coords(hit)[1] + moving[way[i][0]][1] + 60 * N_Y) % (60 * N_Y)])


def move_wrap(canvas, obj, move):
    canvas.move(obj, move[0], move[1])
    if canvas.coords(obj)[0] < 0:
        canvas.coords(obj, [60 * N_X - 60, canvas.coords(obj)[1]])
    elif canvas.coords(obj)[0] >= 60 * N_X:
        canvas.coords(obj, [0, canvas.coords(obj)[1]])
    elif canvas.coords(obj)[1] < 0:
        canvas.coords(obj, [canvas.coords(obj)[0], 60 * N_Y - 60])
    elif canvas.coords(obj)[1] >= 60 * N_Y:
        canvas.coords(obj, [canvas.coords(obj)[0], 0])


def check_move():
    global life
    if canvas.coords(player) == canvas.coords(exit)[:2]:
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    if tuple(canvas.coords(player)) in fires_pos:
        if yeti_life:
            life -= 1
            label.config(text="Здоровье: " + str(life * 20))
        else:
            life = 0
    if canvas.coords(player) == canvas.coords(yeti) or canvas.coords(player) == canvas.coords(hit):
        life = 0
    if life == 0:
        label.config(text="Ты проиграл!")
        master.bind("<KeyPress>", do_nothing)
    # for f in fires:
    #     if canvas.coords(player) == canvas.coords(f):
    #         label.config(text="Ты проиграл!")
    #         master.bind("<KeyPress>", do_nothing)


def key_pressed(event):
    if event.keysym in ['Up', 'Down', 'Left', 'Right'] or event.char.lower() in 'wasd':
        if event.keysym == 'Up':
            move_wrap(canvas, player, (0, -step))
        elif event.keysym == 'Down':
            move_wrap(canvas, player, (0, step))
        elif event.keysym == 'Left':
            move_wrap(canvas, player, (-step, 0))
        elif event.keysym == 'Right':
            move_wrap(canvas, player, (step, 0))
        # elif event.char.lower() == 'w': canvas.coords(bullet, canvas.coords(player)) move_wrap(
        # canvas, bullet, (0, 1)) while canvas.coords(bullet) not in (canvas.coords(player),
        # canvas.coords(yeti), canvas.coords(hit)): time.sleep(0.005) move_wrap(canvas, bullet,
        # (0, 1)) elif event.char.lower() == 'a':
        #
        # elif event.char.lower() == 's':
        #
        # elif event.char.lower() == 'd':

        ai()
        check_move()


def prepare_and_start():
    global player, exit, fires, yeti, hit, fires_pos, bullet, life, hit_life, yeti_life
    life, yeti_life, hit_life = 5, 3, 2
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
    player = canvas.create_image(player_pos, image=zigmund_pic, anchor='nw')
    exit = canvas.create_oval(
        (exit_pos[0], exit_pos[1]),
        (exit_pos[0] + step, exit_pos[1] + step),
        fill='yellow'
    )
    bullet = canvas.create_image((-60, -60), image=tkinter.PhotoImage(file='bullet.gif'))
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
