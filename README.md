Gesture Model Preprocessing Pipeline
Video frame preprocessing and dataset preparation for gesture recognition · LLT Lab, UC Merced
Python
PyTorch
YOLOv8 · Ultralytics
OpenCV
Computer Vision
pandas · numpy · matplotlib
What this does
This repo contains the preprocessing pipeline for the LLT Lab's gesture recognition project. Raw video data from behavioral research sessions is processed into structured frame datasets ready for model training. The goal is to automate detection of pointing and writing gestures in lab video, reducing the need for manual behavioral coding.
Pipeline stages
Frame extraction — OpenCV pulls individual frames from annotated lab video at configurable intervals
Annotation processing — CVAT-exported labels are parsed and aligned to extracted frames
Dataset structuring — frames and labels are organized into PyTorch-compatible tensor datasets
YOLOv8 preparation — data formatted for Ultralytics YOLOv8 training pipeline
Tech stack
Library	Purpose
torch / torchvision	Tensor-based dataset pipeline
ultralytics (YOLOv8)	Object detection model training
opencv-python	Video frame extraction and image processing
pandas / polars	Annotation and metadata handling
matplotlib	Frame and annotation visualization
numpy / scipy	Numerical operations
