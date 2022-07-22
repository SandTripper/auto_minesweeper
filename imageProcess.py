import win32gui
import sys
from PIL import ImageGrab
import pyautogui
import timeTotal

class_name = "扫雷"
title_name = "扫雷"

block_width, block_height = 16, 16
left, top, right, bottom = 0, 0, 0, 0
blocks_x, blocks_y = 0, 0
blocks_img = list(list())


def crop_block(hole_img, x, y):  # 从大图中截取某个小格子的图像
    x1, y1 = x * block_width, y * block_height
    x2, y2 = x1 + block_width, y1 + block_height
    return hole_img.crop((x1, y1, x2, y2))


def get_frame():

    global left, top, right, bottom, blocks_x, blocks_y, blocks_img

    hwnd = win32gui.FindWindow(class_name, title_name)  # 寻找到窗口
    if hwnd:
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)  # 获取窗口坐标
    else:
        print("找不到正在运行的扫雷")
        sys.exit(1)

    # 去除边框，实测了很久的优秀数值
    left += 15
    top += 101
    right -= 11
    bottom -= 11

    blocks_x = int((bottom - top) / block_height)
    blocks_y = int((right - left) / block_width)

    blocks_img = [[0 for col in range(blocks_y)]for raw in range(
        blocks_x)]  # 建一张 blocks_x*blocks_y 的图片数组 ，真高级的语法


def update():

    # timeTotal.startScreen()

    global left, top, right, bottom, blocks_x, blocks_y, blocks_img
    pyautogui.moveTo(left + 16, top-24)  # 将鼠标移开防止影响截图

    img = ImageGrab.grab().crop((left, top, right, bottom))  # 截取图像

    # img.show()

    for x in range(blocks_x):
        for y in range(blocks_y):
            blocks_img[x][y] = crop_block(img, y, x)

    # timeTotal.endScreen()
    return blocks_img
