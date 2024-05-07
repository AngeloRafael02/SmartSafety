from ultralytics import YOLO

# Load a model, use htop to analyze hardware performancex
model = YOLO('models/best.onnx')  # load model here

# Run batched inference on a list of images
results = model('rtsp://admin:Angelorafael69@192.168.1.99:554/Streaming/channels/101/',imgsz=800, vid_stride=1, agnostic_nms=True, max_det=100, iou=0.8, stream=True)  # return a generator of Results objects

# Process results generator
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs
