from pdb import Restart
from zmq import Again
import imageProcess
import pyautogui
import time
import imageAnalyze
import random
import timeTotal

dxdy = [-1, 0, 1]
ocr = list(list())  # 用于记录对应位置的状态，如-2是旗子等等


def click(location, button):
    # 点击模块
    timeTotal.startClick()
    pyautogui.click(imageProcess.left+location[1]*imageProcess.block_width+imageProcess.block_width//2,
                    imageProcess.top+location[0]*imageProcess.block_height+imageProcess.block_height//2, clicks=1, button=button)
    timeTotal.endClick()


def inlimit(x, y):  # 判断是否在限制内
    if 0 <= x and x < imageProcess.blocks_x and 0 <= y and y < imageProcess.blocks_y:
        return True
    else:
        return False


restart = 0


def Ocr(blocks_img):  # 更新状态数组
    timeTotal.startScreen()
    global ocr, restart
    for x in range(imageProcess.blocks_x):
        for y in range(imageProcess.blocks_y):
            if ocr[x][y] == -3 or ocr[x][y] == -1:
                ocr[x][y] = imageAnalyze.analyze_block(blocks_img[x][y])
                if ocr[x][y] == 9:
                    restart = 1
                    return
    timeTotal.endScreen()


def judge(location, num):  # 判断某个点属于哪种情况
    global ocr
    sum_flag = 0
    sum_undo = 0
    for i in dxdy:
        for j in dxdy:
            x, y = location[0]+i, location[1]+j
            if inlimit(x, y):
                val = ocr[x][y]
                if val == -2:
                    sum_flag += 1
                if val == -1:
                    sum_undo += 1
    if sum_flag+sum_undo == num:
        return 2
    elif sum_flag == num:
        return 1
    else:
        return 3


if __name__ == "__main__":
    pyautogui.FAILSAFE = False  # 防止程序停不下来
    pyautogui.PAUSE = 0  # 设置点击间隔最短

    time.sleep(1)

    imageProcess.get_frame()  # 初始化框架

    ocr = [[-3 for col in range(imageProcess.blocks_y)]for raw in range(
        imageProcess.blocks_x)]  # 建立数字矩阵

    x, y = imageProcess.blocks_x//3, imageProcess.blocks_y//3
    click([x, y], "left")  # 将鼠标焦点移至扫雷
    click([x, y], "left")  # 第一次开奖

    blocks_img = imageProcess.update()  # 第一次截图

    Ocr(blocks_img)

    while True:

        total1 = 0

        change = False

        for x in range(imageProcess.blocks_x):  # 遍历整个棋盘
            for y in range(imageProcess.blocks_y):
                val = ocr[x][y]
                if val == -1:
                    total1 += 1
                if -3 <= val and val <= 0:
                    continue

                status = judge([x, y], val)

                if status == 1:  # 符合第一种状态,将周围未打开的雷块打开
                    for i in dxdy:
                        for j in dxdy:
                            xx, yy = x+i, y+j
                            if inlimit(xx, yy):
                                if ocr[xx][yy] == -1:
                                    click([xx, yy], 'left')
                                    change = True
                                    ocr[xx][yy] = -3
                elif status == 2:  # 符合第二种状态,将周围未打开的雷块标记为旗子
                    for i in dxdy:
                        for j in dxdy:
                            xx, yy = x+i, y+j
                            if inlimit(xx, yy):
                                if ocr[xx][yy] == -1:
                                    click([xx, yy], 'right')
                                    change = True
                                    ocr[xx][yy] = -2

        randid = random.randint(1, max(1, total1))
        xrand, yrand = 0, 0
        nowid = 0
        if not change:  # 如果遍历所有格子之后还是没有一个突破，则随机开奖
            for x in range(imageProcess.blocks_x):
                if nowid >= randid:
                    break
                for y in range(imageProcess.blocks_y):
                    val = ocr[x][y]
                    if val == -1:
                        nowid += 1
                        if nowid >= randid:
                            break
                        else:
                            xrand, yrand = x, y
            click([xrand, yrand], 'left')
            if nowid == 0:
                break

        blocks_img = imageProcess.update()  # 重新获取状态
        Ocr(blocks_img)  # 重新获取后再识别
        if restart == 1:  # 如果触雷，则重开一局扫雷
            restart = 0
            timeTotal.time_search, timeTotal.time_screen, timeTotal.time_click = 0, 0, 0
            click([-2, imageProcess.blocks_y//2], 'left')
            time.sleep(0.01)
            blocks_img = imageProcess.update()
            ocr = [[-3 for col in range(imageProcess.blocks_y)]for raw in range(
                imageProcess.blocks_x)]
            Ocr(blocks_img)
