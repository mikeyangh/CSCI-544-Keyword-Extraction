import struct
import os
import sys


def read_utf16_str(file, offset=-1, length=2):
    if offset >= 0:
        file.seek(offset)
    utf16_str = file.read(length)
    return utf16_str.decode('UTF-16LE')


def read_uint16(file):
    return struct.unpack('<H', file.read(2))[0]


def get_word_from_sogou_cell_dict(file_name):
    file = open(file_name, 'rb')
    file_size = os.path.getsize(file_name)
    mask = file.read(128)[4]
    if mask == 0x44:
        hz_offset = 0x2628
    elif mask == 0x45:
        hz_offset = 0x26c4
    else:
        sys.exit(-2)
    py_map = {}
    file.seek(0x1540 + 4)

    while 1:
        py_code = read_uint16(file)
        py_len = read_uint16(file)
        py_str = read_utf16_str(file, -1, py_len)

        if py_code not in py_map:
            py_map[py_code] = py_str
        if py_str == 'zuo':
            break

    file.seek(hz_offset)
    while file.tell() != file_size:
        word_count = read_uint16(file)
        pinyin_count = int(read_uint16(file) / 2)

        py_set = []
        for i in range(pinyin_count):
            py_id = read_uint16(file)
            py_set.append(py_map[py_id])
        py_str = "'".join(py_set)

        for i in range(word_count):
            word_len = read_uint16(file)
            word_str = read_utf16_str(file, -1, word_len)
            file.read(12)
            yield py_str, word_str

    file.close()


def store(records, file):
    for _, utf8str in records:
        file.write('%s 1\n' % str(utf8str))


def sort_dict_txt(dict_txt_file):
    with open(dict_txt_file, 'r') as dict_txt:
        with open(dict_txt_file + '.sorted.txt', 'w+') as dict_txt_sorted:
            line_set = set(line.strip() for line in dict_txt)
            line_set = sorted(line_set)
            dict_txt_sorted.write('\n'.join(line_set))
            dict_txt_sorted.close()
            dict_txt.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Invalid args:\n  Usage: python %s file.scel new.txt' % (sys.argv[0]))
        exit(-1)

    if os.path.isdir(sys.argv[1]):
        for fileName in os.listdir(sys.argv[1]):
            if fileName.endswith('.scel'):
                print('Processing file: ' + fileName)
                generator = get_word_from_sogou_cell_dict(sys.argv[1] + '/' + fileName)
                with open(sys.argv[2], 'a+') as file:
                    store(generator, file)
    else:
        generator = get_word_from_sogou_cell_dict(sys.argv[1])
        with open(sys.argv[2], 'w+') as file:
            store(generator, file)

    sort_dict_txt(sys.argv[2])
