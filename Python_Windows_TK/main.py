# main.py
from window import Window


def main():
    """
    啟動整個 GUI 應用程式。
    登入與推薦邏輯皆在 Window 中處理。
    """
    window = Window(theme="breeze")
    window.mainloop()


if __name__ == "__main__":
    main()
