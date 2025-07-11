# SmartSafety
Proof of concept using YOLOv8 for Object Detection, specifically in detecting Personal Protective Equipment (PPEs)
- [Thesis Paper for this project](https://docs.google.com/document/d/1CD70BwggRvtN7NG-7XvpduxyeaSWInP7A-58_7Fy-Zo/edit?usp=sharing)
- [GDrive Link](https://drive.google.com/drive/folders/1GjP6j3rx3E-O5p5ZIsNx8JrNMGOGS661?usp=sharing) used for Training via Google Colab


## Pictures from Past Tests:
![plot](./photo-collage.png(2).png)

## DISCLAIMER
This repo/project is merely a proof of concept to show the effectiveness of using Machine Vision and Deep Learning to create a system that can detect if workers are using PPE and is not to be deployed in an actual setting.

## Benchmarks

### P Curve
![plot](./benchmarks/P_curve%20(1).png)

### R Curve
![plot](./benchmarks/R_curve%20(1).png)

### F1 Curve
![plot](./benchmarks/F1_curve%20(1).png)

### Normalised Confusion Matrix
![plot](./benchmarks/confusion_matrix_normalized%20(1).png)

## Hardware Requirements:
- Raspberry Pi (preferably Pi 5, or newer for better performance
- SD card with Raspberry Pi OS installed
- CCTV Camera with RTSP protocol support
- Ethernet Cables
- Router 

## Software Requirements:
- Python 3.x: Ensure you have Python 3 installed.
- pip: Python package installer.
- Other Python Libraries: Refer to requirements.txt for a complete list.

## Installation Steps:
- Clone the repository:
```
git clone https://github.com/YOUR_USERNAME/ppe-detection-rpi.git
cd ppe-detection-rpi
```
- Create a virtual environment (recommended):

python3 -m venv venv
source venv/bin/activate

Install dependencies:
```
pip install -r requirements.txt
```
Note: Some dependencies, like OpenCV, might require additional system-level packages on Raspberry Pi. Refer to their official documentation if you encounter issues.

