from . import analyzer
from pathlib import Path
import json

def start():
#用户输入文件或文件夹（输入错误则循环提示）
    ff = input("input a file or folder: ")
    f = Path(ff)
    while not ff or not f.exists():
        ff = input("wrong directory, please input again: ")
        f = Path(ff)

    # f = Path('/Users/jess/Desktop/python/测试中文.txt')
    # f = Path("/Users/jess/Desktop/python")

    if f.is_file():
        b = analyzer.get_file_basic(f)
        w = analyzer.get_file_word_analyze(f,top_num=5)
        t = analyzer.get_file_analysis(f,5)
        print(f'file full info: {t.model_dump_json(indent=2)}')
    elif f.is_dir():
        b = analyzer.get_folder_basic(f)
        w = analyzer.get_folder_word_analyze(f,5)
        t = analyzer.get_folder_analysis(f,5)
        print(t)

if __name__ == "__main__":
    start()