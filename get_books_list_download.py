import csv
import os
class BookFinder:
    def __init__(self, csv_file):
        self.books = []
        self.load_books(csv_file)

    def load_books(self, csv_file):
        # 从CSV文件加载书籍信息
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.books.append(row)
    def find_books_by_author(self, author):
      # 根据作者姓名查找所有书籍
        author_books=[]
        for book in self.books:
            if book['作者'] == author:
                author_books.append(book)
        return author_books

    def book_info_by_title(self, title):
      # 根据书名获取书籍的详细信息
        for book in self.books:
            if book['书名'] == title:
                return book
        return None

def books_find(csv_file):
    books_id_list=[]
    # 判断文件路径是否有误
    if not os.path.exists(csv_file):
        print(f"错误：文件 {csv_file} 不存在。")
        return

    book_finder = BookFinder(csv_file)
    books_id_list=[]
    books_name_list=[]
    while True:
        search_type = input("请输入 'author' 查找作者书籍，或输入 'title' 查找书名信息(输入 'exit' 退出): ").strip().lower()

        if search_type == 'exit':
            print("退出书籍查找程序。")
            return books_id_list,books_name_list
            # break

        if search_type == 'author':
            author = input('请输入作者名字以查找书籍信息: ').strip()
            if not author:
                print("作者名字不能为空。")
                continue
            author_books = book_finder.find_books_by_author(author)
            if author_books:
                print(f"下面是与作者‘{author}’相关的书籍:")
                temporary_books_list=[]
                for book in author_books:
                    temporary_books_list.append(book)
                    # print(book)
                    print(f"{len(temporary_books_list)}、ID: {book['ID']}, 书名: {book['书名']}, 作者: {book['作者']}, 类型: {book.get('类型')}, 评分: {book.get('评分',)}, 封面链接: {book.get('封面链接',)}")

                download_intention=input('请问你是否需要下载书籍(Y/n)?:')
                if download_intention.strip().lower() == 'y':
                    books_order_author_str = input("请输入你要下载的书籍序号,以','分隔:").strip()
                    books_order_author = [int(book_order) - 1 for book_order in books_order_author_str.split(',')]
                    # print(books_order_author)
                    for order in books_order_author:
                        books_id_list.append(temporary_books_list[order].get('ID'))
                        books_name_list.append(temporary_books_list[order].get('书名'))
                    # print(books_id_list)

            else:
                print(f"没有找到作者 {author} 的书籍。")

        elif search_type == 'title':
            title = input('请输入书名以查找书籍信息: ').strip()
            if not title:
                print("书名不能为空。")
                continue
            book_info = book_finder.book_info_by_title(title)
            temporary_books_list = []
            if book_info:
                temporary_books_list.append(book)
                print(f"{len(temporary_books_list)}、: ID: {book_info['ID']}, 书名: {book_info['书名']}, 作者: {book_info['作者']}, 封面链接: {book_info.get('封面链接')}")

                download_intention = input('请问你是否需要下载书籍(Y/n)?:')
                if download_intention.lower() == 'y':
                    books_order_author_str = input("请输入你要下载的书籍序号,以','分隔:").strip()
                    books_order_author = [int(book_order) - 1 for book_order in books_order_author_str.split(',')]
                    # print(books_order_author)
                    for order in books_order_author:
                        books_id_list.append(temporary_books_list[order].get('ID'))
                        books_name_list.append(temporary_books_list[order].get('书名'))
                    # print(books_id_list)
            else:
                print("没有找到该书籍。")

        else:
            print("无效的输入，请重新输入。")

if __name__ == '__main__':
    path=r'榜单存储路径'
    books_id_list=books_find(path)
    print(books_id_list)