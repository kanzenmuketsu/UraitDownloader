login = ""            # ваше имя пользователя
password = ""         # ваш пароль

def getURL() -> str:

    bookURL = input('Всавьте ссылку на книгу\n==> ')

    viewerURL = bookURL.replace("book", "viewer") + '#page/'
    bookname = (bookURL.split('/'))[4]

    return (viewerURL, bookname)
