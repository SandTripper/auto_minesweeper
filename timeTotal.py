import time
time_search = 0
time_screen = 0
time_click = 0

te = 0
ts = 0
tc = 0


def startSearch():
    global te
    te = time.time()


def endSearch():
    global te, time_search
    time_search += time.time()-te


def startScreen():
    global ts
    ts = time.time()


def endScreen():
    global ts, time_screen
    time_screen += time.time()-ts


def startClick():
    global tc
    tc = time.time()


def endClick():
    global tc, time_click
    time_click += time.time()-tc
