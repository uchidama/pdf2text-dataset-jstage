
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

def bunkai_text(text):
    separator = "▁"

    # テキストを文分割する
    text = text.replace("\n", separator)

    bunkai = Bunkai()

    result = ""
    a = bunkai(text)
    a = list(a)  # Convert generator to list
    #a = [text]

    # 数字に続くピリオドで始まる単語をチェックする正規表現パターン
    pattern_num = re.compile(r'^\d+\.')
    pattern = re.compile(r'(?<=\S)▁(?=\S)')

    '''
    pattern = re.compile(r'(?<![0-9])▁(?!\d)')
    for sentence in a:
        sentence = re.sub(pattern, "", sentence)  # 任意の文字と文字の間にある ▁ (U+2581) のみ削除
        sentence = sentence.replace("▁", "\n")  # その他の ▁ (U+2581) は改行に戻す
        result += sentence
    '''    

    previous_word = ""

    for sentence in a:
        words = sentence.split(separator)

        for word in words:
            if word:
                
                temp_word = previous_word + '▁' + word
                replace_word = re.sub(pattern, "", temp_word)  # 任意の文字と文字の間にある ▁ (U+2581) のみ削除

                if pattern_num.match(word):
                    # 1. 2. 3. などの数字に続くピリオドで始まる単語の場合は改行を加える
                    result += "\n" + word
                elif pattern_num.match(previous_word):
                    # 前の単語が数字に続くピリオドで始まる単語の場合は改行を加える
                    result += word + "\n"
                elif temp_word != replace_word:
                    # 置換された場合は、改行なしで単語を追加
                    result += word
                else:
                    result += word + "\n"

                previous_word = word  # 現在の単語を前の単語として記憶

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
                
                #out.write(f"【page {i}】\n")
                out.write(text + "\n")  # ページのテキストを書き込む
                print(f"page {i}")
                print(text)
                i += 1

# フォルダpdfの中のPDFを全て処理する
process_pdf_files("pdf")
