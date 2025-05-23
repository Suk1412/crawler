import os
import re


def creat_txt(note_path=None, book_name="未命名", chapter_name="未命名"):
    folder_path = os.path.dirname(__file__) + f"/../note/{book_name}"
    if note_path is not None:
        folder_path = note_path + f"/note/{book_name}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for i in range(1, 20):
        chapter_path = folder_path + f"/第{i}章 " + chapter_name + f".txt"
        with open(chapter_path, 'w') as file:
            file.write(str(i))
    return folder_path


def mergers_chapter(book_path=None, book_name="未命名"):
    def extract_chapter_number(name):
        match = re.search(r'第(\d+)章', name)
        return int(match.group(1)) if match else 0

    if book_path is not None:
        files = os.listdir(book_path)
        files = [f for f in files if re.match(r'^第\d+章', f)]
        files.sort(key=extract_chapter_number)
        num = 0
        for file_name in files:
            num += 1
            file_path = os.path.join(book_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                content_r = f.read()
                if num == 1:
                    with open(book_path + "/" + book_name + ".txt", 'w', encoding='utf-8') as f:
                        f.write(content_r + "\r\n"*3)
                else:
                    with open(book_path + "/" + book_name + ".txt", 'a', encoding='utf-8') as f:
                        f.write(content_r + "\r\n"*3)



if __name__ == "__main__":
    file_path = creat_txt(note_path="/home/wx/Documents")
    mergers_chapter(book_path=file_path)
    # print(os.path.dirname(__file__))