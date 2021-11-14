#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 首先通过screen.fill()来清理屏幕，然后绘制完所有图形后，再调用一次screen.display.update()或.flip()

import pygame
from collections import namedtuple


def scene4_intelligence():
    gameexit = False
    while not gameexit:
        gomoku_main()


def chess_coord():
    font = pygame.font.SysFont("微软雅黑", 16)
    for x in range(320, 920, 40):  # 循环绘制棋盘纵轴
        coord_x = font.render(str(x), True, black)
        screen.blit(coord_x, (x, 120-30))
    for y in range(120, 720, 40):  # 循环绘制棋盘横轴
        coord_y = font.render(str(y), True, black)
        screen.blit(coord_y, (320 - 30, y))


def chess_line(cell_num, cell_size, space_tb, space_lr):
    for x in range(0, cell_size * cell_num, cell_size):  # 循环绘制棋盘纵轴
        # 画线（画面，颜色，起点，终点，宽度）
        pygame.draw.line(screen, black, (x + space_tb, 0 + space_lr),
                         (x + space_tb, cell_size * (cell_num - 1) + space_lr), 2)
    for y in range(0, cell_size * cell_num, cell_size):  # 循环绘制棋盘横轴
        pygame.draw.line(screen, black, (0 + space_tb, y + space_lr),
                         (cell_size * (cell_num - 1) + space_tb, y + space_lr), 2)


# 通过物理坐标获取逻辑坐标
def get_coord(pos, spacetb, space_lr, cell_size):
    x, y = pos
    xi = round((x - spacetb) * 1.0 / cell_size)  # 保留值趋近于上一位
    yi = round((y - space_lr) * 1.0 / cell_size)
    return xi, yi


# 检查(i,j)位置是否已占用
def check_at(ball_coord, i, j):
    for item in ball_coord:
        # print((i, j), item)
        if (i, j) == item:
            return 0
    return 1


# 在(i,j)位置落子
def chess_drop_at(flagi, chessball_black, chessball_white, pos_x, pos_y):
    # 落子
    if flagi == 1:  # 轮到黑子下
        screen.blit(chessball_black, (pos_x, pos_y))
    else:
        screen.blit(chessball_white, (pos_x, pos_y))
    pygame.display.update()


def check_over(chess_arr):
    direct = [
        [(-1, 0), (1, 0)],
        [(0, -1), (0, 1)],
        [(-1, -1), (1, 1)],
        [(-1, 1), (1, -1)]
    ]  # 分别为横、纵、左下-右上、左上-右下
    last = chess_arr[-1]
    last_type = last['type']  # 最后一子类型
    chess_arr1 = []  # 提取与最后落子颜色相同的棋子
    for balli in chess_arr:
        if balli["type"] == last_type:
            chess_arr1.append(balli)
    chess_arr_reverse = chess_arr1[::-1]  # 逆序排序
    last_x, last_y = last["coord"].x, last["coord"].y  # 最后落子位置
    for d in direct:  # 遍历四个方向
        # print(d)
        balls_tmp = []
        last_x_tmp, last_y_tmp = last_x, last_y  # 在下次循环时复原位置
        for di in d:  # 遍历每个方向的子方向
            last_x_tmpi, last_y_tmpi = last_x_tmp, last_y_tmp  # 内部循环时也复原位置
            balls_tmpi = []
            dt_x, dt_y = di[0], di[1]  # 读取方向
            pos_x, pos_y = dt_x * 40, dt_y * 40
            index = 0
            while index <= len(chess_arr_reverse):
                last_x_tmpi, last_y_tmpi = last_x_tmpi + pos_x, last_y_tmpi + pos_y  # 只有找到满足条件的值才会变化
                # print(last_x_tmpi, last_y_tmpi)
                if 120-20 <= last_x_tmpi <= 680-20 and 60-20 <= last_y_tmpi <= 620-60:  # 控制范围
                    for ball in chess_arr_reverse:  # 从最后落后位置发起，按四个方向判断，如果满足条件就加入列表
                        ball_x,  ball_y = ball["coord"].x,  ball["coord"].y
                        if ball_x == last_x_tmpi and ball_y == last_y_tmpi:  # 有且仅有一个棋子满足条件
                            balls_tmpi.append(ball)
                            print((ball_x,  ball_y), (last_x_tmpi, last_y_tmpi))
                        else:
                            continue
                    index += 1
                else:  # 当超出范围时，说明该方向已穷尽
                    break
            for i in balls_tmpi:
                balls_tmp.append(i)
            if len(balls_tmp) >= 4:
                return 1


def chess_overtext(text):
    font = pygame.font.SysFont("方正仿宋简体", 60)
    gameover_text = font.render(text, True, (255, 0, 0))
    screen.blit(gameover_text, (round(width / 2 - gameover_text.get_width() / 2),
                                round(height / 2 - gameover_text.get_height() / 2)))


