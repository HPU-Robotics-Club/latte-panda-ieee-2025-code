import numpy
import pupil_apriltags as apriltags


class AprilTagDetector:
    def __init__(self):
        self.detector = apriltags.Detector(quad_decimate=1.5)  # TODO: Make this a parameter when integrating this

    def detect_april_tags(self, greyscale_img: numpy.ndarray) -> list[apriltags.Detection]:
        """
        Detects AprilTags in the greyscale image provided.
        :param greyscale_img: The greyscale image.
        :return: A list of detection results. An empty list will return if there are no AprilTags found.

        :Example:
        >>> results = detector.detect_april_tags(greyscale_img)
        >>> results[0].tag_id
        1
        """
        return self.detector.detect(greyscale_img)  # This actually returns a list of apriltags.Detection
