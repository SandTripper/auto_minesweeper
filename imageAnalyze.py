def analyze_block(block):

    block_color = block.getpixel((8, 8))

    # 0:空方块
    # -1:未打开
    # -2:插旗
    # -3:未知方块

    if block_color == (192, 192, 192):
        if block.getpixel((3, 3)) == (0, 0, 0):
            res = 7
        elif not block.getpixel((9, 0)) == (255, 255, 255):
            res = 0
        else:
            res = -1

    elif block_color == (0, 0, 255):
        res = 1

    elif block_color == (0, 128, 0):
        res = 2

    elif block_color == (255, 0, 0):
        res = 3

    elif block_color == (0, 0, 128):
        res = 4

    elif block_color == (128, 0, 0):
        res = 5

    elif block_color == (0, 128, 128):
        res = 6

    elif block_color == (0, 0, 0):
        if block.getpixel((6, 6)) == (255, 255, 255):
            # 地雷
            res = 9
        elif block.getpixel((5, 6)) == (255, 0, 0):
            # 旗子
            res = -2
        else:
            res = 7

    elif block_color == (128, 128, 128):
        res = 8
    else:
        res = -3

    return res
