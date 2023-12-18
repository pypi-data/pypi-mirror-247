import os
import sys
import getpass
import subprocess


CACHE_DIR = os.path.join(os.path.expanduser('~'), '.huggingface_cache')
if not os.path.exists(CACHE_DIR):
    os.mkdir(CACHE_DIR)


def download_model(model_id, hf_url='https://hf-mirror.com/', threads=10):
    model_dir = model_id.split('/')[1]
    if os.path.exists(os.path.join(CACHE_DIR, model_dir)):
        print('模型 {} 已存在！'.format(model_dir))
        return os.path.join(CACHE_DIR, model_dir)

    # install aria2 and git
    username = getpass.getuser()
    cmd_prefix = '' if username == 'root' else 'sudo '
    status, _ = subprocess.getstatusoutput('command -v aria2c')
    if status != 0:
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt update')
        if status != 0:
            print('apt update 失败！')
            return None
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y aria2')
        if status != 0:
            print('安装 aria2 失败！')
            return None
    status, _ = subprocess.getstatusoutput('command -v git')
    if status != 0:
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt update')
        if status != 0:
            print('apt update 失败！')
            return None
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y git')
        if status != 0:
            print('安装 git 失败！')
            return None
        status, _ = subprocess.getstatusoutput(cmd_prefix + 'apt install -y git-lfs')
        if status != 0:
            print('安装 git-lfs 失败！')
            return None

    cwd = os.getcwd()

    # Clone模型代码（不下载长文件）
    os.chdir(CACHE_DIR)
    url = hf_url + model_id
    os.environ['GIT_LFS_SKIP_SMUDGE'] = '1'
    status, _ = subprocess.getstatusoutput('git clone ' + url)
    if status != 0:
        print('克隆 {} 失败！'.format(url))
        os.chdir(cwd)
        return None

    # 找出所有长文件
    os.chdir(model_dir)
    status, output = subprocess.getstatusoutput('git lfs ls-files')
    output = output.split('\n')
    ls_files = []
    for line in output:
        file = line.split(' ')[2]
        ls_files.append(file)
        os.system('truncate -s 0 ' + file)

    # 下载所有长文件
    for file in ls_files:
        url = hf_url + model_id + '/resolve/main/' + file
        file_dir = subprocess.getoutput('dirname ' + file)
        file_name = subprocess.getoutput('basename ' + file)
        os.system('mkdir -p ' + file_dir)
        os.system('aria2c -x {} -s {} -k 1M -c {} -d {} -o {}'.format(threads, threads, url, file_dir, file_name))

    os.chdir(cwd)
    return os.path.join(CACHE_DIR, model_dir)


def download():
    download_model(sys.argv[1])


if __name__ == '__main__':
    download_model('vinvino02/glpn-kitti')
