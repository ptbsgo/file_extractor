# -*- coding: utf-8 -*-
# @Time    : 2023/10/18 13:13
# @Author  : ptbs
# @File    : file_extractor.py.py
# @Software: PyCharm
# ---------CODE-------------
import os
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor

src_dir = r'D:\360安全浏览器下载\Automated_bounty_Hunter\相关软件\nuclei-templates\Nuclei-Templates-Collection-main\Nuclei-Templates-Collection-main\community-templates\community-templates'
dst_dir = r'D:\360安全浏览器下载\Automated_bounty_Hunter\相关软件\nuclei-templates\Nuclei-Templates-Collection-main\Nuclei-Templates-Collection-main\community-templates\nuclei-templates'

overwrite = False
exclude = ['temp', 'tmp.txt']

extracted_count = 0
skipped_count = 0


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='extract.log',
                    level=logging.INFO)

exts = input('请输入要提取的扩展名,用英文逗号隔开: ')
ext_list = exts.split(',')


def copy_file(src_path):
    global extracted_count
    global skipped_count
    dst_path = os.path.join(dst_dir, os.path.relpath(src_path, src_dir))
    if os.path.exists(dst_path) and not overwrite:
        logging.info('%s已存在,跳过', dst_path)
        skipped_count += 1
        return

    dst_folder = os.path.dirname(dst_path)
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    shutil.copy2(src_path, dst_path)
    extracted_count += 1


def get_files(dir, ext_list):
    res = []
    for root, dirs, files in os.walk(dir):
        for f in files:
            if f in exclude:
                continue
            if os.path.splitext(f)[-1] in ext_list:
                res.append(os.path.join(root, f))
    return res


files = get_files(src_dir, ext_list)
logging.info('找到%s个文件', len(files))

with ThreadPoolExecutor() as executor:
    executor.map(copy_file, files)

print(f'总共提取了{extracted_count}个文件')
print(f'跳过了{skipped_count}个已存在的文件')