chcp 65001

:loop

cd %~dp0
python master.py conf/default.conf conf/logging.conf
ping 127.0.0.1 -n 60 > nul
timeout 120

goto loop


