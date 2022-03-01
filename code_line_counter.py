# -*- encoding: utf-8 -*-

"""
------------------------------------------
@File       : code_line_counter.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2022/3/1 16:18
------------------------------------------
"""

from os import listdir
from os.path import isdir, splitext, join as path_join


def list_paths(dir_path: str, depth: int = 0, suffix=None, key_str: str = None):
    """
    1) Generator。
    2) 遍历 dir_path 目录下的文件的路径。
    3) 注意：这里的路径使用'/'。
    :param dir_path:    str     要遍历的目录路径
    :param depth:       int     扫描的深度 0:当前目录，1：当前目录的下一级目录
    :param suffix:      str     返回的路径中包含特定后缀，如 ".py" 或者 "py"，默认None，没有后缀限制
    :param key_str:     str     返回的路径中包含特定的关键词
    """

    # 设定当前目录的表示值
    current_dir_level = 0

    if suffix:
        if not suffix.startswith('.'):
            suffix = '.' + suffix

    for _path in listdir(dir_path):
        tmp_path = path_join(dir_path, _path)

        if isdir(tmp_path):
            if current_dir_level < depth:
                yield from list_paths(tmp_path, depth - 1, suffix, key_str)

        else:
            found = []
            if suffix:
                if splitext(tmp_path)[-1] == suffix:
                    found.append(True)
                else:
                    found.append(False)

            if key_str:
                if key_str in tmp_path:
                    found.append(True)
                else:
                    found.append(False)

            if all(found):
                yield tmp_path


def line_count(file_path, include_blank_line=True) -> int:
    """
        计算单个文件中有多少行内容
        :param file_path:           文件路径
        :param include_blank_line:  计算中是否包含空行，默认包含
    """

    with open(file_path, 'r', encoding='utf8') as f:
        content = f.readlines()

        if include_blank_line:
            return len(content)

        content2 = [x for x in content if len(x.strip()) != 0]
        return len(content2)


def worker(root_dir: str, include_blank_line: bool = True):
    """
        root_dir:               项目根目录
        include_blank_line:     将空行统计在内，默认包括
    """
    depth = 10  # 目录深度
    suffix = ".py"  # 搜索后缀为".py"的文件

    res = list_paths(root_dir, depth=depth, suffix=suffix)
    result = []
    for i in res:
        result.append([i, line_count(i)])

    # 按照内容行数从大到小排序
    sorted(result, key=lambda x: x[-1], reverse=True)

    line_counter = 0
    for no, item in enumerate(result, 1):
        content = f"[ NO.{no} ] [ {item[0]} ] [ {item[-1]} ]"
        line_counter += item[-1]
        print(content)

    print(f"\nFiles: {len(result)} | lines: {line_counter}")


def main():
    root_dir = r'E:\Code\localCode\ETL'
    worker(root_dir)


if __name__ == "__main__":
    main()
