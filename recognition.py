from PIL import Image
import numpy as np
import pickle
import math

class Recognition:
    # for skeletization
    # template array for the value of the neighborhood estimate
    h = [[128, 64, 32],
         [16, 0, 8],
         [4, 2, 1]]
    current_count_of_fingerprints = 9
    maximum_fault_percent = 60
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

    templates_spec_dots_4 = [[1, 0, 1,
                              0, 1, 0,
                              1, 0, 1],
                             [0, 1, 0,
                              1, 1, 1,
                              0, 1, 0]]
    templates_spec_dots_3 = [[1, 0, 1,
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
                             [1, 0, 1,
                              0, 1, 0,
                              0, 0, 1],
                             [0, 1, 0,
                              1, 1, 1,
                              0, 0, 0],
                             [0, 0, 1,
                              0, 1, 0,
                              1, 0, 1],
                             [0, 0, 1,
                              1, 1, 0,
                              0, 0, 1],
                             [0, 0, 0,
                              1, 1, 1,
                              0, 1, 0],
                             [0, 1, 0,
                              1, 1, 0,
                              0, 1, 0],
                             ]
    templates_spec_dots_2 = [[1, 0, 0,
                              0, 1, 0,
                              0, 0, 0],
                             [0, 1, 0,
                              0, 1, 0,
                              0, 0, 0],
                             [0, 0, 1,
                              0, 1, 0,
                              0, 0, 0],
                             [0, 0, 0,
                              0, 1, 1,
                              0, 0, 0],
                             [0, 0, 0,
                              0, 1, 0,
                              0, 0, 1],
                             [0, 0, 0,
                              0, 1, 0,
                              0, 1, 0],
                             [0, 0, 0,
                              0, 1, 0,
                              1, 0, 0]]

    def __init__(self, path_to_image):
        self.path_to_image = path_to_image
        self.path_without_ext = self.cut_ext_from_file()
        self.binarization()
        self.skeletization()
        self.find_special_dots()
        self.new_path = self.path_without_ext + '-colored.png'
        self.result = self.compare_with_db()
        self.final_recon_path = self.path_without_ext[:-1] + self.result[-1] \
                                + '.jpg'


    def cut_ext_from_file(self):
        path_img = str(self.path_to_image)
        right_dot = path_img.rfind('.')
        return path_img[:right_dot]

    # 0 - is black, 240-255 - white
    def binarization(self):
        source_image = Image.open(self.path_to_image)
        thresh = 150 # this is our coef. of binarizing
        print("*** Binarization process started ***")
        fn = lambda x : 255 if x > thresh else 0
        r = source_image.convert('L').point(fn, mode='1')
        new_path = self.path_without_ext + '-bin.png'
        r.save(new_path)
        return new_path

    # Roshenfeld template algorithm
    def skeletization_2(self):
        source_bin_image = Image.open(self.path_without_ext + '-bin.png')
        self.source_image_array = np.asarray(source_bin_image)
        self.source_image_array = np.invert(source_bin_image).tolist()
        replace_flag = True
        arr_width = len(self.source_image_array[0])
        arr_heigth = len(self.source_image_array)
        count_lap = 0
        print("*** Skeletization process started ***")
        while replace_flag:
            replace_flag = False
            count_lap += 1
            print("Lap - {0}".format(count_lap))
            for i in range(1, arr_width - 1):
                for j in range(1, arr_heigth - 1):
                    if self.source_image_array[j][i]:
                        if self.calc_value_of_near_pixels_and_make_decision(i, j):
                            replace_flag = True
        to_save_img = Image.new('1', (arr_width, arr_heigth))
        self.source_image_array = np.asarray(self.source_image_array)
        self.source_image_array = np.invert(self.source_image_array).tolist()
        pixels = to_save_img.load()
        for i in range(1, arr_width - 1):
            for j in range(1, arr_heigth - 1):
                pixels[i, j] = self.source_image_array[j][i]
        to_save_img.save(self.path_without_ext + '-skl.png')

    # True - 1 black, False - 0 White
    # Zhang - Suen algorithm
    def skeletization(self):
        source_bin_image = Image.open(self.path_without_ext + '-bin.png')
        self.source_image_array = np.asarray(source_bin_image)
        self.source_image_array = np.invert(source_bin_image).tolist()
        replace_flag = True
        arr_width = len(self.source_image_array[0])
        arr_heigth = len(self.source_image_array)
        count_lap = 0
        print("*** Skeletization process started ***")
        while replace_flag:
            count_lap += 1
            print("Lap - {0}".format(count_lap))
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
                        if self.check_for_noise_spec_dots(near_dots_list):
                            self.source_image_array[j][i] = False
        to_save_img = Image.new('1', (arr_width, arr_heigth))
        self.source_image_array = np.asarray(self.source_image_array)
        self.source_image_array = np.invert(self.source_image_array).tolist()
        pixels = to_save_img.load()
        for i in range(1, arr_width - 1):
            for j in range(1, arr_heigth - 1):
                pixels[i, j] = self.source_image_array[j][i]
        to_save_img.save(self.path_without_ext + '-skl.png')

    def delete_noise_from_skelet_image(self):
        arr_width = len(self.source_image_array[0])
        arr_heigth = len(self.source_image_array)
        count_lap = 0
        replace_flag = True
        print("*** Skeletization process started ***")
        while replace_flag:
            count_lap += 1
            print("Lap - {0}".format(count_lap))
            replace_flag = False
            for i in range(1, arr_width - 1):
                for j in range(1, arr_heigth - 1):
                    if self.source_image_array[j][i]:
                        continue

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

    def calc_value_of_near_pixels_and_make_decision(self, x, y):
        '''
        P1 P2 P3
        P4 P9 P5
        P8 P7 P6
        '''
        total_value_count = 0
        able_to_delete_array = []
        p1 = self.source_image_array[y - 1][x - 1]
        able_to_delete_array.append(p1)
        if p1:
            total_value_count += 128
        p2 = self.source_image_array[y - 1][x]
        if p2:
            total_value_count += 64
        able_to_delete_array.append(p2)
        p3 = self.source_image_array[y - 1][x + 1]
        if p3:
            total_value_count += 32
        able_to_delete_array.append(p3)
        p4 = self.source_image_array[y][x - 1]
        if p4:
            total_value_count += 16
        able_to_delete_array.append(p4)
        p5 = self.source_image_array[y][x + 1]
        if p5:
            total_value_count += 8
        able_to_delete_array.append(p5)
        p6 = self.source_image_array[y + 1][x - 1]
        if p6:
            total_value_count += 4
        able_to_delete_array.append(p6)
        p7 = self.source_image_array[y + 1][x]
        if p7:
            total_value_count += 2
        able_to_delete_array.append(p7)
        p8 = self.source_image_array[y + 1][x + 1]
        if p8:
            total_value_count += 1
        able_to_delete_array.append(p8)
        p9 = self.source_image_array[y][x]
        able_to_delete_array.append(p9)
        action_to_do = self.array_table_of_rules[total_value_count]
        if action_to_do == 0:
            self.source_image_array[y][x] = False
            return True
        elif action_to_do == 1:
            self.source_image_array[y - 1][x - 1] = True
        elif action_to_do == 2:
            self.source_image_array[y - 1][x] = True
        elif action_to_do == 3:
            self.source_image_array[y - 1][x + 1] = True
        elif action_to_do == 4:
            self.source_image_array[y][x - 1] = True
        elif action_to_do == 5:
            self.source_image_array[y][x + 1] = True
        self.source_image_array[y][x] = False
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
        point_spec = 0
        all_spec_dots = []
        curr_dot_info = []
        source_bin_image = Image.open(self.path_without_ext + '-skl.png')
        self.source_image_array = np.invert(source_bin_image).tolist()
        colored_image_array = np.copy(self.source_image_array)
        colored_image_array = np.invert(colored_image_array).tolist()
        arr_width = len(self.source_image_array[0])
        arr_heigth = len(self.source_image_array)
        print("*** Find special dots process started ***")
        for i in range(1, arr_width - 1):
            for j in range(1, arr_heigth - 1):
                current_pixel_near = self.check_pixel_near_pos(i, j)
                if current_pixel_near in self.templates_spec_dots_4:
                    point_spec = 4
                    colored_image_array[j][i] = (0, 0, 255)
                elif current_pixel_near in self.templates_spec_dots_3:
                    if self.check_for_false_spec_dots(i, j, current_pixel_near):
                        point_spec = 3
                        colored_image_array[j][i] = (255, 0, 0)
                    else:
                        continue
                elif current_pixel_near in self.templates_spec_dots_2:
                    point_spec = 2
                    colored_image_array[j][i] = (0, 255, 0)
                if point_spec != 0:
                    for index_i in range(i - 2,i + 2):
                        for index_j in range(j - 2, j + 2):
                            colored_image_array[index_j][index_i] = \
                                colored_image_array[j][i]
                    curr_dot_info.append(float(i / arr_width))
                    curr_dot_info.append(float(j / arr_heigth))
                    curr_dot_info.append(point_spec)
                    all_spec_dots.append(curr_dot_info)
                    curr_dot_info = []
                    point_spec = 0
        self.write_all_data_to_file(all_spec_dots)
        to_save_image = Image.new('RGB', (arr_width, arr_heigth))
        pixels = to_save_image.load()
        for i in range(2, arr_width - 1):
            for j in range(2, arr_heigth - 1):
                if type(colored_image_array) is bool:
                    if colored_image_array:
                        pixels[i, j] = (0, 0, 0)
                    else:
                        pixels[i, j] = (255, 255, 255)
                else:
                    pixels[i, j] = colored_image_array[j][i]
        to_save_image.save(self.path_without_ext + '-colored.png')
        print("*** All special dots was found ***")
        return all_spec_dots


    def check_for_noise_spec_dots(self, all_near_dots):
        noise_template = [[1, 1, 1, 1, 0, 1, 1, 1, 1],
                          [1, 1, 1, 1, 0, 1, 1, 0, 0],
                          [1, 1, 1, 0, 0, 1, 0, 1, 1],
                          [0, 0, 1, 1, 0, 1, 1, 1, 1],
                          [1, 1, 0, 1, 0, 0, 1, 1, 1],

                          [1, 1, 1, 1, 0, 1, 0, 0, 1],
                          [0, 1, 1, 0, 0, 1, 1, 1, 1],
                          [1, 0, 0, 1, 0, 1, 1, 1, 1],
                          [1, 1, 1, 1, 0, 0, 1, 1, 0],

                          [1, 1, 1, 1, 0, 1, 0, 0, 0],
                          [0, 1, 1, 0, 0, 1, 0, 1, 1],
                          [0, 0, 0, 1, 0, 1, 1, 1, 1],
                          [1, 1, 0, 1, 0, 0, 1, 1, 0]]

        all_near_dots = np.invert(np.array(all_near_dots)).tolist()
        if all_near_dots in noise_template:
            return True
        return False

    def check_for_false_spec_dots(self, x, y, near_dots):
        for i in range(len(near_dots)):
            if near_dots[i]:
                if i == 0:
                    if self.source_image_array[y - 2][x - 2] or \
                        self.source_image_array[y - 2][x - 1] or \
                            self.source_image_array[y - 1][x - 2]:
                        return True
                    else:
                        self.source_image_array[y - 1][x - 1] = False
                elif i == 1:
                    if self.source_image_array[y - 2][x - 1] or \
                        self.source_image_array[y - 2][x] or \
                            self.source_image_array[y - 2][x + 1]:
                        return True
                    else:
                        self.source_image_array[y - 1][x] = False
                elif i == 2:
                    if self.source_image_array[y - 2][x + 1] or \
                        self.source_image_array[y - 2][x + 2] or \
                            self.source_image_array[y - 1][x + 2]:
                        return True
                    else:
                        self.source_image_array[y - 1][x + 1] = False
                elif i == 3:
                    if self.source_image_array[y - 1][x - 2] or \
                        self.source_image_array[y - 2][x] or \
                            self.source_image_array[y + 1][x - 2]:
                        return True
                    else:
                        self.source_image_array[y][x - 1] = False
                elif i == 5:
                    if self.source_image_array[y - 1][x + 2] or \
                        self.source_image_array[y][x + 2] or \
                            self.source_image_array[y + 1][x + 2]:
                        return True
                    else:
                        self.source_image_array[y][x + 1] = False
                elif i == 6:
                    if self.source_image_array[y + 1][x - 2] or \
                            self.source_image_array[y - 2][x - 2] or \
                            self.source_image_array[y - 2][x + 1]:
                        return True
                    else:
                        self.source_image_array[y - 1][x - 1] = False
                elif i == 7:
                    if self.source_image_array[y - 2][x - 1] or \
                            self.source_image_array[y - 2][x] or \
                            self.source_image_array[y - 2][x + 1]:
                        return True
                    else:
                        self.source_image_array[y + 1][x] = False
                elif i == 8:
                    if self.source_image_array[y + 1][x + 2] or \
                            self.source_image_array[y + 2][x + 1] or \
                            self.source_image_array[y + 2][x + 2]:
                        return True
                    else:
                        self.source_image_array[y + 1][x + 1] = False
                return False

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
        f = open(self.path_without_ext + '-info.txt', "wb")
        pickle.dump(arr_of_info, f)

    def compare_with_db(self):
        path_to_fingerprint_info = self.path_without_ext + '-info.txt'
        all_files_db = []
        for i in range(1, self.current_count_of_fingerprints):
            if i == int(self.path_without_ext[-1]):
                continue
            path_to_file = self.path_without_ext[:-1] + str(i) + '-info.txt'
            with open(path_to_file, 'rb') as fp:
                item_list = pickle.load(fp)
                all_files_db.append(item_list)
        with open(path_to_fingerprint_info, 'rb') as fp:
            curr_fingerprint = pickle.load(fp)
        max_math_percent = 0
        index_of_max_match = 0
        all_compare_percent = []
        for fp in all_files_db:
            count_of_true_dots = 0
            marked_dots_of_curr_arr = []
            marked_dots_of_another = []
            total_dots_count = min(len(fp), len(curr_fingerprint))
            for dot in fp:
                if dot not in marked_dots_of_another:
                    for curr_dot in curr_fingerprint:
                        if curr_dot not in marked_dots_of_curr_arr:
                            if abs(dot[0] - curr_dot[0]) <= 0.0016 and \
                                    abs(dot[1] - curr_dot[1]) <= 0.0016:
                                marked_dots_of_another.append(dot)
                                marked_dots_of_curr_arr.append(curr_dot)
                                count_of_true_dots += 1
            percent = float(count_of_true_dots / total_dots_count) * 100
            all_compare_percent.append(percent)
        max_percent = max(all_compare_percent)
        index_of_max_percent = all_compare_percent.index(max_percent) + 1
        print("Recognition algorithm finished")
        print("Curr - {}".format(self.path_without_ext))
        print("Highest percent of matching - {}".format(max_percent))
        if max_percent >= 55:
            return "This is the fingerprint with number - " \
                       "{}".format(index_of_max_percent)
        return "Sorry, we didn't match anything :("

# Another method of fingerprint recognition algorithms


class RecognitionCompareMethod:
    def __init__(self, path_to_image, count):
        self.path_to_image = path_to_image
        self.path_without_ext = self.cut_ext_from_file(path_to_image)
        self.binarization(path_to_image)
        self.index_of_recon_image = self.compare_fingerprints(count,
                                                  self.path_without_ext +
                                       '-bin.png')

    def cut_ext_from_file(self, path_to_file):
        path_img = str(path_to_file)
        right_dot = path_img.rfind('.')
        return path_img[:right_dot]

    def binarization(self, path_to_file):
        source_image = Image.open(path_to_file)
        thresh = 150 # this is our coef. of binarizing
        print("*** Binarization process started ***")
        fn = lambda x: 255 if x > thresh else 0
        r = source_image.convert('L').point(fn, mode='1')
        new_path = self.cut_ext_from_file(path_to_file) + '-bin.png'
        r.save(new_path)
        return new_path

    def compare_fingerprints(self, count, path_to_source_file):
        source_bin_image = Image.open(path_to_source_file)
        self.source_image_array = np.asarray(source_bin_image)
        self.source_image_array = np.invert(source_bin_image).tolist()
        arr_width = len(self.source_image_array[0])
        arr_heigth = len(self.source_image_array)
        array_of_percents = []
        for i in range(1, count + 1):
            if i == int(self.path_without_ext[-1]):
                continue
            matched_pixels = 0
            path_to_new_image = self.path_without_ext[:-1] + str(i) + '-bin.png'
            to_compare_image = Image.open(path_to_new_image)
            to_compare_image = to_compare_image.resize((arr_width,
                                                        arr_heigth),
                                                       Image.ANTIALIAS)
            to_compare_image = np.asarray(to_compare_image)
            to_compare_image = np.invert(to_compare_image).tolist()
            for ind_x in range(arr_width):
                for ind_y in range(arr_heigth):
                    if self.source_image_array[ind_y][ind_x] == \
                            to_compare_image[ind_y][ind_x]:
                        matched_pixels += 1
            matched_pixels_percent = matched_pixels / (arr_heigth *
                                                       arr_width) * 100
            print("Image {0} with percent of match - {1}".format(i, matched_pixels_percent))
            array_of_percents.append(matched_pixels_percent)
        max_percent_of_matching = max(array_of_percents)
        if max_percent_of_matching >= 80:
            print("We find it! With {0}% match image with id {1}".format(
                    max_percent_of_matching,
                    array_of_percents.index(max_percent_of_matching) + 1))
            return array_of_percents.index(max_percent_of_matching) + 1
        return False

def add_all_fingerprints(count, path_to_one_file):
    for i in range(1, count + 1):
        print("*** i = {0} ***".format(i))
        path_to_one_file = path_to_one_file[:-5] + str(i) + '.jpg'
        Recognition(path_to_one_file)


example_path = '/home/gleb/PycharmProjects/fingerprint-recognition/' \
               'fingerprint-db/ex2.png'
example_path_2 = 'C:/Users/Glathor/Desktop/421/diploma/fingerprint-db/3.jpg'
example_path_3 = 'D:/gleb/diploma/fingerprint-recognition-main/fingerprint-db' \
                 '/8.jpg'
example_path_4 = "C:/Users/Student/Desktop/fingerprint-recognition" \
                 "/fingerprint-db/6.jpg"


# N = Recognition(example_path_3)
# add_all_fingerprints(10, example_path_3)

# exm = RecognitionCompareMethod(example_path_3, 10)
