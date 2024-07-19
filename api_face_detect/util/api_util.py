import base64
import binascii
import logging
import os

import cv2
import numpy as np

from api_face_detect.util.response_error import raise_error


class ApiUtil:

    @staticmethod
    def to_numpy(encoded):
        """Convert base64 to numpy.
        Args:
            encoded (str): Base64 encoded string to decode.
        Returns:
            'np.ndarray: An ndimentional array of the input image.
        Raises:
            ValueError: Wrong base64 image.
        """
        nparr = np.frombuffer(base64.b64decode(encoded), np.uint8)
        try:
            np_res = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            np_res = cv2.cvtColor(np_res, cv2.COLOR_BGR2RGB)
        except cv2.error:
            raise ValueError('No correct base64 value.')
        return np_res

    @staticmethod
    def is_base64(str_b64):
        """Check if str represents base64 format.
        Args:
            str_b64 (str): String containing base64 code.
        Returns:
            bool: True if input is base64 encoded, raise ValueError otherwise.
        Raises:
            ValueError: Wrong base64 input.
        """
        try:
            base64.b64decode(str_b64)
        except binascii.Error:
            raise ValueError('No correct base64 value.')
        return True

    def is_valid_request(self, request):
        """Check if the request has the valid parameters and values.
        Args:
            request (Request): Object of the request.
        Returns:
            vector: (np.ndarray) an n dimensional array of the 64 image.
        """
        image, cropped = self.__is_valid(request)
        # str represents base64?
        image_np = self.__is_64image(image)  # return an numpy array.
        # ---
        return image_np, cropped

    def is_full_valid_request(self, request):
        """Check if the request has the valid parameters and values.
        Args:
            request (Request): Object of the request.
        Returns:
            vector: (np.ndarray) an n dimensional array of the 64 image.
        """
        image, cropped = self.__is_valid(request)
        # str represents base64?
        self.is_base64(image)
        # ---
        return image, cropped

    @staticmethod
    def __is_valid(request):
        """Check if the request has the valid parameters and values.
        Args:
            request (Request): Object of the request.
        Returns:
            vector: () 64 image and cropped.
        """
        if not request.is_json:
            raise_error(400)
        result = request.get_json()
        # The request contains the correct parameters?
        if not all(key in result for key in ['image', 'cropped']):
            raise_error(404)
        # Contains a boolean value?
        if isinstance(result['cropped'], bool) is False:
            raise_error(408)
        return result['image'], result['cropped']

    def __is_64image(self, image):
        """Check if the image is base64 valid.
        Args:
            image (str): String containing base64 code.
        Returns:
            np.ndarray: An n dimensional array of the 64 image.
        """
        image_np = image
        try:
            self.is_base64(image_np)
            image_np = self.to_numpy(image_np)
        except ValueError:
            raise_error(401)
        # Is valid numpy?
        if image_np is None:
            raise_error(401)
        return image_np

    @staticmethod
    def environ_value(environ):
        """
        Get values from operating system environment.
        Args:
            environ: (str) Environment variable name.
        Returns:
            (str) Value of the environment variable.
        """
        try:
            return os.environ[environ]
        except KeyError:
            logging.getLogger('face_detect.api').info(
                environ + ' > not found')
            raise_error(428)
