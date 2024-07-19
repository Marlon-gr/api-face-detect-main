import asyncio
import logging

from flask import Blueprint, jsonify, request

from api_face_detect.service.detector_service import DetectorService
from api_face_detect.util.api_util import ApiUtil

detection_route = Blueprint('detection_route', __name__)


@detection_route.route("/image/face-detect", methods=['POST'])
def image_detect():
    api_util = ApiUtil()
    service = DetectorService()

    image_np, cropped = api_util.is_valid_request(request)
    faces_detected = service.face_detector(image_np, cropped)
    # Output response.
    output_response = {
        'number_of_faces': len(faces_detected),
        'cropped_faces': cropped,
        'data': faces_detected
    }
    logging.getLogger('face_detect.controller').info({
        "detail": "Success",
        "number_of_faces": output_response["number_of_faces"]
    })
    return jsonify(output_response), 200


@detection_route.route("/image/full-face-detect", methods=['POST'])
def image_full_detect():
    api_util = ApiUtil()
    service = DetectorService()
    image_b64, cropped = api_util.is_full_valid_request(request)
    # Start loops.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Get faces.
    faces_detected = service.full_face_detector(image_b64, cropped, loop)
    # Output response.
    output_response = {
        'number_of_faces': len(faces_detected),
        'cropped_faces': cropped,
        'data': faces_detected
    }
    logging.getLogger('face_detect.controller').info({
        "detail": "Success",
        "number_of_faces": output_response["number_of_faces"]
    })
    return jsonify(output_response), 200
