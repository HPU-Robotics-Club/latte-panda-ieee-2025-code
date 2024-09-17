import unittest

import cv2

from util.april_tag import *


class AprilTagDetectorTests(unittest.TestCase):
    def test_detect_april_tags(self):
        detector = AprilTagDetector()

        self.verify_april_tag(detector, 4, "resources/april_tags/april_tag1.jpg")  # https://www.youtube.com/watch?v=QyZKwqk_p8A&ab_channel=MathaGoram
        self.verify_april_tag(detector, 5, "resources/april_tags/april_tag2.jpg")  # https://www.mathworks.com/help/vision/ref/readapriltag.html
        self.verify_april_tag(detector, 3, "resources/april_tags/april_tag3.jpg")  # https://engprojects.tcnj.edu/robot-guide-dog/apriltags/

    def verify_april_tag(self, detector: AprilTagDetector, expected_tag_count: int, image_path: str):
        img = cv2.imread(image_path)
        greyscale_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        results = detector.detect_april_tags(greyscale_img)
        actual_tag_count = len(results)

        self.assertEqual(expected_tag_count, actual_tag_count, f"Expected tag count of {expected_tag_count} but got {actual_tag_count}.\nImage path: {image_path}")


if __name__ == '__main__':
    unittest.main()
