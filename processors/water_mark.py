import os
from PIL import Image


class WaterMarker():
    """
    :var percentage: percentage of the base_img's width will be covered by water marker img
    """
    marker_img = 'static/main_app/img/logo-transparent.png'
    
    percentage = 0.2
    
    def __init__(self, base_img=None, marker_img=None):
        """
        :param base_img: uploaded image, water_marker image will be placed onto this
        :param marker_img: transparent water marker, which will be placed
        """
        self.base_img = base_img
        
        if marker_img:
            self.marker_img = marker_img
        
        if not self.is_img_exists():
            ##
            ##### post should be unpublished or some actions should be taken HERE.....
            ##
            print('Some image is not found')
    
    def is_img_exists(self):
        return os.path.isfile(self.base_img) and os.path.isfile(self.marker_img)
    
    def resized_img(self):
        """
        resizing water-marker image before placing..
        a percentage of the base_img's width will be covered by water marker img
        :var marker: water_marker image object
        :var base: base image object
        :var aspect_ratio: aspect_ratio of water_marker image
        :var new_height: resized height of water mark
        :var new_width: resized width of water mark
        """
        marker = Image.open(self.marker_img, 'r')
        base = Image.open(self.base_img, 'r')
        
        new_width = self.percentage * base.width
        new_height = new_width * (marker.height / marker.width)
        
        temp_dir = 'media/temp'
        temp_file_path = os.path.join(temp_dir, 'marker.png')
        
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # resizing image
        marker.thumbnail(size=(new_width, new_height))
        
        # saving the resized image in temp directory
        marker.save(temp_file_path)
        
        marker.close()
        base.close()
        
        # returning the temporary file name
        return temp_file_path
    
    def water_mark(self):
        base_img = Image.open(self.base_img, 'r')
        marker_img = Image.open(self.resized_img(), 'r')  # resized image based on base image
        
        # setting position on the bottle right corner
        set_pos = (base_img.width-marker_img.width, base_img.height-marker_img.height)
        
        new_base_img = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
        
        new_base_img.paste(base_img, (0, 0))
        new_base_img.paste(marker_img, set_pos, mask=marker_img)
        
        new_base_img.save(self.base_img, format="png")
        
        new_base_img.close()
        base_img.close()

