from pynput import *
import threading
import datetime
import time
import os

start_time = red_buff = blue_buff = red_crab = blue_crab = small_dragon = rift_herald = top_6 = mid_6 = bot_6 = 0
time_queue = []
goal_queue = []
state_button = True


def init_time(start_time):
    red_buff = start_time + datetime.timedelta(seconds=90)
    blue_buff = start_time + datetime.timedelta(seconds=90)
    red_crab = start_time + datetime.timedelta(seconds=195)
    blue_crab = start_time + datetime.timedelta(seconds=195)
    small_dragon = start_time + datetime.timedelta(minutes=5)
    rift_herald = start_time + datetime.timedelta(minutes=9)
    top_6 = start_time + datetime.timedelta(seconds=65+30*9+30)
    mid_6 = start_time + datetime.timedelta(seconds=65+30*9+20)
    bot_6 = start_time + datetime.timedelta(seconds=65+30*13+30)
    global time_queue
    global goal_queue
    time_queue = [red_buff, blue_buff, red_crab, blue_crab,
                  small_dragon, rift_herald, top_6, mid_6, bot_6]
    goal_queue = ['red buff', 'blue buff', 'red crab',
                  'blue crab', 'dragon', 'pioneer', 'top get 6', 'mid get 6', 'bot get 6']
    sort_queue()


def sort_queue():
    # Bubble sorting algorithm, sorting the broadcasting list according the time order.
    a = 1
    global time_queue
    global goal_queue
    while a != 0:
        a = 0
        for i in range(len(time_queue)-1):
            if time_queue[i].__gt__(time_queue[i+1]):
                tmp = time_queue[i+1]
                time_queue[i+1] = time_queue[i]
                time_queue[i] = tmp
                tmp = goal_queue[i+1]
                goal_queue[i+1] = goal_queue[i]
                goal_queue[i] = tmp
                a += 1
                pass
    print('items list has been refreshed ' + str(goal_queue))


def update_item(update_goal, update_time):
    i = 0
    global time_queue
    global goal_queue
    for goal in goal_queue:
        if goal == update_goal:
            goal_queue[i] = update_goal
            time_queue[i] = update_time
        i += 1
    sort_queue()


def broadcast_queue():
    while state_button:
        if time_queue:
            current_time = datetime.datetime.now()
            i = 0
            for time_ in time_queue:
                left_boundary = current_time - datetime.timedelta(seconds=1)
                right_boundary = current_time + datetime.timedelta(seconds=1)
                check_point_1 = time_ - datetime.timedelta(minutes=1)
                if left_boundary.__lt__(check_point_1) and right_boundary.__gt__(check_point_1):
                    do_broadcast(goal_queue[i], ' only one minute')
                ckeck_point_2 = time_ - datetime.timedelta(minutes=2)
                if left_boundary.__lt__(ckeck_point_2) and right_boundary.__gt__(ckeck_point_2):
                    do_broadcast(goal_queue[i], ' still two minutes')
                if left_boundary.__lt__(time_) and right_boundary.__gt__(time_):
                    do_broadcast(goal_queue[i], ' has appeared')
                i += 1
            time.sleep(2)
        else:
            time.sleep(3)


def do_broadcast(goal, type_):
    if type_ == ' has appeared':
        print(goal + type_)
        os.system('say ' + goal + type_)
    elif type_ == ' still two minutes':
        print('There are ' + type_ + ' before ' + goal)
        os.system('say There are' + type_ + ' before ' + goal)
    elif type_ == ' only one minute':
        print('There is ' + type_ + ' before ' + goal)
        os.system('say There is' + type_ + ' before ' + goal)


def on_release(key):
    if key == keyboard.Key.f8:
        global start_time
        start_time = datetime.datetime.now() - datetime.timedelta(seconds=15)
        os.system('say ' + 'Timer started')
        # Inisital all items
        init_time(start_time)

    if key == keyboard.Key.f1:
        global red_buff
        red_buff = datetime.datetime.now() + datetime.timedelta(minutes=5)
        os.system('say ' + 'red buff has recorded')
        update_item('red buff', red_buff)

    if key == keyboard.Key.f2:
        global blue_buff
        blue_buff = datetime.datetime.now() + datetime.timedelta(minutes=5)
        os.system('say ' + 'blue buff has been recorded')
        update_item('blue buff', blue_buff)

    if key == keyboard.Key.f3:
        global red_crab
        red_crab = datetime.datetime.now() + datetime.timedelta(seconds=150)
        os.system('say ' + 'red area crab has been recorded')
        update_item('red crab', red_crab)

    if key == keyboard.Key.f4:
        global blue_crab
        blue_crab = datetime.datetime.now() + datetime.timedelta(seconds=150)
        os.system('say ' + 'blue area crab has been recorded')
        update_item('blue crab', blue_crab)

    if key == keyboard.Key.f5:
        global small_dragon
        small_dragon = datetime.datetime.now() + datetime.timedelta(minutes=6)
        os.system('say ' + 'dragon has been recorded')
        update_item('dragon', small_dragon)

    if key == keyboard.Key.f6:
        global rift_herald
        rift_herald = datetime.datetime.now() + datetime.timedelta(minutes=6)
        os.system('say ' + 'pioneer has been recorded')
        update_item('pioneer', rift_herald)

    if key == keyboard.Key.delete:
        # 终结程序
        global state_button
        state_button = False
        return False


def start_listening():
    with keyboard.Listener(on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    threads = []
    t1 = threading.Thread(target=start_listening)
    threads.append(t1)
    t2 = threading.Thread(target=broadcast_queue)
    threads.append(t2)
    print('jungling assistance has launched, may you have a pentakill')
    os.system(
        'say ' + 'jungling assistance has launched, may you have a pentakill')
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print('jungling assistance has terminated')
    os.system('say ' + 'jungling assistance has terminated')
