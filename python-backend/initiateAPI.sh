#!/bin/bash
python API_Job_Management.py &
python API_File_Management.py &

# 保持腳本運行
while true; do
    sleep 1
done