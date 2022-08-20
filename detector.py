import cv2
import numpy as np
import time

class Detector:
    def __init__(self, videoPath, configPath, modelPath, classPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classPath = classPath
        
        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320,320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.55, 127.5, 127.5))
        self.net.setInputSwapRB(True)
        self.readClasses()

    def readClasses(self):
        with open(self.classPath, "r") as f:
            self.classList = f.read().splitlines()
        self.classList.insert(0, "__Background__")
        print(self.classList)

    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)
        
        if (cap.isOpened()==False):
            print('failed to open')
            return

        (success, image) = cap.read()
        prevTime = 0
        while success:
            newtime = time.time()
            fps = 1/(newtime - prevTime)
            print(fps)
            prevTime = newtime
            classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold = 0.4)
            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1,-1)[0])
            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = 0.5, nms_threshold = 0.2)
            if (len(bboxIdx) != 0):
                for i in range(0, len(bboxIdx)):
                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classList[classLabelID]
                    # classColor = [int(c) for c in self.colorList[classLabelID]]
                    x,y,w,h = bbox
                    displayText  = "{classname},{confidence}".format(classname=classLabel, confidence=classConfidence)
                    print("displayText", displayText)
                    cv2.rectangle(image, (x,y), (x+w, y+h), color=(255,255,255), thickness=1)
                    cv2.putText(image, displayText, (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1,(225,0,0),2)
            cv2.imshow("result", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            
            (success, image) = cap.read()
        cv2.destroyAllWindows()