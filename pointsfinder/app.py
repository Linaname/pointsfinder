#! /usr/bin/env python

import argparse


class PointSet:

    def __init__(self, text_data):
        lines = text_data.splitlines()
        self.points = list(map(self._parse_line, lines))
        self._sorted_by_x = sorted(self.points, key=lambda point: point[0])
        self._sorted_by_y = sorted(self.points, key=lambda point: point[1])

    @staticmethod
    def _parse_line(line):
        x, y, tag = line.split(' ', 3)
        return float(x), float(y), tag

    @staticmethod
    def _are_near(x1, y1, x2, y2, r):
        return (x1 - x2)**2 + (y1 - y2)**2 <= r**2

    @staticmethod
    def _min_index_of_higher_element(sorted_list, value, key):
        left = -1
        right = len(sorted_list)
        while left + 1 < right:
            mid = (left + right)//2
            if key(sorted_list[mid]) <= value:
                left = mid
            else:
                right = mid
        return right

    @staticmethod
    def _max_index_of_lower_element(sorted_list, value, key):
        left = -1
        right = len(sorted_list)
        while left + 1 < right:
            mid = (left + right)//2
            if key(sorted_list[mid]) < value:
                left = mid
            else:
                right = mid
        return left

    def find_neighbors_tags(self, center_x, center_y, r):
        right = self._min_index_of_higher_element(self._sorted_by_x, center_x + r, lambda point: point[0])
        left = self._max_index_of_lower_element(self._sorted_by_x, center_x - r, lambda point: point[0])
        top = self._min_index_of_higher_element(self._sorted_by_y, center_y + r, lambda point: point[1])
        bottom = self._max_index_of_lower_element(self._sorted_by_y, center_y - r, lambda point: point[1])
        suitable_points_by_x = self._sorted_by_x[left + 1:right]
        suitable_points_by_y = self._sorted_by_y[bottom + 1:top]
        suitable_points = set(suitable_points_by_x) & set(suitable_points_by_y)
        tags = []
        for point in suitable_points:
            x, y, tag = point
            if self._are_near(center_x, center_y, x, y, r):
                tags.append(tag)
        return sorted(tags)

    def run_io_loop(self):
        while True:
            user_input = input()
            if user_input == 'exit':
                break
            try:
                x, y, r = map(float, user_input.split())
            except ValueError:
                print('Input is incorrect')
                continue
            neighbors_tags = self.find_neighbors_tags(x, y, r)
            output_string = ', '.join(neighbors_tags)
            print(output_string)


def read_file(path):
    with open(path) as file:
        text_data = file.read()
    return PointSet(text_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to file')
    args = parser.parse_args()
    path = args.path
    try:
        pointset = read_file(path)
    except FileNotFoundError:
        exit("File '{}' not found".format(path))
    except IsADirectoryError:
        exit("'{}' is a directory".format(path))
    except ValueError:
        exit('File is incorrect')
    pointset.run_io_loop()
