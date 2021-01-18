# -\- coding: utf-8 -\-
# -F:打包成一个EXE文件 
# -w:不带console输出控制台，window窗体格式(外带文件时不可用窗体模式)
# --paths：依赖包路径 
# --icon：图标 
# --noupx：不用upx压缩 
# --clean：清理掉临时文件

from PyInstaller.__main__ import run

designer_path = r'D:\Anaconda3\Lib\site-packages\qt5_applications\Qt\bin'
plugins_path = r'D:\Anaconda3\Lib\site-packages\qt5_applications\Qt\plugins'
UPX_DIR = r'D:\Anaconda3\Scripts'

if __name__ == '__main__':
    opts = [
            # '-F',
            '-w',
            '--paths='+designer_path,
            '--paths='+plugins_path,
            # '--icon=favicon.ico',
            '--noupx',
            '--clean',
            "--name=new_test",
            'main.py']
    run(opts)
