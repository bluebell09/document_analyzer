import jieba
import re
import json
from collections import Counter
from pathlib import Path
from typing import Any
from models import FileBasic, WordAnalysis, FileAnalysis

#获得该文件的基础信息（字符数，行数）
def get_file_basic(file: Path) ->  FileBasic:
    file_name = file.name #Path可以直接通过.name得到文件名
    with open(file, encoding="utf_8-sig",errors="ignore") as f:
        char_count = 0
        line_count = 0
        for line in f: #直接按行读取
            char_count += len(line.rstrip('\r\n'))
            line_count += 1
    data = {"file_name":file_name, "char_count": char_count, "line_count": line_count}
    return FileBasic.model_validate(data)

#获得该文件夹中所有文件的基础信息（“.txt”文件名对应的字符数，行数）
def get_folder_basic(folder: Path) -> list[FileBasic]:
    basic = list()
    for file in folder.glob("*.txt"): #该文件夹中所有的“.txt”文件
        basic.append(get_file_basic(file))
    return basic

#该文件的单词数，及前xx的高频单词
def get_file_word_analyze(file: Path, top_num= None) -> WordAnalysis:
    chunk_size = 4096
    remainder = ""
    ending = re.compile(r"[，。；？！ ]")
    top_words = ()
    word_count = 0
    cleanword_lib ={}
    if top_num is not None:
        with open("/Users/jess/Desktop/python/stop_words.json",encoding="utf-8-sig",errors="ignore") as j:
            stopwords = json.load(j)
    file_name = file.name #Path可以直接通过.name得到文件名
    with open(file, encoding="utf_8-sig",errors="ignore") as f:
        #按照chunk size分段导入，防止文件过大，同时处理段末的词，使之不被切割成两份
        while chunk := f.read(chunk_size):
            simp_words=[]
            sentence = list(ending.finditer(chunk))
            if sentence:
                last_match = sentence[-1].end()
                text = remainder + chunk[:last_match]
                remainder = chunk[last_match:]
            else:
                text = remainder + chunk

            #对每个chunk进行词统计
            words = jieba.cut(text)
            for word in words:
                simp_word = word.strip().lower()
                if simp_word and simp_word not in "。，；“”.,;":
                    simp_words.append(simp_word)
            word_count += len(simp_words)
            #若高频词传参，则过滤stop words后统计剩下各词的出现次数
            if top_num is not None:
                for word in simp_words:
                    if word not in stopwords: 
                        cleanword_lib[word] = cleanword_lib.get(word, 0) + 1
        if top_num is not None: #若高频词传参，则统计最高频次出现的词
            top_words = Counter(cleanword_lib).most_common(top_num)
        analysis = {"file_name":file_name, "word_count":word_count, "top_words": top_words}
    return WordAnalysis.model_validate(analysis)

#该文件夹中所有的“.txt”文件的单词数，及前xx的高频单词
def get_folder_word_analyze(folder: Path, top_num= None) -> list[WordAnalysis]:
    folder_words =list()
    for file in folder.glob("*.txt"): #该文件夹中所有的“.txt”文件
        folder_words.append(get_file_word_analyze(file, top_num))
    return folder_words

#利用已有的2个分析函数，得到完整的文件的分析结果
def get_file_analysis(file: Path, top_num = None) -> FileAnalysis:
    if file_info :=get_file_basic(file):
        word_info = get_file_word_analyze(file, top_num)
        data ={
            "file_name" : file_info.file_name,
            "char_count" :  file_info.char_count,
            "line_count": file_info.line_count,
            "word_count": word_info.word_count,
            "top_words": word_info.top_words
        }
    return FileAnalysis.model_validate(data)

#整个文档的完整的分析结果
def get_folder_analysis(folder: Path, top_num = None) -> list[FileAnalysis]:
    folder_info = list()
    for file in folder.glob("*.txt"):
        folder_info.append(get_file_analysis(file,top_num))
    return folder_info
