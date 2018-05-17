from PIL import Image
import numpy as np


class Recognition:

    # for skeletization
    # template array for the value of the neighborhood estimate

    h = [[128, 64, 32],
        [16, 0, 8],
        [4, 2, 1]]

    array_table_of_rules = [1, 0, 0, 3, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1,
                            0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1,
                            0, 5, 0, 0, 0, 0, 0, 5, 1, 1, 0, 3, 1, 1, 1, 1,
                            0, 0, 0, 0, 2, 5, 2, 0, 0, 0, 0, 0, 1, 1, 0, 0,
                            4, 0, 0, 0, 0, 0, 0, 0, 1, 1, 4, 3, 1, 1, 1, 1,
                            1, 5, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
                            1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 4, 0, 1, 1, 0, 1,
                            1, 5, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
                            3, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 2, 4, 4,
                            1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1,
                            2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 2, 0, 0,
                            0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0,
                            1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 4, 0, 1, 0, 1, 0,
                            1, 5, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0,
                            1, 5, 0, 0, 0, 0, 0, 0, 1, 1, 4, 0, 1, 1, 0, 0,
                            1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0]

    def __init__(self, path_to_image):
        self.path_to_image = path_to_image
        self.path_without_ext = self.cut_ext_from_file()
        self.new_path = self.binarization()
        self.skeletization()

    def cut_ext_from_file(self):
        path_img = str(self.path_to_image)
        right_dot = path_img.rfind('.')
        return path_img[:right_dot]

    # 0 - is black, 240-255 - white
    def binarization(self):
        source_image = Image.open(self.path_to_image)
        thresh = 200 # this is our coef. of binarizing
        fn = lambda x : 255 if x > thresh else 0
        r = source_image.convert('L').point(fn, mode='1')
        new_path = self.path_without_ext + '-bin.jpg'
        r.save(new_path)
        return new_path

    def skeletization(self):
        source_bin_image = Image.open(self.path_without_ext + '-bin.jpg')
        source_image_array = np.asarray(source_bin_image).tolist()
        replace_flag = True
        while replace_flag:
            replace_flag = False
            for line in source_image_array:
                for element in line:
                    if element <= 100:
                        index_x = line.index(element)
                        index_y = source_image_array.index(line)
                        index_full = [index_x, index_y]
                        total_value = self.count_value_of_near_pixels(source_image_array, index_full)
                        if total_value != 256:
                            position_to_move = self.array_table_of_rules[total_value]
                            if self.replace_pixel(source_image_array, index_full, position_to_move):
                                replace_flag = True

    def count_value_of_near_pixels(self, source_image_array, index_of_element):
        if index_of_element[0] == 0 or index_of_element[1] == 0 or index_of_element[0] == len(source_image_array[0]) \
                or index_of_element[1] == len(source_image_array):
            return 256
        total_value = 0
        # there are 9 near pixels, which we need to check
        if source_image_array[index_of_element[1] - 1][index_of_element[0] - 1] <= 100:
            total_value += 128
        if source_image_array[index_of_element[1] - 1][index_of_element[0]] <= 100:
            total_value += 64
        if source_image_array[index_of_element[1]][index_of_element[0] + 1] <= 100:
            total_value += 32
        if source_image_array[index_of_element[1]][index_of_element[0] - 1] <= 100:
            total_value += 16
        if source_image_array[index_of_element[1]][index_of_element[0] + 1] <= 100:
            total_value += 8
        if source_image_array[index_of_element[1] + 1][index_of_element[0] - 1] <= 100:
            total_value += 4
        if source_image_array[index_of_element[1] + 1][index_of_element[0]] <= 100:
            total_value += 2
        if source_image_array[index_of_element[1] + 1][index_of_element[0] + 1] <= 100:
            total_value += 1
        return total_value

    def replace_pixel(self, source_image_array, index_of_element, position_to_move):
        if position_to_move == 1:
            source_image_array[index_of_element[1] - 1][index_of_element[0] - 1] = 0
        if position_to_move == 2:
            source_image_array[index_of_element[1] - 1][index_of_element[0]] = 0
        if position_to_move == 3:
            source_image_array[index_of_element[1] - 1][index_of_element[0] + 1] = 0
        if position_to_move == 4:
            source_image_array[index_of_element[1]][index_of_element[0] + 1] = 0
        if position_to_move == 5:
            source_image_array[index_of_element[1] + 1][index_of_element[0] + 1] = 0
        source_image_array[index_of_element[1]][index_of_element[0]] = 255
        return True


example_path = '/home/gleb/PycharmProjects/fingerprint-recognition/fingerprint-db/example.jpg'
N = Recognition(example_path)
print(N.array_table_of_rules[182])