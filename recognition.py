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
    templates_spec_dots = [[1, 0, 1,
                              0, 1, 0,
                              1, 0, 1],
                             [0, 1, 0,
                              1, 1, 1,
                              0, 1, 0],
                             [1, 0, 1,
                              0, 1, 0,
                              0, 0, 1],
                             [1, 0, 1,
                              0, 1, 0,
                              0, 1, 0],
                             [1, 0, 1,
                              0, 1, 0,
                              1, 0, 0],
                             [1, 0, 0,
                              0, 1, 1,
                              0, 1, 0],
                             [1, 0, 0,
                              0, 1, 1,
                              1, 0, 0],
                             [0, 1, 0,
                              0, 1, 1,
                              0, 1, 0],
                             [0, 1, 0,
                              0, 1, 1,
                              1, 0, 0],
                             [1, 0, 0,
                              0, 1, 0,
                              1, 0, 1],
                             [0, 1, 0,
                              0, 1, 1,
                              0, 1, 0],
                             [1, 0, 1,
                              0, 1, 0,
                              0, 0, 1],
                             [0, 1, 0,
                              1, 1, 1,
                              0, 0, 0]
                             ]
    def __init__(self, path_to_image):
        self.path_to_image = path_to_image
        self.path_without_ext = self.cut_ext_from_file()
        self.new_path = self.binarization()
        self.skeletization()
        self.find_special_dots()

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
        new_path = self.path_without_ext + '-bin.png'
        r.save(new_path)
        return new_path

    #True - 1 black, False - 0 White
    #Zong-Suyn alogrithm
    def skeletization(self):
        source_bin_image = Image.open(self.path_without_ext + '-bin.png')
        self.source_image_array = np.asarray(source_bin_image)
        self.source_image_array = np.invert(source_bin_image).tolist()
        replace_flag = True
        arr_width = len(self.source_image_array[0])
        arr_heigth = len(self.source_image_array)
        count_lap = 0
        while replace_flag:
            count_lap += 1
            print("Lap - {0}".format(count_lap))
            if count_lap == 8:
                print("breakpoint")
            replace_flag = False
            for i in range(1, arr_width - 1):
                for j in range(1, arr_heigth - 1):
                    if self.source_image_array[j][i]:
                        near_dots_list, total_black_count = self.calc_near_pixels(i, j)
                        if near_dots_list[1] * near_dots_list[3] * near_dots_list[5] == 0:
                            if near_dots_list[3] * near_dots_list[5] * near_dots_list[7] == 0:
                                if total_black_count in range(2, 6):
                                    if self.check_near_dots_01_sequence(i, j):
                                        self.source_image_array[j][i] = False
                                        replace_flag = True
        to_save_img = Image.new('1', (arr_width, arr_heigth))
        self.source_image_array = np.asarray(self.source_image_array)
        self.source_image_array = np.invert(self.source_image_array).tolist()
        pixels = to_save_img.load()
        for i in range(1, arr_width - 1):
            for j in range(1, arr_heigth - 1):
                pixels[i, j] = self.source_image_array[j][i]
        to_save_img.save(self.path_without_ext + '-skl.png')

    def check_near_dots_01_sequence(self, x, y):
        all_pixels, total_black_count = self.calc_near_pixels(x, y)
        all_pixels.pop(-1)
        all_pixels.append(all_pixels[0])
        sequence_count = 0
        for index in range(len(all_pixels) - 1):
            if not all_pixels[index]:
                if all_pixels[index + 1]:
                    sequence_count += 1
            if sequence_count > 1:
                return  False
        if sequence_count != 1:
            return False
        return True

    def calc_near_pixels(self, x, y):
        '''
        P9 P2 P3
        P8 P1 P4
        P7 P6 P5
        '''
        total_black_count = 0
        able_to_delete_array = []
        p1 = self.source_image_array[y][x]
        able_to_delete_array.append(p1)
        p2 = self.source_image_array[y - 1][x]
        if p2:
            total_black_count += 1
        able_to_delete_array.append(p2)
        p3 = self.source_image_array[y - 1][x + 1]
        if p3:
            total_black_count += 1
        able_to_delete_array.append(p3)
        p4 = self.source_image_array[y][x + 1]
        if p4:
            total_black_count += 1
        able_to_delete_array.append(p4)
        p5 = self.source_image_array[y + 1][x + 1]
        if p5:
            total_black_count += 1
        able_to_delete_array.append(p5)
        p6 = self.source_image_array[y + 1][x]
        if p6:
            total_black_count += 1
        able_to_delete_array.append(p6)
        p7 = self.source_image_array[y + 1][x - 1]
        if p7:
            total_black_count += 1
        able_to_delete_array.append(p7)
        p8 = self.source_image_array[y][x - 1]
        if p8:
            total_black_count += 1
        able_to_delete_array.append(p8)
        p9 = self.source_image_array[y - 1][x - 1]
        if p9:
            total_black_count += 1
        able_to_delete_array.append(p9)
        return able_to_delete_array, total_black_count


    # Find special dots
    # Here we also need to use templates to find ending of line, or other
        # special fingerprint points

    def find_special_dots(self):
        all_spec_dots = []
        curr_dot_info = []
        source_bin_image = Image.open(self.path_without_ext + '-skl.png')
        self.source_image_array = np.asarray(source_bin_image)
        self.source_image_array = np.invert(source_bin_image).tolist()
        arr_width = len(self.source_image_array[0])
        arr_heigth = len(self.source_image_array)
        for i in range(1, arr_width - 1):
            for j in range(1, arr_heigth - 1):
                current_pixel_near = self.check_pixel_near_pos(i, j)
                for template in self.templates_spec_dots:
                    if current_pixel_near == template:
                        curr_dot_info.append(i)
                        curr_dot_info.append(j)
                        curr_dot_info.append(self.templates_spec_dots.index(template))
                        all_spec_dots.append(curr_dot_info)
                        curr_dot_info = []
                        break
        self.write_all_data_to_file(all_spec_dots)
        return all_spec_dots

    def check_pixel_near_pos(self, x, y):
        arr_of_near_pixels =[]
        # Here we need to get all near pixels
        # P1 P2 P3
        # P4 x P5
        # P7 P8 P9
        arr_of_near_pixels.append(self.source_image_array[y - 1][x - 1])
        arr_of_near_pixels.append(self.source_image_array[y - 1][x])
        arr_of_near_pixels.append(self.source_image_array[y - 1][x + 1])
        arr_of_near_pixels.append(self.source_image_array[y][x - 1])
        arr_of_near_pixels.append(self.source_image_array[y][x])
        arr_of_near_pixels.append(self.source_image_array[y][x + 1])
        arr_of_near_pixels.append(self.source_image_array[y + 1][x - 1])
        arr_of_near_pixels.append(self.source_image_array[y + 1][x])
        arr_of_near_pixels.append(self.source_image_array[y + 1][x + 1])
        return arr_of_near_pixels

    def write_all_data_to_file(self, arr_of_info):
        name_of_file = self.path_without_ext[self.path_without_ext.rfind('/'):]
        f = open(self.path_without_ext + '-info.txt', "w+", encoding='utf8')
        for dot in arr_of_info:
            f.write(str(dot) + '\n')

example_path = '/home/gleb/PycharmProjects/fingerprint-recognition/fingerprint-db/ex2.png'
example_path_2 = 'C:/Users/Glathor/Desktop/421/diploma/fingerprint-db/3.jpg'
example_path_3 = 'D:/gleb/diploma/fingerprint-recognition-main/fingerprint-db' \
                 '/1.jpg'

N = Recognition(example_path_3)

