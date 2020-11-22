#!/bin/bash

echo "iniciando vnc"

/usr/bin/vncserver :1 -geometry 1350x700


cd "Desktop/Maquete-industria-4.0"
echo "Iniciando a Maquete"
date

cd ./website
/usr/bin/python3 serve.py &

cd ..
cd ./servidor
source bin/activate
usr/bin/python3 app.py

deactivate
