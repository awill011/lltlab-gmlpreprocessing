# Gesture Model Preprocessing Pipeline

**Video frame preprocessing and dataset preparation for gesture recognition · LLT Lab, UC Merced**

![Python](https://img.shields.io/badge/Python-3.9+-blue) ![PyTorch](https://img.shields.io/badge/Framework-PyTorch-orange) ![YOLOv8](https://img.shields.io/badge/Model-YOLOv8-green)

---

## What this does

This repo contains the preprocessing pipeline for the LLT Lab's gesture recognition project. Raw video data from behavioral research sessions is processed into structured frame datasets ready for model training. The goal is to automate detection of pointing and writing gestures in lab video, reducing the need for manual behavioral coding.

---

## Pipeline stages

1. **Frame extraction** — OpenCV pulls individual frames from annotated lab video at configurable intervals
2. **Annotation processing** — CVAT-exported labels are parsed and aligned to extracted frames
3. **Dataset structuring** — frames and labels are organized into PyTorch-compatible tensor datasets
4. **YOLOv8 preparation** — data formatted for Ultralytics YOLOv8 training pipeline

---

## Tech stack

| Library | Purpose |
|---|---|
| `torch` / `torchvision` | Tensor-based dataset pipeline |
| `ultralytics` (YOLOv8) | Object detection model training |
| `opencv-python` | Video frame extraction and image processing |
| `pandas` / `polars` | Annotation and metadata handling |
| `matplotlib` | Frame and annotation visualization |
| `numpy` / `scipy` | Numerical operations |

---

## How to run it

```bash
git clone https://github.com/awill011/lltlab-gmlpreprocessing
cd lltlab-gmlpreprocessing
pip install -r requirements.txt

python scripts/.py
```

> Note: Raw video data is not included in this repo (participant privacy). Scripts expect annotated video frames in a local `data/` directory.

---

## Context

Part of the LLT Lab Biliteracy Project at UC Merced, which studies bilingual reading comprehension and embodied cognition. This preprocessing pipeline feeds into a gesture recognition model designed to automate behavioral coding of participant interactions — a task that currently requires significant manual annotation time.

---

*LLT Lab · UC Merced · [@awill011](https://github.com/awill011)*
