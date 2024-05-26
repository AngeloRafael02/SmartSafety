from flask import Flask, Response, render_template, send_from_directory
from dotenv import load_dotenv
from ultralytics import YOLO
import datetime
import time
import cv2
import subprocess

import numpy as np
import db
import fs
import threading
import socket
import signal
import sys
import os

SAMBA_MOUNT_POINT = '/mnt/samba'

load_dotenv()
# Crete temporary directory for screenshots
os.makedirs('screenshots', exist_ok=True)

app = Flask(__name__)

# Open the webcam (usually, 0 for the default camera, 1 for additional ones)
camera = cv2.VideoCapture("rtspsrc location=rtsp://admin:Angelorafael69@192.168.1.99:554/Streaming/channels/101/ short-header=True buffer-mode=0 do-rtsp-keep-alive=True is-live=True onvif-rate-control=False onvif-mode=True drop-on-latency=True latency=0 ! rtph265depay ! h265parse ! avdec_h265 output-corrupt=False skip-frame=5 thread-type=Frame ! videoconvert ! appsink drop=1", cv2.CAP_GSTREAMER)
#camera = cv2.VideoCapture("rtsp://admin:Angelorafael69@192.168.1.99:554/Streaming/channels/101/", cv2.CAP_FFMPEG) # for Laptop only

# reduce buffer size
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# Frame dimensions
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = camera.get(cv2.CAP_PROP_FPS)
print(f"Frame dimensions: {width}x{height}, FPS: {fps}")

#model = YOLO('models_800/best_int8_openvino_model/') #for laptop only
model = YOLO('models_640/best_ncnn_model/', task='detect')

now = datetime.datetime.now()
show_live_camera = True  # Flag to toggle between live camera and uploaded content
last_screenshot_time = time.time()  # Variable to track the last screenshot time
screenshot_interval = 5  # Set the interval for taking screenshots (in seconds)


def generate_frames():
    global last_screenshot_time
    while True:
        # Read a frame from the webcam
        success, frame = camera.read()  # If the camera is open
        if not success:
            break
        else:
            # Run object detection on the frame
            results = model.predict(frame, conf=0.6, iou=0.8, imgsz=640, half=True, max_det=10, stream_buffer=True, agnostic_nms=True, vid_stride=12)  # Perform detection
            if results and results[0].boxes:
                current_time = time.time()
                if current_time - last_screenshot_time >= screenshot_interval:
                    screenshot_thread = threading.Thread(target=take_screenshot, args=(results,))
                    screenshot_thread.start()  # Start a thread to take a screenshot
                    last_screenshot_time = current_time
                    #screenshot_thread.stop()
                    #screenshot_thread.join()

            # Draw bounding boxes and labels on the frame
            detected_frame = results[0].plot()  # This renders the detections
            print(results[0].boxes.cls.numpy())

            # Convert the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', detected_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            frame = buffer.tobytes()

            # Use a multipart response to continuously send frames
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()


def take_screenshot(results):
    '''Takes a Screenshot and saves it to a file server and its metadata in a database'''
    #Setting up screenshot and metadata
    hostname = socket.gethostname()
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    screenshot_fileLoc = f'screenshots/{hostname}_{current_time}.jpg' #temporary local storage location
    fileName = screenshot_fileLoc[len('screenshots/'):-len('.jpg')]

    #Create an array storing the frequencies of objects,
    completeArr=[0,1,2,3,3,4,5]
    classArray = results[0].boxes.cls.numpy().copy()
    notFoundArr = np.setdiff1d(np.array(completeArr),np.array(classArray)).tolist()
    print("NOTFound" + str(notFoundArr))

    # Temporarily stores screenshot to local directory
    cv2.imwrite(screenshot_fileLoc, results[0].plot())
    newURL = f'{datetime.datetime.now().strftime("%Y-%m-%d")}/{hostname}'

    # Make Directory/Path if not Found
    if fs.checkDir(currentFolder) == False:
        fs.mkdirSamba(dateFolder)
        fs.mkdirSamba(currentFolder)
        time.sleep(0.5)
    # Add screenshot to File Server
    fs.putSamba(screenshot_fileLoc, f'{newURL}/{screenshot_fileLoc[len("screenshots/"):]}')

    # Add screenshot metadata to Database
    for value in notFoundArr:
        db.upload_metadata(fileName, newURL, os.getenv('HOSTNAME_ID'),datetime.datetime.now(), int(value + 1))

    # Delete Excess Photos from temp directory
    try:
        os.remove(screenshot_fileLoc) #Delete Screenshot in local machine Permanently
        empty_temp()
    except FileNotFoundError:
        print(f"File '{screenshot_fileLoc}' not found. Skipping removal.")
    except Exception as e:
        print(f"An error occurred: {e}")


def empty_temp():
    """Removes any pictures in temporary folder"""
    try:
        folder_name = "screenshots"
        folder_path = os.path.join(os.path.dirname(__file__), folder_name)
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def cleanup():
    empty_temp()
    sys.exit(0)


@app.route('/')
def index():
    # A simple HTML page with an embedded video stream
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Stream the video feed as multipart content
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/updates')
def logs():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='apron' ORDER BY dateandtime DESC;")
    data1 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='bunny suit' ORDER BY dateandtime DESC;")
    data2 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='mask' ORDER BY dateandtime DESC;")
    data3 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='gloves' ORDER BY dateandtime DESC;")
    data4 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='goggles' ORDER BY dateandtime DESC;")
    data5 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='headcap' ORDER BY dateandtime DESC;")
    data6 = cur.fetchall()
    cur.close()
    conn.close()

    # A simple HTML page with an embedded video stream
    return render_template('updates.html', data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6)

@app.route('/logs')
def update():
    conn = db.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='apron' ORDER BY dateandtime DESC LIMIT 15;")
    data1 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='bunny suit' ORDER BY dateandtime DESC LIMIT 15;")
    data2 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='mask' ORDER BY dateandtime DESC LIMIT 15;")
    data3 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='gloves' ORDER BY dateandtime DESC LIMIT 15;")
    data4 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='goggles' ORDER BY dateandtime DESC LIMIT 15;")
    data5 = cur.fetchall()
    cur.execute("SELECT * FROM undetected_items WHERE detectedobject='headcap' ORDER BY dateandtime DESC LIMIT 15;")
    data6 = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('contents2.html', data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6)

@app.route('/images/<path:filename>')
def serve_image(filename):
    print(SAMBA_MOUNT_POINT + currentFolder, filename + ".jpg")
    return send_from_directory(SAMBA_MOUNT_POINT + "/" + currentFolder, filename + ".jpg")

# Run the Flask app
if __name__ == '__main__':
    signal.signal(signal.SIGTERM, cleanup)
    dateFolder = datetime.datetime.now().strftime("%Y-%m-%d")
    hostFolder = socket.gethostname()
    currentFolder = f'{dateFolder}/{hostFolder}'
    try:
        fs.mkdirSamba(dateFolder)
        fs.mkdirSamba(currentFolder)
        app.run(debug=True, threaded=True, host='0.0.0.0',load_dotenv=True, port=3000)
    except KeyboardInterrupt:
        pass
