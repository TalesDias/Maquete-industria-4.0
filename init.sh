#!/bin/bash

su pi <<'EOF'

cd "/home/pi/Desktop/Maquete-industria-4.0"
sudo pigpiod
tmux new -d -s core
tmux split-window -v
tmux split-window -h

pyPath=/usr/bin/python3

#iniciando o website
tmux send "cd website" ENTER 
tmux send "sudo $pyPath serve.py" ENTER 

#iniciando o controle 
tmux select-pane -t 1
tmux send "cd controle" ENTER
tmux send "sudo $pyPath main.py" ENTER

#iniciando o servidor
tmux select-pane -t 0
tmux send "cd servidor" ENTER
tmux send "source bin/activate" ENTER
tmux send "sudo ./bin/uwsgi --http :5000 --wsgi-file app.py --callable app" ENTER
tmux send "deactivate" ENTER

EOF
