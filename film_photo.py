from PIL import Image, ImageFilter, ImageEnhance
import pathlib
import random

class FilmPhoto:        
    def __init__(self, input_path, clarity=0, sharpness=1, 
                grain=0, tonal_curve=1, warm=1, 
                red=1, green=1, blue=1):
        """
        constructor for FilmPhoto class
        
        Parameters
        ----------
        input_path : 
            path to the input image file
        clarity : 
            clarity factor to adjust burriness. The higher the factor, the more blurry the image
        sharpness : 
            sharpness factor to adjust sharpness. The higher the factor, the sharper the image.
        grain : 
            blending factor to adjust grain. The higher the factor, the more grainy the image
        tonal_curve : 
            tonal curve factor to adjust tonal curves. The higher the factor, the more contrast the image
        warm : 
            warmness factor to adjust color warmness of the photo. The higher the factor, the warmer it looks
        red : 
            red factor to adjust red color. The higher the factor, the more red the image
        green : 
            green factor to adjust green color. The higher the factor, the more green the image
        blue : 
            blue factor to adjust blue color. The higher the factor, the more blue the image
        """
        # Raise an error if the input path is not a valid file path
        if not pathlib.Path(input_path).is_file():
            raise ValueError(f"{input_path} is not a valid file path")
        self._initializing = True
        # Open the image and copy the data to the instance
        with Image.open(input_path) as img:
            self._original_image = img.copy()
            self._image = img.copy()
            self._width = img.width
            self._height = img.height
        self._clarity = clarity
        self._sharpness = sharpness
        self._grain = grain
        self._tonal_curve = tonal_curve
        self._warmness = warm
        self._rgb = {'red': red, 'green': green, 'blue': blue}
        self.transform()
        self._initializing = False
    
    @property
    def image(self):
        # Getter for image object
        return self._image
    
    @property
    def width(self):
        # Getter for image width
        return self._width
    
    @property
    def height(self):
        # Getter for image height
        return self._height
    
    @property
    def clarity(self):
        # Getter for clarity factor
        return self._clarity
    
    @property
    def sharpness(self):
        # Getter for sharpness factor
        return self._sharpness
    
    @property
    def grain(self):
        # Getter for grain factor
        return self._grain
    
    @property
    def tonal_curve(self):
        # Getter for tonal curve factor
        return self._tonal_curve
    
    @property
    def warmness(self):
        # Getter for warmness factor
        return self._warmness
    
    @property
    def rgb(self):
        # Getter for rgb factors
        return self._rgb
    
    @clarity.setter
    def clarity(self, factor):
        """
        Setter for clarity factor
        
        Parameters
        ----------
        factor :
            clarity factor to adjust burriness. The higher the factor, the more blurry the image
        
        Adjust clarity factor to adjust burriness. 
        Film photo tends to be more blurry than digital photo
        Bound 0 to 1000, 0 is the original image, 100 is the most blurry
        """
        FilmPhoto.validate_factor({'clarity factor': factor})
        self._image = self._image.filter(ImageFilter.GaussianBlur(radius=factor))
        self._clarity = factor
    
    @sharpness.setter
    def sharpness(self, factor):
        """
        sharpness setter
        
        Parameters
        ----------
        factor :
            sharpness factor to adjust sharpness. The higher the factor, the sharper the image.
        
        Adjust sharpness factor. 
        Factor 1.0 always returns a copy of the original image, lower factors mean less color
        (brightness, contrast, etc), and higher values more. 
        Bound -300 to 300, 1 is the original image, 300 is the most sharp, -300 is the least sharp
        """   
        FilmPhoto.validate_factor({'sharpness factor': factor})    
        enhancer = ImageEnhance.Sharpness(self._image)
        self._image = enhancer.enhance(factor)
        self._sharpness = factor
    
    @grain.setter
    def grain(self, factor):
        """
        grain setter
        
        Parameters
        ----------
        factor :
            blending factor to adjust grain. The higher the factor, the more grainy the image
        
        Adjust blending factor. 
        The presence of grain contributes to a textured and sometimes gritty appearance of a photo
        0.0 returns the original image, 1.0 returns the grain_image, and 0.5 returns a 50/50 blend of two images
        """
        FilmPhoto.validate_factor({'grain factor': factor})
        # Generate a grain image
        width, height = self._width, self._height
        # Create a new image in grayscale mode, 'L' refers to grayscale mode
        grain_image = Image.new('L', (width, height))
        # Iterate through each pixel in the image
        for x in range(width):
            for y in range(height):
                pixel = random.randint(0, 255)
                grain_image.putpixel((x, y), pixel)
        # Convert the grain image to RGB mode for compatibility in the blend function
        grain_image = grain_image.convert('RGB') 
        # Blend to images together. Adjust the blending factor as needed
        self._image = Image.blend(self._image, grain_image, factor) 
        self._grain = factor
    
    @tonal_curve.setter
    def tonal_curve(self, factor):
        """
        tonal_curve setter

        Parameters
        ----------
        factor :
            tonal curve factor to adjust tonal curves. 
            
        Adjust tonal curves factor. The higher the factor, the more contrast the image
        Darker color pixels (lower pixel values) are more sensitive to the change 
        Bound from 1 to 30, with 30 being the most contrast, 1 being original
        """
        FilmPhoto.validate_factor({'tonal curve factor': factor})
        tone_curve = lambda x: int(255 * (x / 255) ** factor) 
        self._image = self._image.point(tone_curve)
        self._tone_curve = factor
    
    @warmness.setter
    def warmness(self, factor):
        """
        warmness setter
        
        Parameters
        ----------
        factor :
            warmness factor to adjust color warmness of the photo. The higher the factor, the warmer it looks
        
        Adjust color warmness of the photo. 
        An enhancement factor of 0.0 gives a black and white photo. A factor of 1.0 gives the original photo.
        Bound 0 to 10, 0 is black and white, 1 is the original image, 10 is the most warm
        """
        FilmPhoto.validate_factor({'warmness factor': factor})
        enhancer = ImageEnhance.Color(self._image)
        self._image = enhancer.enhance(factor)
        self._warmness = factor
           
    @rgb.setter
    def rgb(self, rgb_factors):
        """
        rgb setter
        
        Parameters
        ----------
        rgb_factors :
            rgb factors to adjust three primary colors to achieve the desired vintage tone
        
        Adjust three primary colors to achieve the desired vintage tone
        Bound 0 for black, 1 for original, 5 is max
        """
        red_factor, green_factor, blue_factor = rgb_factors
        # Adjust three primary colors to achieve the desired vintage tone
        # Bound 0 for black, 1 for original, 5 is max
        if not isinstance(red_factor, str) and not isinstance(green_factor, str) and not isinstance(blue_factor, str):
            rgb_factors_dict = {
                'RGB factor': {
                    'red': red_factor, 
                    'green': green_factor, 
                    'blue': blue_factor
                }
            }
            FilmPhoto.validate_factor(factors=rgb_factors_dict)
            # Split the image into three color channels
            r, g, b = self._image.split()
            # Adjust each channel separately
            r = r.point(lambda i: i * red_factor)
            g = g.point(lambda i: i * green_factor)
            b = b.point(lambda i: i * blue_factor)
            # Merge the channels back together
            self._image = Image.merge('RGB', (r, g, b))
            self._rgb = {'red': red_factor, 'green': green_factor, 'blue': blue_factor}
            
    @staticmethod
    def validate_factor(factors, all=False):
        """
        validation checks
        
        Parameters
        ----------
        factors :
            factors to be validated
        all :
            whether to validate all factors or only the factors that are present in the factors dictionary
        """
        def validate_rgb_factor(factor, min_value, max_value):
            # Helper function to validate rgb factor
            for color, value in factor.items():
                if not isinstance(value, dict) and not isinstance(value, str):
                    if not min_value <= value <= max_value:
                        raise ValueError(f"Out of bound: {color} must be between {min_value} and {max_value}.")
                
        # Define the valid ranges for each factor
        valid_ranges = {
            'clarity factor': (0, 1000),
            'sharpness factor': (-300, 300),
            'grain factor': (0.0, 1.0),
            'tonal curve factor': (1, 30),
            'warmness factor': (0, 10),
            'RGB factor': (0, 5)
        }

        if all:
            # Validate all factors
            for factor_name, (min_value, max_value) in valid_ranges.items():
                factor = factors.get(factor_name)
                if factor_name == 'RGB factor' and factors['RGB factor']:
                    # Handle the 'RGB factor' separately
                    validate_rgb_factor(factors['RGB factor'], min_value, max_value)
                else:
                    if factor is not None and not min_value <= factor <= max_value:
                        raise ValueError(f"Out of bound: {factor_name} must be between {min_value} and {max_value}.")
        else:
            # Validate only the factors that are present in the factors dictionary
            for factor_name, factor in factors.items():
                min_value, max_value = valid_ranges.get(factor_name)
                if factor_name == 'RGB factor' and factors['RGB factor']:
                    # Handle the 'RGB factor' separately
                    validate_rgb_factor(factors['RGB factor'], min_value, max_value)
                else:
                    if not min_value <= factor <= max_value:
                        raise ValueError(f"Out of bound: {factor_name} must be between {min_value} and {max_value}.")
    
    def reset(self):
        """
        reset the image and settings to their initial state
        same as original image
        """
        self._image = self._original_image.copy()
        self._clarity = 0
        self._sharpness = 1
        self._grain = 0
        self._tonal_curve = 1
        self._warmness = 1
        self._rgb = {'red': 1, 'green': 1, 'blue': 1}
    
    def auto_transform(self):
        """
        Automatically transform the image to a film photo with default settings
        These are not meant to change as they are default settings
        """
        self.clarity = 1
        self.sharpness = 0.7
        self.grain = 0.1
        self.tonal_curve = 1.2
        self.warmness = 1.1
        self.rgb = (1, 0.95, 0.9)
        
    def transform(self, clarity=None, sharpness=None, grain=None, 
                  tonal_curve=None, warmness=None, rgb=None):        
        """
        Change the settings of the image to transform it to a film photo
        Parameters are same as the constructor
        """
        # If the arguments are None, use the instance variables
        self.clarity = clarity if clarity is not None else self._clarity
        self.sharpness = sharpness if sharpness is not None else self._sharpness
        self.grain = grain if grain is not None else self._grain
        self.tonal_curve = tonal_curve if tonal_curve is not None else self._tonal_curve
        self.warmness = warmness if warmness is not None else self._warmness
        if rgb is not None:
            self.rgb = rgb[0], rgb[1], rgb[2]
        else:
            self.rgb = self._rgb['red'], self._rgb['green'], self._rgb['blue']        
    
    def save(self, output_path):
        """
        Save the image to the output path
        """
        self._image.save(output_path)
        
    
def main():
    img_filename = "leo.jpeg"
    input_image_path = pathlib.Path(__file__).parent / img_filename
    output_filename = f"{img_filename.split('.')[0]}_film.jpeg"
    output_image_path = pathlib.Path(__file__).parent / output_filename
    image = FilmPhoto(input_image_path)
    image.auto_transform()
    #image.clarity = 2
    #image.sharpness = 0.7
    #image.grain = 0.3
    #image.tonal_curve = 1.2
    #image.warmness = 1.3
    #image.rgb = (1, 0.95, 0.9)
    #image.transform(clarity=1.5, sharpness=0.7, grain=0.1, tonal_curve=1.2, warmness=1.1, rgb=(1, 0.95, 0.9))
    #image.reset()
    image.save(output_image_path)    

if __name__ == "__main__":
    main()