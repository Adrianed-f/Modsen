import unittest
import os
import shutil
from PIL import Image
from tensorflow.keras.models import Model
from feature_extraction import feature_extraction_model_keras, extract_features_keras

class TestFeatureExtraction(unittest.TestCase):

    def setUp(self):
        self.test_folder = 'tests/test_images'
        os.makedirs(self.test_folder, exist_ok=True)
        self.image_path = os.path.join(self.test_folder, 'test_image.jpg')
        # Create a dummy image
        img = Image.new('RGB', (10, 10), color = 'red')
        img.save(self.image_path)

    def tearDown(self):
        shutil.rmtree(self.test_folder)

    def test_feature_extraction_model_keras(self):
        model = feature_extraction_model_keras()
        self.assertIsInstance(model, Model)

    def test_extract_features_keras(self):
        model = feature_extraction_model_keras()
        features = extract_features_keras([self.image_path], model)
        self.assertEqual(features.shape[0], 1)

if __name__ == '__main__':
    unittest.main()