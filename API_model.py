from efficientnet_pytorch import EfficientNet
from torchvision import transforms
from PIL import Image, ImageDraw
from models.experimental import attempt_load
from utils.general import non_max_suppression
import os
import torch

def predict(image_path):
    # EfficientNet 모델 설정
    model_name = 'efficientnet-b5'
    num_classes = 5
    model = EfficientNet.from_pretrained(model_name, num_classes=num_classes)
    model_path = '/home/intin-dev-001/HealthOverView/BackEnd/model/president_model0823.pt'
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()

    # YOLOv5 모델 설정
    yolo_model = attempt_load('/home/intin-dev-001/HealthOverView/BackEnd/model/best0823.pt')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    yolo_model.to(device)
    yolo_model.eval()

    # 클래스 네임 정의 (비가임기, 과도기, 가임기, 이물질, 에러(리트라이))
    class_names = ['infertility_period', 'transitional_period', 'ovulatory_phase', 'foreign_substance', 'retry']

    # Yolo이미지 전처리
    def preprocess_image(img_size=640):
        img = Image.open(image_path).convert('RGB')
        img = transforms.Resize((img_size, img_size))(img)
        img = transforms.ToTensor()(img)
        img = img.unsqueeze(0)
        return img

    # effcientnet 전처리
    def preprocess_image_efficientnet(img_size=456):
        img = Image.open(image_path).convert("RGB")
        transform = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        img = transform(img)
        img = img.unsqueeze(0)
        return img

    # effcientnet 모델 예측
    def predict_efficientnet(image):
        with torch.no_grad():
            outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        return class_names[predicted.item()]

    # Yolo 모델 예측
    def predict_yolo(image):
        input_image = image.to(device)
        with torch.no_grad():
            detections = yolo_model(input_image)[0]
            detections = non_max_suppression(detections, conf_thres=0.5, iou_thres=0.4)[0]

        yolo_label = 4
        if detections is not None:
            for detection in detections:
                class_idx = int(detection[5])
                confidence = detection[4]
                bounding_box = detection[:4]

                x_min, y_min, x_max, y_max = map(int, bounding_box)  # Convert to integers

                class_idx = int(detection[5])
                if class_idx == 0:
                    if yolo_label == 1:
                        continue
                    elif yolo_label == 2:
                        continue
                    else:
                        yolo_label = class_idx

                elif class_idx == 1:
                    if yolo_label == 2:
                        continue
                    else:
                        yolo_label = class_idx

                elif class_idx == 2:
                    yolo_label = class_idx

                elif class_idx == 3:
                    if yolo_label == 0:
                        continue
                    elif yolo_label == 1:
                        continue
                    elif yolo_label == 2:
                        continue
                    else:
                        yolo_label = class_idx

        return class_names[yolo_label]

    # 받은 이미지 모델별 전처리
    image_efficientnet = preprocess_image_efficientnet()
    efficientnet_label = predict_efficientnet(image_efficientnet)

    # 전처리한 이미지 모델 예측
    image_yolo = preprocess_image()  # Use the correct preprocessing function for YOLO
    yolo_label = predict_yolo(image_yolo)

    # 예측 결과 출력
    print("EfficientNet Predicted Label:", efficientnet_label)
    print("YOLO Predicted Label:", yolo_label)

    # 최종 예측
    if efficientnet_label == 'retry':
        result = efficientnet_label
    else:
        if yolo_label == 'foreign_substance' or yolo_label == 'retry':
            result = efficientnet_label
        else:
            result = yolo_label
    print("Final Result:", result)
    return result
