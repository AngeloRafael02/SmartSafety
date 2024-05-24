from flask import Flask, Response, render_template
from ultralytics import YOLO
import time
import cv2

app = Flask(__name__)

# Open the webcam (usually, 0 for the default camera, 1 for additional ones)
camera = cv2.VideoCapture("rtspsrc location=rtsp://admin:Angelorafael69@192.168.1.99:554/Streaming/channels/101/ short-header=True buffer-mode=0 do-rtsp-keep-alive=True is-live=True onvif-rate-control=False onvif-mode=True drop-on-latency=True latency=0 ! rtph265depay ! h265parse ! avdec_h265 output-corrupt=False skip-frame=5 thread-type=Frame ! videoconvert ! appsink drop=1", cv2.CAP_GSTREAMER)
#camera = cv2.VideoCapture("rtsp://admin:Angelorafael69@192.168.1.99:554/Streaming/channels/101/", cv2.CAP_FFMPEG)
# reduce buffer size
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

#model = YOLO('models_800/best_int8_openvino_model/')
model = YOLO('models_640/best_ncnn_model/')

def generate_frames():

    while True:
        # Read a frame from the webcam
        success, frame = camera.read()  # If the camera is open
        if not success:
            break
        else:
            # Run object detection on the frame
            results = model.predict(frame, conf=0.6, iou=0.8, imgsz=640, half=True, max_det=10, stream_buffer=False, agnostic_nms=True)  # Perform detection
            # Draw bounding boxes and labels on the frame 
            detected_frame = results[0].plot()  # This renders the detections

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', detected_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            frame = buffer.tobytes()

            # Use a multipart response to continuously send frames
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # A simple HTML page with an embedded video stream
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Stream the video feed as multipart content
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='127.0.0.1', port=3000)
