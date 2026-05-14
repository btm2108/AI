import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tsp_utils import generate_data, get_distance_matrix_string
from sa_solver import solve_tsp_sa
from cso_solver import solve_tsp_cso  # ĐỔI ACO THÀNH CSO

class TspAppGUI:
    def __init__(self, root, num_cities=15):
        self.root = root
        self.num_cities = num_cities
        self.cities_data = []
        self.dist_matrix = []
        
        # Biến điều khiển Animation
        self.history = []
        self.current_frame = 0
        self.is_paused = False
        self.animation_job = None
        self.current_algo_name = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        # Khởi tạo Frame điều khiển bên trái (2 dòng này bị thiếu)
        left_frame = tk.Frame(self.root, width=300, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        tk.Label(left_frame, text="BẢNG ĐIỀU KHIỂN", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=5)
        
        # Ô nhập liệu số thành phố
        tk.Label(left_frame, text="Số lượng thành phố:", bg="#f0f0f0").pack(pady=(10, 0))
        self.entry_cities = tk.Entry(left_frame, width=10)
        self.entry_cities.insert(0, "10") # Mặc định là 10
        self.entry_cities.pack(pady=5)
        
        # Các nút bấm
        tk.Button(left_frame, text="1. Tạo Bản đồ mới", command=self.gen_data, width=30, bg="lightgray").pack(pady=5)
        tk.Button(left_frame, text="2. Chạy Luyện Kim Giả Lập (SA)", command=lambda: self.start_algo("SA"), width=30, bg="lightblue").pack(pady=5)
        tk.Button(left_frame, text="3. Chạy Bầy Đàn Con Gà (CSO)", command=lambda: self.start_algo("CSO"), width=30, bg="lightgreen").pack(pady=5)
        tk.Button(left_frame, text="4. Chạy Benchmark (Xuất CSV)", command=self.run_benchmark, width=30, bg="plum").pack(pady=5)
        
        self.btn_pause = tk.Button(left_frame, text="Tạm dừng / Tiếp tục", command=self.toggle_pause, width=30, bg="orange")
        self.btn_pause.pack(pady=5)
        
        # Bảng Log và Ma trận
        tk.Label(left_frame, text="Nhật ký Lộ trình (Solution Log):", bg="#f0f0f0").pack(anchor="w", pady=(5, 0))
        self.log_text = tk.Text(left_frame, height=10, width=40, font=("Consolas", 8))
        self.log_text.pack(pady=5)
        
        tk.Label(left_frame, text="Ma trận Khoảng cách:", bg="#f0f0f0").pack(anchor="w")
        self.matrix_text = tk.Text(left_frame, height=10, width=40, font=("Consolas", 8))
        self.matrix_text.pack(pady=5)
        
        # Frame Đồ thị bên phải
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.reset_plots()
        
    def reset_plots(self):
        self.ax1.clear()
        self.ax1.set_title("Bản đồ Lộ trình")
        self.ax2.clear()
        self.ax2.set_title("Biểu đồ Lịch sử Hội tụ")
        self.canvas.draw()
        
    def gen_data(self):
        try:
            self.num_cities = int(self.entry_cities.get())
            if self.num_cities < 3:
                messagebox.showwarning("Lỗi", "Số thành phố phải lớn hơn 2!")
                return
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập số nguyên hợp lệ!")
            return
            
        self.cities_data, self.dist_matrix = generate_data(self.num_cities)
        self.reset_plots()
        
        # Hiển thị Ma trận lên Textbox
        matrix_str = get_distance_matrix_string(self.cities_data, self.dist_matrix)
        self.matrix_text.delete(1.0, tk.END)
        self.matrix_text.insert(tk.END, matrix_str)
        self.log_text.delete(1.0, tk.END)
        
        # Vẽ các thành phố (Kèm tên)
        x = [c[0] for c in self.cities_data]
        y = [c[1] for c in self.cities_data]
        self.ax1.scatter(x, y, c='black', zorder=5)
        for cx, cy, name in self.cities_data:
            self.ax1.text(cx+1, cy+1, name, fontsize=8, color="blue")
        self.canvas.draw()
        
    def start_algo(self, algo):
        if not self.dist_matrix:
            messagebox.showwarning("Lỗi", "Vui lòng bấm tạo dữ liệu trước!")
            return
            
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"Đang chạy {algo}...\n")
        self.root.update()
        
        # Chạy ẩn thuật toán để lấy toàn bộ lịch sử
        # Chạy ẩn thuật toán để lấy toàn bộ lịch sử
        if algo == "SA":
            _, _, self.history, exec_time = solve_tsp_sa(self.dist_matrix)
            self.current_algo_name = "Simulated Annealing"
        else:
            _, _, self.history, exec_time = solve_tsp_cso(self.dist_matrix)
            self.current_algo_name = "Chicken Swarm Optimization"
            
        self.log_text.insert(tk.END, f"Thời gian xử lý: {exec_time:.3f}s\nBắt đầu dựng đồ họa...\n")
        
        # Bắt đầu Animation
        self.current_frame = 0
        self.is_paused = False
        self.animate_step()
        
    def animate_step(self):
        if self.is_paused:
            self.animation_job = self.root.after(100, self.animate_step)
            return
            
        if self.current_frame < len(self.history):
            route, cost = self.history[self.current_frame]
            
            # Cập nhật đồ thị 1 (Bản đồ)
            self.ax1.clear()
            self.ax1.set_title(f"{self.current_algo_name} - Frame: {self.current_frame}")
            
            x = [self.cities_data[i][0] for i in route] + [self.cities_data[route[0]][0]]
            y = [self.cities_data[i][1] for i in route] + [self.cities_data[route[0]][1]]
            
            # Nếu là frame cuối, vẽ màu xanh lá (Tối ưu), ngược lại vẽ màu đỏ (Đang tìm)
            line_color = 'green' if self.current_frame == len(self.history) - 1 else 'red'
            self.ax1.plot(x, y, marker='o', c=line_color, mfc='black', mec='black')
            
            for cx, cy, name in self.cities_data:
                self.ax1.text(cx+1, cy+1, name, fontsize=8, color="blue")
                
            # Cập nhật đồ thị 2 (Hội tụ)
            self.ax2.clear()
            self.ax2.set_title("Biểu đồ Lịch sử Hội tụ")
            past_costs = [c for _, c in self.history[:self.current_frame+1]]
            self.ax2.plot(range(len(past_costs)), past_costs, c='blue')
            self.ax2.set_xlabel("Vòng lặp")
            self.ax2.set_ylabel("Quãng đường")
            
            self.canvas.draw()
            
            # Ghi Log các lộ trình tìm được (Chỉ ghi khi có sự cải thiện để tránh tràn log)
            if self.current_frame == 0 or cost < self.history[self.current_frame-1][1]:
                route_names = " ➔ ".join(self.cities_data[i][2] for i in route)
                self.log_text.insert(tk.END, f"[{self.current_frame}] Cost: {cost:.2f} | {route_names}\n")
                self.log_text.see(tk.END)
            
            self.current_frame += 1
            # Tốc độ khung hình (30ms)
            self.animation_job = self.root.after(30, self.animate_step)
        else:
            final_cost = self.history[-1][1]
            self.log_text.insert(tk.END, f"\nHOÀN THÀNH!\nBest Tour Length: {final_cost:.2f}\n")
            self.log_text.see(tk.END)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
    def run_benchmark(self):
            import csv
            import random
            
            # Lấy giá trị từ ô nhập liệu hoặc dùng mặc định
            try:
                n_cities = int(self.entry_cities.get())
            except ValueError:
                n_cities = 10
                
            self.log_text.insert(tk.END, "\nĐang chạy 30 bài test tự động...\n")
            self.root.update()
            
            with open('benchmark_results.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # Tạo tiêu đề cho file CSV
                # Tạo tiêu đề cho file CSV
            writer.writerow(['Test ID', 'So_Thanh_Pho', 'Chi_Phi_SA', 'Thoi_Gian_SA', 'Chi_Phi_CSO', 'Thoi_Gian_CSO'])
            
            for i in range(1, 31):
                # Tạo bản đồ ngẫu nhiên cho mỗi bài test
                _, dist_mat = generate_data(n_cities)
                
                # Chạy SA
                _, cost_sa, _, time_sa = solve_tsp_sa(dist_mat)
                
                # Chạy CSO (Gà)
                _, cost_cso, _, time_cso = solve_tsp_cso(dist_mat)
                
                # Ghi kết quả
                writer.writerow([i, n_cities, round(cost_sa, 2), round(time_sa, 4), round(cost_cso, 2), round(time_cso, 4)])
                    
            self.log_text.insert(tk.END, f"Đã lưu kết quả 30 vòng chạy vào file 'benchmark_results.csv'!\n")
            self.log_text.see(tk.END)