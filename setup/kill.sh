#1/bin/bash

# Kill airflow processes
ps aux | grep airflow | awk '{print $2}' | xargs -n1 bash -c 'kill $0'