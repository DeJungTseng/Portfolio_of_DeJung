from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
import view
from tkinter import messagebox


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
        # get the recommandation from the backend
        # image_names,image_paths=main_exec.main(user_id=self.login_dialog.user_id)
        # self.image_names=image_names
        # self.image_paths=image_paths
        self.image_paths = ["Images/AI_and_ai.jpg", "Images/lawyerhell.jpg", "Images/library.jpg","Images/gandam.jpg","Images/goose.jpg"]
        self.image_names = ["AI與小愛", "地獄律師", "圖書館裡的妖精","鋼彈吊單槓","以鵝傳鵝"]

        # self.image_paths =["Images/"+item['poster']]
        # self.image_names = ["movie_title"]

        self.canvas = view.TopCanvas(self.top_frame, self.image_paths, self.image_names, self.add_to_watchlist,height=400,bg='white' )
        self.canvas.pack(fill="both", expand=True)
        # ====End Top Canvas=====

        # =====End Top Frame=
        
        # =====Bottom Container=====
        bottom_container = ttk.Frame(main_container)
        bottom_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # =====Bottom Frame Left=====
        self.bottom_frame_left = ttk.LabelFrame(bottom_container, text="待播清單", padding=10)

        # ====Watch List Treeview====
        self.watch_list =view.TreeViewWidget(self.bottom_frame_left)
        self.watch_list.pack(fill="both", expand=True)

        # =====End =Watch List Treeview====
        self.bottom_frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        # =====End Bottom Frame Left=====


        
        # =====Bottom Frame Right=====
        self.bottom_frame_right = ttk.LabelFrame(bottom_container, text="觀看紀錄", padding=10)
   

        # =====Played List Treeview====
        self.played_list = view.TreeViewWidget(self.bottom_frame_right)
        # movie_title=datasource.get_watched(user_id)
        # for item in movie_title:
        #     self.played_list.add_item(item)
        # movie_title is a pd frame
        self.played_list.add_item("datasource")
        self.played_list.add_item("三生三世三十場考試")
        self.played_list.add_item("我的模型還活著嗎")
        self.played_list.add_item("南港展覽館官方網站綻放萬丈光芒")
        self.played_list.add_item("紅鯉魚與綠鯉魚與驢")
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



def main():
    window = Window(theme="breeze")
    window.mainloop()

if __name__ == '__main__':
    main()