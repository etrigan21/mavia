from detector import *
import os

def main():
    videoPath = 0
    configPath = os.path.join("models", "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
    modelPath = os.path.join("models", "frozen_inference_graph.pb")
    classPath = os.path.join("models", "coco.names")
    print(classPath)
    detector = Detector(videoPath, configPath, modelPath, classPath)
    detector.onVideo()

if __name__ == '__main__':
    main()