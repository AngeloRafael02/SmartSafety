from ultralytics import YOLO

# Load a YOLOv8n PyTorch model
model = YOLO('models/best.pt')

## Export the model to openVINO format
#model.export(format='openvino', imgsz=800, half=True, int8=True)  # creates 'best_int8_openvino_model/'

## Export the model to ONNX format
#model.export(format='onnx', imgsz=800, half=True, simplify=True)  # creates 'best.onnx'

## Export the model to NCNN format
#model.export(format='ncnn', imgsz=800, half=True)  # creates 'best_int8_openvino_model/'

## Export the model to TensorRT Format
#model.export(format='engine', imgsz=800, half=True, simplify=True, workspace=1.0, device=0)  # creates 'best.engine'