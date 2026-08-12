from sites.parser import Parser
from sites.config_loader import load_config_for_url   

if __name__ == "__main__":
    url = 'https://m.shuhaige.net/382358/'
    config = load_config_for_url(url)
    parser = Parser(config)
    book_name = parser.get_book_name(url)
    chapters = parser.get_chapter_list(url)

    content_url = list(chapters.values())[0][1]
    content = parser.get_chapter_content(content_url)
    print(content)
