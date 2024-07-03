import download_books
import get_books_list_download



books_id_list, books_name_list = get_books_list_download.books_find(r'D:\pythonProject\python课设\课设项目\fanqie\data.csv')
download_books.cycle_download(books_id_list, books_name_list)