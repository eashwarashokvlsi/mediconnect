import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from common import classify

class ClassifierTests(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(classify({"heartRate":76,"spo2":98,"temperature":36.8})["status"], "NORMAL")
    def test_low_oxygen_is_abnormal(self):
        result = classify({"heartRate":76,"spo2":89,"temperature":36.8})
        self.assertEqual(result["status"], "ABNORMAL")
        self.assertEqual(result["breaches"][0]["metric"], "spo2")

if __name__ == "__main__": unittest.main()

