
# bunkai 1.5.7
# https://pypi.org/project/bunkai/
#
# 

# 仮想環境の作成
# python3 -m venv venv

# 
# source venv/bin/activate

# requests.txtの作成
# pip freeze > requests.txt


import fitz  # PyMuPDF
from bunkai import Bunkai
from pathlib import Path
import re

def insert_newlines_for_subheadings(text):
    # 小見出し後に改行を挿入するための正規表現パターン
    subheading_pattern = re.compile(r'(\d+\．[^\s]+)')
    # 小見出しの後に改行を挿入
    modified_text = re.sub(subheading_pattern, r'\1\n', text)
    return modified_text

def bunkai_text(text):
    # 既存の処理...
    # text = insert_newlines_for_subheadings(text)

    # テキストを文分割する
    text = text.replace("\n", "▁")
    #print("text:" + text)

    bunkai = Bunkai()
    #pattern = re.compile(r'(?<=\S)▁(?=\S)')
    #pattern = re.compile(r'(?<=\S)▁(?!\d)')
    pattern = re.compile(r'(?<![0-9])▁(?!\d)')

    result = ""
    a = bunkai(text)
    a = list(a)  # Convert generator to list
    print("a len:", len(a))
    
    for sentence in a:
        sentence = re.sub(pattern, "", sentence)  # 任意の文字と文字の間にある ▁ (U+2581) のみ削除
        sentence = sentence.replace("▁", "\n")  # その他の ▁ (U+2581) は改行に戻す
        result += sentence

    return result

def process_pdf_files(folder_path):
    pdf_files = Path(folder_path).glob('*.pdf')
    for pdf_file in pdf_files:
        doc = fitz.open(pdf_file)  # ドキュメントを開く
        output_filename = pdf_file.stem + ".txt"  # 出力ファイル名を設定
        with open("pdf_text/" + output_filename, "w") as out:  # テキスト出力を作成する
            i = 0
            for page in doc:  # ドキュメントのページを反復処理する
                text = page.get_text().encode("utf8")  # プレーンテキストを取得（UTF-8形式）
                text = bunkai_text(text.decode("utf8"))
                
                out.write(f"【page {i}】\n")
                out.write(text + "\n")  # ページのテキストを書き込む
                print(f"page {i}")
                print(text)
                i += 1

# フォルダpdfの中のPDFを全て処理する
process_pdf_files("pdf")
