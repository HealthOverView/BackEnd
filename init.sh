wget https://github.com/HealthOverView/yolov5_for_gosari/archive/refs/heads/main.zip -O yolo.zip
unzip yolo.zip -d ./
mv ./yolov5_for_gosari-main/* ./
rm -rf yolo.zip
rm -rf yolov5_for_gosari-main
pip install -r requirements.txt
mkdir images
