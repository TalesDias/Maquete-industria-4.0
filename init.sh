#!/bin/bash

echo "iniciando vnc"

/usr/bin/vncserver :1 -geometry 1350x700


cd "Desktop/Maquete-industria-4.0"
echo "Iniciando a Maquete"
date

cd ./website
sudo /usr/bin/python3 serve.py &

cd ../servidor
source bin/activate
./bin/uwsgi --http :5000 --wsgi-file app.py --callable app

deactivate
