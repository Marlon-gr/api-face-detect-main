
import base64
from io import BytesIO

import dlib
import face_recognition_models as f_r_m
from PIL import Image

from api_face_detect.service.requisitions_service import \
    RequisitionsService
from api_face_detect.util.api_util import ApiUtil
from api_face_detect.util.response_error import raise_error


class DetectorService:

    __fr_model = f_r_m.face_recognition_model_location()
    rotate_endpoints = list()  # Preprocess API (image/rotate-by-angle)

    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.pose_predictor = f_r_m.pose_predictor_five_point_model_location()
        self.utils = ApiUtil()

    def face_detector(self, image_np, cropped):
        faces = None
        # Number of times it should up sample.
        number_of_times_to_up_sample = 0
        try:
            faces = self.detector(image_np, number_of_times_to_up_sample)
        except TypeError:
            raise_error(401)
        return self.get_box_from_faces(faces, image_np, cropped)

    def full_face_detector(self, image_b64, cropped, loop):
        b64_np = self.utils.to_numpy(image_b64)
        face_locations = self.detector(b64_np, 0)

        if len(face_locations) == 0:
            pre_process_response = self.get_rotated_b64(image_b64, loop)
            for pre_process in pre_process_response:
                if pre_process[0] == 200:
                    b64_np = self.utils.to_numpy(pre_process[1]['b64_image'])
                    face_locations = self.detector(b64_np, 0)
                if len(face_locations) > 0:
                    break
        # face was not found in the image.
        if len(face_locations) == 0:
            raise_error(403)
        return self.get_box_from_faces(face_locations, b64_np, cropped)

    def get_box_from_faces(self, faces, image_np, cropped):
        bounding_boxes_and_base64_face = []

        for box in faces:
            b = self.get_box(box, image_np)
            bounding_box = [{'left': b.left(), 'top': b.top(), 'right': b.right(), 'bottom': b.bottom()}]
            # Return cropped face in base 64 string.
            if cropped:
                bounding_boxes_and_base64_face.append({
                    'bounding_box': bounding_box,
                    'cropped_face': self.get_base64_from_bounding_box(b, image_np),
                    'landmarks': self.get_landmarks(image_np, b)
                })
            else:  # Without cropped face.
                bounding_boxes_and_base64_face.append({
                    'bounding_box': bounding_box,
                    'landmarks': self.get_landmarks(image_np, b)
                })
        return bounding_boxes_and_base64_face

    @staticmethod
    def get_base64_from_bounding_box(box, image_np):
        buff = BytesIO()
        cropped_face = image_np[box.top():box.bottom(), box.left():box.right()]
        pil_img = Image.fromarray(cropped_face)
        pil_img.save(buff, "PNG")
        new_image_64 = base64.b64encode(buff.getvalue()).decode("utf-8")
        return new_image_64

    def get_rotated_b64(self, base_64, loop):
        """
        Get image in base64 code, rotated at angles
        [0, 90. 180, 270]. Integration done with the api-preprocess.
        Args:
            base_64: (str) Containing base64 code from image 1.
            loop: (event_loop) Event loop in the current OS thread.
        Returns:
            (list) Responses to requests made to the api-face-detect
                   (8 request).
        """
        requisitions_service = RequisitionsService()
        # Payload and url for ' Preprocess API'.
        self.pre_process_url_payload(base_64)
        # Rotate image at various angles (90, 180, 270)
        pre_process_response = requisitions_service.start_loop(
            loop, self.rotate_endpoints)
        return pre_process_response

    def pre_process_url_payload(self, base_64) -> None:
        """
        Process and get the url and the payload for the request for base64.
        Args:
            base_64: (str) Containing base64 code from image 1.
        Returns:
        """
        url = self.utils.environ_value('PRE_PROCESS_URL')
        for angle in [90, 180, 270]:
            self.rotate_endpoints.append([
                url, {"image": base_64, "angle": angle}])

    def get_landmarks(self, image, face_locations) -> dict:
        shape_predictor = dlib.shape_predictor(self.pose_predictor)
        landmarks_five_point = shape_predictor(image, face_locations)

        landmarks = {
            "left_eye": {
                "x1": landmarks_five_point.part(0).x,
                "y1": landmarks_five_point.part(0).y,
                "x2": landmarks_five_point.part(1).x,
                "y2": landmarks_five_point.part(1).y
            },
            "right_eye": {
                "x1": landmarks_five_point.part(2).x,
                "y1": landmarks_five_point.part(2).y,
                "x2": landmarks_five_point.part(3).x,
                "y2": landmarks_five_point.part(3).y
            },
            "nose": {
                "x": landmarks_five_point.part(4).x,
                "y": landmarks_five_point.part(4).y
            }
        }
        return landmarks

    @staticmethod
    def get_box(box, image_np):
        left = max(box.left(), 0)
        top = max(box.top(), 0)
        right = min(box.right(), image_np.shape[1])
        bottom = min(box.bottom(), image_np.shape[0])
        return dlib.rectangle(left, top, right, bottom)
