import unittest
from app import predict_rent

class TestPrediction(unittest.TestCase):
    def test_basic_prediction(self):
        result = predict_rent(2, 1, 'Flat', 'OX1')
        self.assertGreater(result, 500)
        self.assertLess(result, 3000)
    
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            predict_rent(-1, 1, 'Flat', 'OX1')

if __name__ == '__main__':
    unittest.main()