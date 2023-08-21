from efficientnet_pytorch.utils import efficientnet
import torch
import torch.nn as nn
from efficientnet_pytorch import EfficientNet
from torchvision import transforms
from PIL import Image
import os
from PIL import Image, ImageDraw
from models.experimental import attempt_load
from utils.general import non_max_suppression


model_name = 'efficientnet-b5' #모델 이름
num_classes = 4  # Replace with the actual number of classes #클래스 갯수
model = EfficientNet.from_pretrained(model_name, num_classes=num_classes) #사용 모델 선언
model_path = '/home/intin-dev-001/HealthOverView/BackEnd/model/president_model3.pt' #모델 베스트 PT import
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'))) #CPU 모드로 전환
model.eval() # 파이토치를 평가 모드로 변경

def predict(image_path):

    #이미지 전처리
    def preprocess_image(image_path):
        transform = transforms.Compose([
            transforms.Resize((640, 640)),  #640*640포멧으로 설정
            transforms.ToTensor(), #Tensor 포멧으로 변경
        ])
        image = Image.open(image_path).convert("RGB") #이미지 객체를 RGB로 변경
        image = transform(image) 

        # 이미지 밝기 조정
        brightness_factor = 0.85  # You can experiment with this value
        image = image * brightness_factor

        #이미지 정규화 및 색상 조정
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) 
        image = normalize(image)

        return image

    # 베스트 모델 PT에 예측
    def predict_image_class(image, model):
        with torch.no_grad():
            outputs = model(image.unsqueeze(0))
        _, predicted = torch.max(outputs, 1)
        return predicted.item()

    # 로드한 이미지를 사이즈 조정 등에 조정과 텐서 포멧으로 변경
    specified_image = preprocess_image(image_path)

    # 이미지를 모델을 통한 예측값을 받음
    predicted_class = predict_image_class(specified_image, model)

    # 반환 값은 번호를 가지기 때문에 해당 번호에 해당하는 클래스 네임가 매칭
    class_names = ['ovulatory_phase', 'transitional_period', 'infertility_period', 'foreign_substance']
    res = class_names[predicted_class]
    print("EFF res >",res)
    
    #EfficientNet 결과가 이물질로 나왔을때 이물질에서 Yolo를 통해 한 번 더 검증 과정을 거친다.
    if predicted_class == 3:
      # Load YOLOv5 model

      model_yolo = attempt_load('/home/intin-dev-001/HealthOverView/BackEnd/model/best.pt')

      device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

      model_yolo.to(device)

      model_yolo.eval()

      #욜로 환경에서 데이터 처리를 위한 전처리 
      def preprocess_image(image_path, img_size=640):
          print("preprocess_image")
          img = Image.open(image_path).convert('RGB') #RGB변경
          img = transforms.Resize((img_size, img_size))(img) #이미지 사이즈 조정
          img = transforms.ToTensor()(img) #Tensor 포멧으로 변경
          img = img.unsqueeze(0) #\차원 생성
          return img
      
      #이미지 전처리
      input_image = preprocess_image(image_path).to(device)
      
      with torch.no_grad(): #Autogred 비활성화
          detections = model_yolo(input_image)[0] #입력으로 들어온 이미지 객체 감지를 진행
          detections = non_max_suppression(detections, conf_thres=0.5, iou_thres=0.4)[0]

      class_Yolo_names = ['infertility_period', 'transitional_period', 'ovulatory_phase', 'foreign_substance', 'error']

      label = 4
      if detections is not None:
          original_image = Image.open(image_path)
          draw = ImageDraw.Draw(original_image)

          for detection in detections:
              class_idx = int(detection[5])
              if class_idx == 0:
                 if label == 1: continue
                 elif label == 2: continue
                 else : label = class_idx

              elif class_idx == 1:
                  if label == 2: continue
                  else: label = class_idx

              elif class_idx == 2: label = class_idx

              elif class_idx == 3:
                  if label == 0: continue
                  elif label == 1: continue
                  elif label == 2: continue
                  else: label = class_idx

          res = class_Yolo_names[label]
          print("Yolo res >",res)

    return res


