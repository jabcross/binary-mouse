#! /usr/bin/python3

import sys
import subprocess as sp
import json
import os

DIV_CONST = 2

def get_state():
    state = {}
    try:
        with open("/tmp/binary_mouse.tmp") as file:
            state = json.loads(file.read())
    except:
        pass

    print(state)

    cmd = "xdotool getmouselocation"
    print(cmd)
    out = sp.run(cmd.split(" "), capture_output=True).stdout.decode("UTF-8")

    mousepos = {x.split(":")[0]:int(x.split(":")[1]) for x in out.split()}

    print(mousepos)

    if "x" in state and "y" in state:
        if state["x"] != mousepos["x"] or state["y"] != mousepos["y"]:
            print("has_moved")
            # mouse has moved; reset binary search
            for x in ["left", "right", "up", "down"]:
                if x in state:
                    state.pop(x)

    state.update(mousepos)

    cmd = "xrandr | grep 'Screen {}' | sed -E 's/^.*current ([0-9]+) x ([0-9]+).*$/\\1 \\2/'".format(state["screen"])

    print(cmd)

    out = sp.run(cmd,capture_output=True,shell=True)

    state.update({x:int(y) for x,y in zip(["screen_width","screen_height"],out.stdout.split())})

    print(state)
    return state

def update_file(state):
    with open("/tmp/binary_mouse.tmp","w") as file:
        file.write(json.dumps(state))

print(sys.argv)

if len(sys.argv) < 2:
    exit()
if sys.argv[1] == "bin-left":
    # sp.run("notify-send bin-left",shell=True)
    state = get_state()
    left = int(state["x"] / DIV_CONST)
    if "left" in state:
        left = state["left"]

    cmd = "xdotool mousemove_relative -- {} {}".format(-left, 0)
    print(cmd)

    state["x"] -= left
    state["left"] = int(left / DIV_CONST)
    state["right"] = int(left / DIV_CONST)

    update_file(state)

    sp.run(cmd.split())

if sys.argv[1] == "bin-right":
    # sp.run("notify-send bin-right",shell=True)
    state = get_state()
    right = int((state["screen_width"] - state["x"]) / DIV_CONST)
    if "right" in state:
        right = state["right"]

    cmd = "xdotool mousemove_relative -- {} {}".format(right, 0)
    print(cmd)

    state["x"] += right
    state["left"] = int(right / DIV_CONST)
    state["right"] = int(right / DIV_CONST)

    update_file(state)

    sp.run(cmd.split())

if sys.argv[1] == "bin-down":
    # sp.run("notify-send bin-down",shell=True)
    state = get_state()
    down = int((state["screen_height"] - state["y"]) / DIV_CONST)
    if "down" in state:
        down = state["down"]

    cmd = "xdotool mousemove_relative -- {} {}".format(0, down)
    print(cmd)

    state["y"] += down
    state["up"] = int(down / DIV_CONST)
    state["down"] = int(down / DIV_CONST)

    update_file(state)

    sp.run(cmd.split())

if sys.argv[1] == "bin-up":
    # sp.run("notify-send bin-up",shell=True)
    state = get_state()
    up = int(state["y"] / DIV_CONST)
    if "up" in state:
        up = state["up"]

    cmd = "xdotool mousemove_relative -- {} {}".format(0, -up)
    print(cmd)

    state["y"] -= up
    state["up"] = int(up / DIV_CONST)
    state["down"] = int(up / DIV_CONST)

    update_file(state)

    sp.run(cmd.split())

if sys.argv[1] == "clear":
    try:
        os.remove("/tmp/binary_mouse.tmp")
    except:
        pass