def gomoku_main():
    cell_size = 40
    space_tb, space_lr = 320, 120
    cell_num = 15
    time1 = pygame.time.get_ticks()
    flag = 1  # 1黑2白
    ball_coord = []
    chess_arr = []  # 多维数组
    checkerboard = pygame.image.load(image_background)
    chessball_black = pygame.image.load(image_black_chess)
    chessball_white = pygame.image.load(image_white_chess)
    chessball_width, chessball_height = chessball_white.get_width(), chessball_white.get_height()

    screen.blit(checkerboard, (0, 0))
    chess_line(cell_num, cell_size, space_tb, space_lr)  # 绘制棋盘
    chess_coord()  # 绘制坐标

    # 构造一个带字段名的元组
    position_chess = namedtuple("position", ["x", "y"])
    chess_over = False
    while not chess_over:
        time2 = pygame.time.get_ticks()
        time3 = time2 - time1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if time3 >= 1000:  # 停顿1秒后执行
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        # 绝对坐标转化为轴数
                        xi, yi = get_coord(pos, space_tb, space_lr, cell_size)
                        if 0 <= xi < 15 and 0 <= yi < 15:
                            # 检查落子位置
                            if check_at(ball_coord, xi, yi) == 1:
                                pos_x = xi * cell_size + space_tb - chessball_width / 2  # 反推横轴
                                pos_y = yi * cell_size + space_lr - chessball_height / 2  # 反推纵轴
                                ball_pos = {'type': flag, 'coord': position_chess(pos_x, pos_y)}
                                chess_arr.append(ball_pos)  # 记录棋子位置与颜色
                                chessballs_num = len(chess_arr)  # 棋子数量
                                flagi = chess_arr[-1]["type"]

                                # 绘制落子位置
                                chess_drop_at(flagi, chessball_black, chessball_white, pos_x, pos_y)
                                ball_coord.append((xi, yi))

                                # 当棋子总数大于8时，判断输赢
                                if chessballs_num > 8:
                                    gomoku_state = check_over(chess_arr)
                                    if gomoku_state == 1 and flagi == 2:  # 白棋win
                                        text = "哈哈，你输喽！"  # 我是黑方，这意味着lose
                                        chess_overtext(text)
                                        chess_over = True
                                    elif gomoku_state == 1 and flagi == 1:  # 黑棋win
                                        text = "恭喜，你赢了！"  # 我是黑方，这意味着win
                                        chess_overtext(text)
                                        chess_over = True
                                    else:
                                        flag = 2 if flag == 1 else 1
                                        continue
                                # 如果棋子总数小于等于8，那么交替下
                                else:
                                    flag = 2 if flag == 1 else 1
                            else:
                                print("不能在这个地方落子！")

                pygame.display.update()


def gomoku_win():
    gameexit = False
    while not gameexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # screen.blit(renju.chessboard(), (0, 0))
            button("继续！", 400, 700, 100, 50, grey2, grey1, scene5)  # scene1
            button("放弃！", 700, 700, 100, 50, grey2, grey1, quitgame)
            pygame.display.update()


def gomoku_lose():
    gameexit = False
    while not gameexit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # screen.blit(renju.chessboard(), (0, 0))
            button("来，再战！", 400, 700, 100, 50, grey2, grey1, scene4_intelligence)  # scene4_intelligence
            button("放弃！", 700, 700, 100, 50, grey2, grey1, quitgame)
            pygame.display.update()


def button(msg, x, y, w, h, ic, ac, action):
    mouse = pygame.mouse.get_pos()  # =返回鼠标光标的坐标 (x, y)，以窗口左上角为基准点
    click = pygame.mouse.get_pressed()  # 获取鼠标按键的情况，由布尔值组成的列表
    # print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # 鼠标点击在固定范围内
        # print(x, x + w, y, y + h, mouse[0], mouse[1])
        pygame.draw.rect(screen, ac, (x, y, w, h))  # 按钮高亮
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    smalltext = pygame.font.SysFont('方正仿宋简体', 20)
    textsurf, textrect = text_objects(msg, smalltext)
    textrect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textsurf, textrect)


def quitgame():
    pygame.quit()
    exit()


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


if __name__ == '__main__':
    '''初始化'''
    # 初始化窗口
    pygame.init()
    # 加载本地图片
    # picdir = "D:\\Py\\QFFA\\Pygame-master\\resources\\bb\\images\\"
    picdir = "D:\\04Hobby\\041Coding\\Pythons\\QFFA\\Pygame-master\\resources\\bb\\images\\"

    # 加载本地图片
    image_background = picdir + "checker3.jpg"
    image_white_chess = picdir + "chessball_white1.png"
    image_black_chess = picdir + "chessball_black1.png"

    # width, height = 800, 680
    width, height = 1200, 800
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    red = (200, 0, 0)
    green = (0, 200, 0)
    bright_red = (255, 0, 0)
    bright_green = (0, 255, 0)
    blue = (0, 0, 255)
    grey1 = (150, 150, 150)
    grey2 = (200, 200, 200)
    grey3 = (240, 240, 240)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('五子棋')

    gomoku_main()