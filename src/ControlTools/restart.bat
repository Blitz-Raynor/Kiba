@echo off
echo 受指令影响，正在重新启动 Kiba....
taskkill /im python.exe /f
cd..
cd..
start python bot.py
exit