from flask import Flask, Response, render_template
from ultralytics import YOLO
import time
import cv2
import subprocess

app = Flask(__name__)

# Open the webcam (usually, 0 for the default camera, 1 for additional ones)
camera = cv2.VideoCapture("rtspsrc location=rtsp://admin:Angelorafael69@192.168.1.99:554/Streaming/channels/101/ short-header=True buffer-mode=0 do-rtsp-keep-alive=True is-live=True onvif-rate-control=False onvif-mode=True drop-on-latency=True latency=0 ! rtph265depay ! h265parse ! avdec_h265 output-corrupt=False skip-frame=5 thread-type=Frame ! videoconvert ! appsink drop=1", cv2.CAP_GSTREAMER)
#camera = cv2.VideoCapture("rtsp://admin:Angelorafael69@192.168.1.99:554/Streaming/channels/101/", cv2.CAP_FFMPEG)

# reduce buffer size
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Frame dimensions
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 12 #camera.get(cv2.CAP_PROP_FPS)
print(f"Frame dimensions: {width}x{height}, FPS: {fps}")

#model = YOLO('models_800/best_int8_openvino_model/')
model = YOLO('models_640/best_ncnn_model/', task='detect')

def generate_frames():

    while True:
        # Read a frame from the webcam
        success, frame = camera.read()  # If the camera is open
        if not success:
            break
        else:
            # Run object detection on the frame
            results = model.predict(frame, conf=0.6, iou=0.8, imgsz=640, half=True, max_det=10, stream_buffer=True, agnostic_nms=True, vid_stride=12)  # Perform detection
            # Draw bounding boxes and labels on the frame
            detected_frame = results[0].plot()  # This renders the detections

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', detected_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            frame = buffer.tobytes()

            # Use a multipart response to continuously send frames
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()



def main():
    while True:
        # Read a frame from the webcam
        success, frame = camera.read()  # If the camera is open
        if not success:
            break
        else:
            # Run object detection on the frame
            results = model.predict(frame, conf=0.6, iou=0.8, imgsz=640, half=True, max_det=10, stream_buffer=True, agnostic_nms=True)
            # Draw bounding boxes and labels on the frame
            detected_frame = results[0].plot()  # This renders the detections

            # Encode frame to h265 using ffmpeg (replace with your ffmpeg path)
            process = subprocess.Popen(['ffmpeg',
                        '-v', 'debug',
        		'-y',  # Overwrite output files
        		'-f', 'rawvideo',
        		'-vcodec', 'rawvideo',
        		'-pix_fmt', 'bgr24',
        		'-s', f'{width}x{height}',  # Size of one frame
        		'-r', str(int(fps)),  # Frames per second
        		'-i', '-',  # The input comes from a pipe
        		'-c:v', 'libx265',  # Use H.264 codec
        		'-preset', 'ultrafast',  # Use ultrafast preset for low latency
        		'-f', 'rtsp', 'http://127.0.0.1:8554/test'], stdin=subprocess.PIPE)

            # Write frame to ffmpeg process
            process.stdin.write(frame.tobytes())

    # Release resources
    camera.release()
    process.wait()

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
    #app.run(debug=True, threaded=True, host='0.0.0.0', port=3000)
    main()
