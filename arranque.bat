@echo off
title Lanzador Sublimé Studio - Carlos Lozada
echo ✨ Iniciando el ecosistema de Sublimé Studio...
echo ------------------------------------------------
echo 1. Instalando dependencias (Solo si es necesario)...
pip install flask flask-cors
echo ------------------------------------------------
echo 2. Encendiendo el Servidor Backend...
start cmd C:\Users\sytpr\Documents\SUBLIMÉ STUDIO\WEB python upload.py
echo ------------------------------------------------
echo 3. Abriendo Panel de Administrador...
start admin.html
echo ------------------------------------------------
echo 4. Abriendo Catalogo de Clientes...
start index.html
echo ------------------------------------------------
echo ✅ ¡Todo listo Carlos! Ya puedes trabajar.
pause