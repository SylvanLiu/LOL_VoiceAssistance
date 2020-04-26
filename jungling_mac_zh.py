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
    goal_queue = ['红buff', '蓝buff', '红区河道蟹',
                  '蓝区河道蟹', '小龙', '先锋', '上路到6', '中路到6', '下路到6']
    sort_queue()


def sort_queue():
    # 冒泡算法, 按照时间大小整理播报队列
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
    print('时间节点已刷新'+str(goal_queue))


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
                    do_broadcast(goal_queue[i], '还有一分钟')
                ckeck_point_2 = time_ - datetime.timedelta(minutes=2)
                if left_boundary.__lt__(ckeck_point_2) and right_boundary.__gt__(ckeck_point_2):
                    do_broadcast(goal_queue[i], '还有两分钟')
                if left_boundary.__lt__(time_) and right_boundary.__gt__(time_):
                    do_broadcast(goal_queue[i], '已经出现')
                i += 1
            time.sleep(2)
        else:
            time.sleep(3)


def do_broadcast(goal, type_):
    if type_ == '已经出现':
        print(goal + type_)
        os.system('say ' + goal + type_)
    else:
        print('距离' + goal + type_)
        os.system('say 距离' + goal + type_)


def on_release(key):
    if key == keyboard.Key.f8:
        global start_time
        start_time = datetime.datetime.now() - datetime.timedelta(seconds=15)
        os.system('say ' + '已开始计时')
        # 初始化所有条目时间
        init_time(start_time)

    if key == keyboard.Key.f1:
        global red_buff
        red_buff = datetime.datetime.now() + datetime.timedelta(minutes=5)
        os.system('say ' + '己方红buff已记录')
        update_item('红buff', red_buff)

    if key == keyboard.Key.f2:
        global blue_buff
        blue_buff = datetime.datetime.now() + datetime.timedelta(minutes=5)
        os.system('say ' + '己方蓝buff已记录')
        update_item('蓝buff', blue_buff)

    if key == keyboard.Key.f3:
        global red_crab
        red_crab = datetime.datetime.now() + datetime.timedelta(seconds=150)
        os.system('say ' + '红区河道蟹已记录')
        update_item('红区河道蟹', red_crab)

    if key == keyboard.Key.f4:
        global blue_crab
        blue_crab = datetime.datetime.now() + datetime.timedelta(seconds=150)
        os.system('say ' + '蓝区河道蟹已记录')
        update_item('蓝区河道蟹', blue_crab)

    if key == keyboard.Key.f5:
        global small_dragon
        small_dragon = datetime.datetime.now() + datetime.timedelta(minutes=6)
        os.system('say ' + '小龙已记录')
        update_item('小龙', small_dragon)

    if key == keyboard.Key.f6:
        global rift_herald
        rift_herald = datetime.datetime.now() + datetime.timedelta(minutes=6)
        os.system('say ' + '峡谷先锋已记录')
        update_item('先锋', rift_herald)

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
    os.system('say ' + '打野辅助系统已开始运行, 祝您武运昌隆')
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    os.system('say ' + '打野辅助系统已停止运行')
