#raspistill -md 6
#raspistill -w 640
#raspistill -h 480
#raspistill -q 75
#raspistill --awb auto

DATE=$(date +"%Y-%m-%d_%H%M")
raspistill -vf -hf -o /home/pi/camera/$DATE.jpg
echo /home/pi/camera/$DATE.jpg
