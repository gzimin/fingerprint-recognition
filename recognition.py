from PIL import Image

class Recognition:

    def __init__(self, path_to_image):
        self.path_to_image = path_to_image
        self.new_path = self.binarization()

    def binarization(self):
        source_image = Image.open(self.path_to_image)
        thresh = 200 # this is our coef. of binarizing
        fn = lambda x : 255 if x > thresh else 0
        r = source_image.convert('L').point(fn, mode='1')
        path_img = str(self.path_to_image)
        right_dot = path_img.rfind('.')
        path_without_ext = path_img[:right_dot]
        new_path = path_without_ext + '-bin.jpg'
        r.save(new_path)
        return new_path
