import tkinter as tk
from gui import TspAppGUI

def main():
    root = tk.Tk()
    root.title("Hệ Thống Trí Tuệ Nhân Tạo: Bài Toán Người Du Lịch (TSP)")
    root.geometry("1200x650") # Mở rộng khung cửa sổ để chứa Textbox
    
    app = TspAppGUI(root, num_cities=15)
    
    root.mainloop()

if __name__ == "__main__":
    main()