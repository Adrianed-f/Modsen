import unittest
import os
import shutil
from PIL import Image
from compare_folders import compare_folders

class TestCompareFolders(unittest.TestCase):

    def setUp(self):
        self.folder1 = 'tests/test_images_folder1'
        self.folder2 = 'tests/test_images_folder2'
        os.makedirs(self.folder1, exist_ok=True)
        os.makedirs(self.folder2, exist_ok=True)
        # Create different dummy images
        img1 = Image.new('RGB', (10, 10), color = 'red')
        img1.save(os.path.join(self.folder1, 'test_image1.jpg'))
        img2 = Image.new('RGB', (10, 10), color = 'blue')
        img2.save(os.path.join(self.folder1, 'test_image2.jpg'))
        img3 = Image.new('RGB', (10, 10), color = 'green')
        img3.save(os.path.join(self.folder2, 'test_image3.jpg'))
        img4 = Image.new('RGB', (10, 10), color = 'yellow')
        img4.save(os.path.join(self.folder2, 'test_image4.jpg'))

    def tearDown(self):
        shutil.rmtree(self.folder1)
        shutil.rmtree(self.folder2)

    def test_compare_folders(self):
        duplicates = compare_folders(self.folder1, self.folder2)
        self.assertEqual(len(duplicates), 0)

if __name__ == '__main__':
    unittest.main()