from pydantic import BaseModel
class FileBasic(BaseModel):
    file_name: str
    char_count: int
    line_count: int

# class FolderBasic(BaseModel):
#     folder_name: str
#     folder: list[FileBasic]

class WordAnalysis(BaseModel):
    file_name: str
    word_count: int
    top_words: list[tuple[str,int]] 

class FileAnalysis(BaseModel):
    file_name: str
    char_count: int
    line_count: int
    word_count: int
    top_words: list[tuple[str,int]]
    
