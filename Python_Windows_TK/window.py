from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
import view
from tkinter import messagebox
import datasource
from recommendation_engine import get_recommendation  

class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # First handle login before creating any widgets
        self.withdraw()  # Hide main window
        self.login_dialog = view.LoginDialog(self, title="登入")

        # If login failed or was cancelled, close the application
        if not self.login_dialog.apply():
            print("Login cancelled or failed")
            self.quit()
            self.destroy()  # Ensure window is properly destroyed
            return

        # Only proceed with window setup if login was successful
        print("Login successful, initializing main window")
        self.title('Watch new movie now!')

        # ====Geometry====
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 1200
        window_height = 675
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        self.resizable(False, False)
        # =====End Geometry=====

        # Create widgets only after successful login
        self.create_widgets()

        # Show the main window
        self.deiconify()

    def create_widgets(self):
        # 設定樣式
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel', font=('Arial', 20))

        # 創建主容器
        main_container = ttk.Frame(self, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)

        # =====Top Frame=====
        self.top_frame = ttk.LabelFrame(main_container, text="你可能會喜歡", padding=10)
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # ====Top Canvas=====
        user_id = self.login_dialog.username.get()
        self.image_names, self.image_paths = get_recommendation(user_id)

        self.canvas = view.TopCanvas(
            self.top_frame,
            self.image_paths,
            self.image_names,
            self.add_to_watchlist,
            height=400,
            bg='white'
        )
        self.canvas.pack(fill="both", expand=True)
        # ====End Top Canvas=====

        # =====End Top Frame=

        # =====Bottom Container=====
        bottom_container = ttk.Frame(main_container)
        bottom_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # =====Bottom Frame Left=====
        self.bottom_frame_left = ttk.LabelFrame(bottom_container, text="待播清單", padding=10)

        # ====Watch List Treeview====
        self.watch_list = view.TreeViewWidget(self.bottom_frame_left)
        self.watch_list.pack(fill="both", expand=True)

        # =====End =Watch List Treeview====
        self.bottom_frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        # =====End Bottom Frame Left=====

        # =====Bottom Frame Right=====
        self.bottom_frame_right = ttk.LabelFrame(bottom_container, text="觀看紀錄", padding=10)

        # =====Played List Treeview====
        self.after(100, self.load_watched_movies)
        self.played_list = view.TreeViewWidget(self.bottom_frame_right)
        self.played_list.clear_all()

        self.played_list.pack(fill="both", expand=True)
        # =====End Played List Treeview====

        self.bottom_frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        # =====End Bottom Frame Right=====

    def add_to_watchlist(self, image_name):
        """
        Callback function for handling image click events.
        Adds the clicked image's name to the TreeView.
        """
        self.watch_list.add_item(image_name)

    def load_watched_movies(self):
        self.played_list.clear_all()
        watched_list = datasource.get_watched(self.login_dialog.username.get())
        for movie in watched_list:
            self.played_list.add_item(movie['movie_title'])


# def main():
#     window = Window(theme="breeze")
#     window.mainloop()

# if __name__ == '__main__':
#     main()