#/bin/bash
#run random until deadlock occurs

while true; do
python3 do_random.py
make clean
make run
state=$(cat run_state)
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo $state
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
if [ "$state" == "deadlock" ]; then 
    break; 
fi
done