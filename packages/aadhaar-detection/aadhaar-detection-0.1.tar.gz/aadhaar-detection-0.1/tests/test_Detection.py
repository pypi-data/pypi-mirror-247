# tests/test_detection.py

import unittest
from aadhaar_detection import AadhaarDetector  # Update the import statement

class TestAadhaarDetector(unittest.TestCase):

    def test_detection_on_aadhaar_image(self):
        # Assuming you have a sample Aadhaar image for testing
        aadhaar_detector = AadhaarDetector()
        result = aadhaar_detector.detect_aadhaar('path_to_aadhaar_test_image.jpg')
        self.assertTrue(result['detected'], "Aadhaar not detected in the image")

    def test_detection_on_non_aadhaar_image(self):
        # Assuming you have a sample non-Aadhaar image for testing
        aadhaar_detector = AadhaarDetector()
        result = aadhaar_detector.detect_aadhaar('path_to_non_aadhaar_test_image.jpg')
        self.assertFalse(result['detected'], "Aadhaar incorrectly detected in a non-Aadhaar image")

if __name__ == '__main__':
    unittest.main()
