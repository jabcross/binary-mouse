# binary-mouse

A Python script to move the mouse in a binary-search kind of way.

Allows for precise cursor positioning in log(n) keystrokes.

### Requirements

- `xrandr`
- `xdotool`
- Python3

### Usage:

```
python3 <script path>/binary-mouse.py bin-up 
python3 <script path>/binary-mouse.py bin-down 
python3 <script path>/binary-mouse.py bin-left
python3 <script path>/binary-mouse.py bin-right
python3 <script path>/binary-mouse.py clear
```

Bind your shortcuts with your favorite keyboard shortcut provider.

Example `i3wm` config:

```
bindsym $mod+Ctrl+j exec "python3 /home/jabcross/experiments/binary-mouse/binary-mouse.py bin-left"
bindsym $mod+Ctrl+l exec "python3 /home/jabcross/experiments/binary-mouse/binary-mouse.py bin-right"
bindsym $mod+Ctrl+i exec "python3 /home/jabcross/experiments/binary-mouse/binary-mouse.py bin-up"
bindsym $mod+Ctrl+k exec "python3 /home/jabcross/experiments/binary-mouse/binary-mouse.py bin-down"
```

The script keeps a state file at `/tmp/binary-mouse.tmp`.

The first time you call one of the commands, the mouse will be taken to the midpoint between its current position and the border of the screen. Each subsequent call will move the cursor half the distance previously walked. The vertical and horizontal distances are kept separately.

If you move the mouse manually or call the script with the `clear` command, the state is removed and a new search can be started.

You can use `xdotool` to send mouse clicks.
