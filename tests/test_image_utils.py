import unittest
import os
import shutil
from PIL import Image
from image_utils import load_images_from_folder, compute_hashes, find_duplicates

class TestImageUtils(unittest.TestCase):

    def setUp(self):
        self.test_folder = 'tests/test_images'
        os.makedirs(self.test_folder, exist_ok=True)
        self.image_path = os.path.join(self.test_folder, 'test_image.jpg')
        # Create a dummy image
        img = Image.new('RGB', (10, 10), color = 'red')
        img.save(self.image_path)

    def tearDown(self):
        shutil.rmtree(self.test_folder)

    def test_load_images_from_folder(self):
        images, paths = load_images_from_folder(self.test_folder)
        self.assertEqual(len(images), 1)
        self.assertEqual(paths[0], self.image_path)

    def test_compute_hashes(self):
        images, _ = load_images_from_folder(self.test_folder)
        hashes = compute_hashes(images)
        self.assertEqual(len(hashes), 1)

    def test_find_duplicates(self):
        images, paths = load_images_from_folder(self.test_folder)
        hashes = compute_hashes(images)
        duplicates = find_duplicates(hashes, paths)
        self.assertEqual(len(duplicates), 0)

if __name__ == '__main__':
    unittest.main()