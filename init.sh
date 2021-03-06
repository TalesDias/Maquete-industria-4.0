#!/bin/bash

echo "Iniciando o pigpio daemon"
pigpiod

cd "Desktop/Maquete-industria-4.0"
echo "Iniciando a Maquete"
date

cd /home/pi/Desktop/Maquete-industria-4.0/website
sudo /usr/bin/python3 serve.py &

cd ../controle
/usr/bin/python3 main.py &
/usr/bin/python3 config_cor.py &

cd ../servidor
source bin/activate
./bin/uwsgi --http :5000 --wsgi-file app.py --callable app

deactivate

