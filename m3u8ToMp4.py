import os
from pathlib import Path
import os.path as osp
import argparse
import shutil
import locale
from subprocess import Popen, PIPE

def get_shufix_files(file_list, shufix:list):
    return filter(lambda x: os.path.splitext(x)[-1] in shufix, file_list)

def fix_m3u8(m3u8_path:str, content_dir_root:str):
    # content_dir_root = osp.abspath(osp.dirname(src_path)) 
    m3u8_file_name = osp.basename(m3u8_path)
    lines = [str]
    with open(m3u8_path, 'r') as f:
        lines = f.readlines()
    for index, line in enumerate(lines):
        found_start_idx = line.find("file://")
        found_end_idx = line.find(m3u8_file_name)
        if found_start_idx != -1 and found_end_idx != -1:
            lines[index] = line.replace(line[found_start_idx:found_end_idx - 1], content_dir_root)
    if not osp.exists(m3u8_path + ".bak"):
        shutil.move(m3u8_path, m3u8_path + ".bak")
    fixed_path = m3u8_path.replace(' ', '_')
    fixed_path = fixed_path.replace('(', '')
    fixed_path = fixed_path.replace(')', '')
    with open(fixed_path, 'w+') as f:
        f.writelines(lines)
    return fixed_path

def restore_m3u8_files(root_dir):
    file_list = os.listdir(root_dir)
    m3u8_list = get_shufix_files(file_list, [".m3u8"])
    for m3u8_name in m3u8_list:
        os.remove(osp.join(root_dir, m3u8_name))

    org_m3u8_list = get_shufix_files(file_list, [".bak"])
    for org_m3u8 in org_m3u8_list:
        org_m3u8_path = osp.join(root_dir, org_m3u8)
        org_m3u8_name = org_m3u8[:-4]
        shutil.move(org_m3u8_path, osp.join(root_dir, org_m3u8_name))

def m3u8_to_mp4(m3u8_path, out_dir, is_encode_audio=False):
    file_name = os.path.splitext(os.path.basename(m3u8_path))[0]
    mp4_path = os.path.join(out_dir, file_name + ".mp4")
    print(f"process [{file_name}] ...")
    if osp.exists(mp4_path):
        print(f"converted mp4 file {mp4_path} is exist")
        return
    ffmpeg_cmd = f"ffmpeg -allowed_extensions ALL -i {m3u8_path} -c copy {mp4_path}"
    if is_encode_audio:
        ffmpeg_cmd = f"ffmpeg -allowed_extensions ALL -i {m3u8_path} -c:v copy -c:a libopus {mp4_path}"
    ffmpeg_cmd = ffmpeg_cmd.encode(locale.getdefaultlocale()[1])
    try:
        proc = Popen(ffmpeg_cmd, stdout = PIPE, shell = True)
        print(proc.stdout.read())
    except:
        print(f"process {file_name} error...")    


def process_files(m3u8_dir, mp4_dir, is_encode_audio=False):
    all_files = os.listdir(m3u8_dir)
    m3u8_files = get_shufix_files(all_files, [".m3u8",])
    for m3u8_file in m3u8_files:
        m3u8_path = os.path.join(m3u8_dir, m3u8_file)
        if not osp.exists(m3u8_path + ".bak"):
            content_dir_root = osp.abspath(osp.dirname(m3u8_path)) 
            m3u8_path = fix_m3u8(m3u8_path, content_dir_root)
        m3u8_to_mp4(m3u8_path, mp4_dir, is_encode_audio)

def fix_m3u8_files(m3u8_dir:str, content_dir_root:str, end_tag:str="video"):
    all_files = os.listdir(m3u8_dir)
    m3u8_files = get_shufix_files(all_files, [".m3u8",])
    for idx, m3u8_file in enumerate(m3u8_files):
        m3u8_path = osp.join(m3u8_dir, m3u8_file)
        _ = fix_m3u8(m3u8_path, content_dir_root, end_tag)


def parse_args():
    parser = argparse.ArgumentParser(description='Convert offline m3u8 to mp4')    
    parser.add_argument('m3u8_dir', help='offline m3u8 file and content dir')
    parser.add_argument(
        '--mod',
        choices=['fix', 'convert', 'restore'],
        default='fix',
        help='fix is fix m3u8 file path, convert is convert the m3u8 offline files to mp4, restore mod is restore the org m3u8 file')
    parser.add_argument(
        '--content-dir',
        default=None,
        help='m3u8 content dir')
    parser.add_argument('--save-dir', default='./mp4', help='mp4 file save dir')
    parser.add_argument(
        '--encode-audio',
        action='store_true',
        help='enable encode audio')
    
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    m3u8_dir = args.m3u8_dir
    if args.mod == 'convert':
        mp4_dir = args.save_dir
        os.makedirs(mp4_dir, exist_ok=True)
        process_files(m3u8_dir, mp4_dir, args.encode_audio)  
        restore_m3u8_files(m3u8_dir)
    elif args.mod == 'fix' and args.content_dir is not None:
        fix_m3u8_files(m3u8_dir, args.content_dir)
    elif args.mod == 'restore':
        restore_m3u8_files(m3u8_dir)
    else:
        print("mod input a error type")

    print("=== Done ===")
    pass