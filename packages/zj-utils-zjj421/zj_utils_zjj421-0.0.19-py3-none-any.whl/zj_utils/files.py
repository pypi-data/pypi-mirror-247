#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by zj on 2022/05/13 
# Task:
import binascii
import glob
import hashlib
import os
import re
from datetime import datetime
from PIL import Image
import fitz
# import concurrent
# import multiprocessing
# from multiprocessing import Pool, Queue
# from concurrent.futures import ProcessPoolExecutor
# from tqdm import tqdm

try:
    from .timer import MyTimer
except:
    from timer import MyTimer


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_image_md5(image_arr):
    md5_hash = hashlib.md5(image_arr.tobytes()).digest()
    md5_hash = binascii.hexlify(md5_hash).decode()
    return md5_hash


def makedirs_if_not_exists(dirname):
    dirname = os.path.abspath(dirname)
    assert not os.path.isfile(dirname), '‘{}’ 存在同名文件！'.format(dirname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def makedirs(dirname):
    return makedirs_if_not_exists(dirname)


def remove_file_path_prefix(file_path: str, prefix: str):
    if not prefix.endswith('/'):
        prefix += '/'
    return file_path.replace(prefix, '')


def delete_earlier_model(root, file_name, keeps=3, log=True):
    files = glob.glob(os.path.join(root, file_name))
    files = sorted(files, key=os.path.getctime, reverse=True)
    files_deleted = files[keeps:]
    # print([os.path.basename(x) for x in files])
    if len(files_deleted) != 0:
        if log:
            print('Deleting files in {} ...'.format(root))
        for f in files_deleted:
            os.remove(f)
            if log:
                print("File ‘{}’ have been deleted.".format(os.path.basename(f)))


def delete_0_dir(dir_root):
    """
    删除目录下的空白目录。
    :param dir_root:
    :return:
    """
    root, dirs, _ = next(os.walk(dir_root))
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        files_ = os.listdir(dir_path)
        len_ = len(files_)
        if len_ == 0:
            os.rmdir(dir_path)  # 目录为空时才可以删除，否则报错
            print("目录 '{}' 已被删除。".format(dir))
        elif len_ == 1:
            if files_[0][:7] == 'logger_' and files_[0].endswith('.log'):
                os.remove(os.path.join(dir_path, files_[0]))
                os.rmdir(dir_path)  # 目录为空时才可以删除，否则报错
                print("目录 '{}' 已被删除。".format(dir))


def get_file_path_list(dir_path, ext=None):
    """
    从给定目录中获取所有文件的路径

    :param dir_path: 路径名
    :return: 该路径下的所有文件路径(path)列表
    """
    if ext:
        patt = re.compile(r".*{}$".format(ext))

    file_path_list = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if ext:
                result = patt.search(file)
                if not result:
                    continue
            path = os.path.join(root, file)
            file_path_list.append(path)
    # print("'{}'目录中文件个数 : {}".format(os.path.basename(dir_path), len(file_path_list)))
    return file_path_list


def pdf2image(pdf_path, dpi=200, save_dir=None):
    mytimer = MyTimer()
    if save_dir:
        save_dir = os.path.join(save_dir, os.path.splitext(os.path.basename(pdf_path))[0])
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    # rotate = int(0)
    # zoom = 2
    # trans = fitz.Matrix(zoom, zoom).preRotate(rotate)
    ret = []
    with fitz.open(pdf_path) as pdf:
        for i in range(pdf.page_count):
            # pm = pdf[i].getPixmap(matrix=trans, alpha=False)
            pm = pdf[i].get_pixmap(dpi=dpi)
            if save_dir:
                image_save_path = os.path.join(save_dir, f'{i:03d}.png')
                pm.save(image_save_path)
                ret.append(image_save_path)
            else:
                pix = Image.frombytes("RGB", [pm.width, pm.height], pm.samples)
                ret.append(pix)
    mytimer.log(f'convert {pdf_path} to images time', unit='s')
    return ret


# def _page2rgb(pdf_path, page_idx, dpi=200, queue_=None, save_path=None):
#     pdf = fitz.open(pdf_path)
#     page = pdf[page_idx]
#     pix = page.get_pixmap(dpi=dpi)
#     pix = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#     if save_path:
#         makedirs(os.path.dirname(save_path))
#         pix.save(save_path)
#     if queue_ is None:
#         return page_idx, pix
#     else:
#         queue_.put((page_idx, pix))
#
#
# def pdf2image2(pdf_path, dpi=200, save_dir=None, workers=1):
#     mytimer = MyTimer()
#     if save_dir:
#         save_dir = os.path.join(save_dir, os.path.splitext(os.path.basename(pdf_path))[0])
#         if not os.path.exists(save_dir):
#             os.makedirs(save_dir)
#     # rotate = int(0)
#     # zoom = 2
#     # trans = fitz.Matrix(zoom, zoom).preRotate(rotate)
#     ret = []
#     queue_ = Queue()
#     # pool = Pool(workers)
#
#     pdf = fitz.open(pdf_path)
#     pages = [pdf[i] for i in range(len(pdf))]
#     with ProcessPoolExecutor(max_workers=workers) as executor:
#         future_to_page = {executor.submit(_page2rgb, pdf_path, i, dpi, None, os.path.join(save_dir, f'{i:03d}.png')): i
#                           for i in
#                           range(len(pages))}
#         # 获取已完成任务的结果
#         for future in concurrent.futures.as_completed(future_to_page):
#             page_number = future_to_page[future]
#             try:
#                 # page_idx, pix = future.result()
#                 ret.append(future.result())
#                 print(f"Page {page_number} result save to ret")
#             except Exception as e:
#                 print(f"Error processing page {page_number}: {e}")
#
#     mytimer.log(f'convert {pdf_path} to images time', unit='s')
#     return ret


def main():
    pass


if __name__ == '__main__':
    start = datetime.now()
    print("Start time is {}".format(start))
    main()
    end = datetime.now()
    print("End time is {}".format(end))
    print("\nTotal running time is {}s".format((end - start).seconds))
    print("\nCongratulations!!!")
