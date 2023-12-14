import unittest
import pathlib
from film_photo import FilmPhoto

class TestFilmPhoto(unittest.TestCase):
    def setUp(self):
        # Set up a FilmPhoto instance for use in the tests
        filename = "leo.jpeg"
        input_file_path = pathlib.Path(__file__).parent / filename
        self.photo = FilmPhoto(input_file_path)

    def test_initialization(self):
        # Test that the photo is correctly initialized
        self.assertEqual(self.photo._clarity, 0)
        self.assertEqual(self.photo._sharpness, 1)
        self.assertEqual(self.photo._grain, 0)
        self.assertEqual(self.photo._tonal_curve, 1)
        self.assertEqual(self.photo._warmness, 1)
        self.assertEqual(self.photo._rgb, {'red': 1, 'green': 1, 'blue': 1})

    def test_image_not_none(self):
        # Test the image not None
        self.assertIsNotNone(self.photo.image)

    def test_width_not_none(self):
        # Test the width not None
        self.assertIsNotNone(self.photo.width)

    def test_height_not_none(self):
        # Test the height not None
        self.assertIsNotNone(self.photo.height)
        
    def test_clarity_not_none(self):
        # Test the clarity not None
        self.assertIsNotNone(self.photo.clarity)
        
    def test_sharpness_not_none(self):
        # Test the sharpness not None
        self.assertIsNotNone(self.photo.sharpness)
    
    def test_grain_not_none(self):
        # Test the grain not None
        self.assertIsNotNone(self.photo.grain)
    
    def test_tonal_curve_not_none(self):
        # Test the tonal_curve not None
        self.assertIsNotNone(self.photo.tonal_curve)
    
    def test_warmness_not_none(self):
        # Test the warmness not None
        self.assertIsNotNone(self.photo.warmness)
    
    def test_rgb_not_none(self):
        # Test the rgb not None
        self.assertIsNotNone(self.photo.rgb)
        
    def test_clarity_in_bound(self):
        # Test that no error is raised for in-bound clarity
        self.photo.clarity = 0
        self.assertEqual(self.photo.clarity, 0)
        self.photo.clarity = 500
        self.assertEqual(self.photo.clarity, 500)
        self.photo.clarity = 1000
        self.assertEqual(self.photo.clarity, 1000)

    def test_clarity_out_of_bound(self):
        # Test that an error is raised for out-of-bound clarity
        with self.assertRaises(ValueError):
            self.photo.clarity = -1
        
        with self.assertRaises(ValueError):
            self.photo.clarity = 1001

    def test_sharpness_in_bound(self):
        # Test that no error is raised for in-bound sharpness
        self.photo.sharpness = -300
        self.assertEqual(self.photo.sharpness, -300)
        self.photo.sharpness = 0
        self.assertEqual(self.photo.sharpness, 0)
        self.photo.sharpness = 300
        self.assertEqual(self.photo.sharpness, 300)

    def test_sharpness_out_of_bound(self):
        # Test that an error is raised for out-of-bound sharpness
        with self.assertRaises(ValueError):
            self.photo.sharpness = -301
            
        with self.assertRaises(ValueError):
            self.photo.sharpness = 301
            
        
    def test_grain_in_bound(self):
        # Test that no error is raised for in-bound grain
        self.photo.grain = 0
        self.assertEqual(self.photo.grain, 0)
        self.photo.grain = 0.5
        self.assertEqual(self.photo.grain, 0.5)
        self.photo.grain = 1
        self.assertEqual(self.photo.grain, 1)
    
    def test_grain_out_of_bound(self):
        # Test that an error is raised for out-of-bound grain
        with self.assertRaises(ValueError):
            self.photo.grain = -0.1
            
        with self.assertRaises(ValueError):
            self.photo.grain = 1.1
    
    def test_tonal_curve_in_bound(self):
        # Test that no error is raised for in-bound tonal_curve
        self.photo.tonal_curve = 1
        self.assertEqual(self.photo.tonal_curve, 1)
    
    def test_tonal_curve_out_of_bound(self):
        # Test that an error is raised for out-of-bound tonal_curve
        with self.assertRaises(ValueError):
            self.photo.tonal_curve = 0
            
        with self.assertRaises(ValueError):
            self.photo.tonal_curve = 31
    
    def test_warmness_in_bound(self):
        # Test that no error is raised for in-bound warmness
        self.photo.warmness = 0
        self.assertEqual(self.photo.warmness, 0)
        self.photo.warmness = 5
        self.assertEqual(self.photo.warmness, 5)
        self.photo.warmness = 10
        self.assertEqual(self.photo.warmness, 10)
        
    def test_warmness_out_of_bound(self):
        # Test that an error is raised for out-of-bound warmness
        with self.assertRaises(ValueError):
            self.photo.warmness = -1
            
        with self.assertRaises(ValueError):
            self.photo.warmness = 11
    
    def test_rgb_in_bound(self):
        # Test that no error is raised for in-bound rgb
        self.photo.rgb = {'red': 1, 'green': 1, 'blue': 1}
        self.assertEqual(self.photo.rgb, {'red': 1, 'green': 1, 'blue': 1})
             
    

if __name__ == '__main__':
    unittest.main()