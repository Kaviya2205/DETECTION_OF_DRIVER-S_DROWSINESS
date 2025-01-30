import cv2
import dlib
from scipy.spatial import distance
from config import EYE_AR_THRESH, EYE_AR_CONSEC_FRAMES
from utils import eye_aspect_ratio, play_alarm

class DrowsinessDetector:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        self.frame_counter = 0

    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)

        for face in faces:
            landmarks = self.predictor(gray, face)
            left_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
            right_eye = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]

            left_EAR = eye_aspect_ratio(left_eye)
            right_EAR = eye_aspect_ratio(right_eye)
            avg_EAR = (left_EAR + right_EAR) / 2.0

            if avg_EAR < EYE_AR_THRESH:
                self.frame_counter += 1
                if self.frame_counter >= EYE_AR_CONSEC_FRAMES:
                    play_alarm("alarm.wav")
            else:
                self.frame_counter = 0
