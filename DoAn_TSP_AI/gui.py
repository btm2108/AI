import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tsp_utils import generate_data, get_distance_matrix_string
from sa_solver import solve_tsp_sa
from cso_solver import solve_tsp_cso

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
        # Thiết lập Frame tổng bên trái
        left_container = tk.Frame(self.root, width=420, bg="#e8e8e8")
        left_container.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # --- Khối 1: Cài đặt bài toán ---
        setup_frame = tk.LabelFrame(left_container, text=" THIẾT LẬP BÀI TOÁN ", font=("Arial", 10, "bold"), bg="#e8e8e8")
        setup_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(setup_frame, text="Số lượng thành phố (N):", bg="#e8e8e8").pack(side=tk.LEFT, padx=5, pady=5)
        self.entry_cities = tk.Entry(setup_frame, width=8, justify="center")
        self.entry_cities.insert(0, "20")
        self.entry_cities.pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(setup_frame, text="Tạo Bản đồ", command=self.gen_data, bg="lightgray").pack(side=tk.RIGHT, padx=10, pady=5)

        # --- Khối 2: Chạy thuật toán chính ---
        algo_frame = tk.LabelFrame(left_container, text=" THUẬT TOÁN CHÍNH ", font=("Arial", 10, "bold"), bg="#e8e8e8")
        algo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(algo_frame, text="Chạy Simulated Annealing (SA)", command=lambda: self.start_algo("SA"), bg="#add8e6", height=1).pack(fill=tk.X, padx=5, pady=2)
        tk.Button(algo_frame, text="Chạy Chicken Swarm (CSO)", command=lambda: self.start_algo("CSO"), bg="#90ee90", height=1).pack(fill=tk.X, padx=5, pady=2)
        tk.Button(algo_frame, text="Tạm dừng / Tiếp tục Đồ họa", command=self.toggle_pause, bg="#ffcc66").pack(fill=tk.X, padx=5, pady=2)

        # --- Khối 3: Nhật ký lộ trình (ĐÃ CÂN BẰNG KÍCH THƯỚC) ---
        log_frame = tk.LabelFrame(left_container, text=" NHẬT KÝ LỘ TRÌNH (ANIMATION) ", font=("Arial", 10, "bold"), bg="#e8e8e8")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(log_frame, height=12, width=50, font=("Consolas", 9), bg="white")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Khối 4: KHU VỰC BENCHMARK (ĐÃ CÂN BẰNG KÍCH THƯỚC) ---
        bench_frame = tk.LabelFrame(left_container, text=" HỆ THỐNG ĐỐI KHÁNG (TEST LOG) ", font=("Arial", 10, "bold"), bg="#dcdcdc")
        bench_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        btn_box = tk.Frame(bench_frame, bg="#dcdcdc")
        btn_box.pack(fill=tk.X)
        
        tk.Button(btn_box, text="So Sánh Trực Tiếp (Head-to-Head)", command=self.run_comparison, bg="gold", font=("Arial", 9, "bold")).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        tk.Button(btn_box, text="Xuất CSV", command=self.run_benchmark, bg="plum").pack(side=tk.RIGHT, padx=5, pady=5)
        
        self.bench_log = tk.Text(bench_frame, height=12, width=50, font=("Consolas", 9), bg="#f8f8f8", fg="#333")
        self.bench_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # --- Khối 5: Ma trận khoảng cách ---
        matrix_frame = tk.LabelFrame(left_container, text=" Ma trận Khoảng cách ", font=("Arial", 9), bg="#e8e8e8")
        matrix_frame.pack(fill=tk.X, padx=10, pady=5)
        self.matrix_text = tk.Text(matrix_frame, height=5, width=50, font=("Consolas", 8), bg="#f0f0f0")
        self.matrix_text.pack(fill=tk.X, padx=5, pady=5)

        # Frame Đồ thị bên phải
        right_frame = tk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(11, 6))
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
                messagebox.showwarning("Lỗi", "Số thành phố phải > 2!")
                return
        except ValueError:
            messagebox.showwarning("Lỗi", "Vui lòng nhập số nguyên!")
            return
            
        self.cities_data, self.dist_matrix = generate_data(self.num_cities)
        self.reset_plots()
        
        # Cập nhật Matrix
        matrix_str = get_distance_matrix_string(self.cities_data, self.dist_matrix)
        self.matrix_text.delete(1.0, tk.END)
        self.matrix_text.insert(tk.END, matrix_str)
        
        # Reset các bảng Log
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"--- ĐÃ KHỞI TẠO MAP: {self.num_cities} THÀNH PHỐ ---\n")
        self.bench_log.delete(1.0, tk.END)
        self.bench_log.insert(tk.END, "Sẵn sàng thực hiện đối kháng hệ thống...\n")
        
        # Vẽ thành phố
        x = [c[0] for c in self.cities_data]
        y = [c[1] for c in self.cities_data]
        self.ax1.scatter(x, y, c='black', zorder=5)
        for cx, cy, name in self.cities_data:
            self.ax1.text(cx+1, cy+1, name, fontsize=8, color="blue")
        self.canvas.draw()
        
    def start_algo(self, algo):
        if not self.dist_matrix:
            messagebox.showwarning("Lỗi", "Vui lòng tạo bản đồ trước!")
            return
            
        if self.animation_job:
            self.root.after_cancel(self.animation_job)
            
        self.log_text.delete(1.0, tk.END)
        self.log_text.insert(tk.END, f"Đang thực thi {algo}...\n")
        self.root.update()
        
        if algo == "SA":
            _, _, self.history, exec_time = solve_tsp_sa(self.dist_matrix)
            self.current_algo_name = "Simulated Annealing"
        else:
            _, _, self.history, exec_time = solve_tsp_cso(self.dist_matrix)
            self.current_algo_name = "Chicken Swarm Opt"
            
        self.log_text.insert(tk.END, f"Thời gian tính toán: {exec_time:.5f}s\n")
        self.current_frame = 0
        self.is_paused = False
        self.animate_step()
        
    def animate_step(self):
        if self.is_paused:
            self.animation_job = self.root.after(100, self.animate_step)
            return
            
        if self.current_frame < len(self.history):
            route, cost = self.history[self.current_frame]
            self.ax1.clear()
            self.ax1.set_title(f"{self.current_algo_name} - Frame: {self.current_frame}")
            
            x = [self.cities_data[i][0] for i in route] + [self.cities_data[route[0]][0]]
            y = [self.cities_data[i][1] for i in route] + [self.cities_data[route[0]][1]]
            
            line_color = 'green' if self.current_frame == len(self.history) - 1 else 'red'
            self.ax1.plot(x, y, marker='o', c=line_color, mfc='black', mec='black')
            
            for cx, cy, name in self.cities_data:
                self.ax1.text(cx+1, cy+1, name, fontsize=8, color="blue")
                
            self.ax2.clear()
            self.ax2.set_title("Biểu đồ Lịch sử Hội tụ")
            past_costs = [c for _, c in self.history[:self.current_frame+1]]
            self.ax2.plot(range(len(past_costs)), past_costs, c='blue')
            self.canvas.draw()
            
            if self.current_frame == 0 or cost < self.history[self.current_frame-1][1]:
                route_names = " -> ".join(self.cities_data[i][2] for i in route)
                self.log_text.insert(tk.END, f"[Lặp {self.current_frame}] Cost: {cost:.1f} | {route_names}\n")
                self.log_text.see(tk.END)
            
            self.current_frame += 1
            self.animation_job = self.root.after(20, self.animate_step)
        else:
            self.log_text.insert(tk.END, f"\n=> KẾT QUẢ CUỐI: {self.history[-1][1]:.2f}\n")
            self.log_text.see(tk.END)

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def run_benchmark(self):
        import csv
        try: n_cities = int(self.entry_cities.get())
        except: n_cities = 20
            
        self.bench_log.delete(1.0, tk.END)
        self.bench_log.insert(tk.END, "Đang chạy 30 vòng Benchmark ngầm...\n")
        self.root.update()
        
        with open('benchmark_results.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Cities', 'Cost_SA', 'Time_SA', 'Cost_CSO', 'Time_CSO'])
            for i in range(1, 31):
                _, dist_mat = generate_data(n_cities)
                _, c_sa, _, t_sa = solve_tsp_sa(dist_mat)
                _, c_cso, _, t_cso = solve_tsp_cso(dist_mat)
                writer.writerow([i, n_cities, round(c_sa, 2), round(t_sa, 4), round(c_cso, 2), round(t_cso, 4)])
                
        self.bench_log.insert(tk.END, "XONG! Đã xuất file: benchmark_results.csv\n")
        self.bench_log.see(tk.END)

    # =================================================================
    # HÀM NÂNG CẤP: SO SÁNH TRỰC TIẾP (CHI TIẾT NHƯ CONSOLE)
    # =================================================================
    def run_comparison(self):
        import time
        self.bench_log.delete(1.0, tk.END)
        self.bench_log.insert(tk.END, "=== BẮT ĐẦU ĐỐI KHÁNG TRỰC TIẾP ===\n\n")
        self.root.update()
        
        cases = [10, 20, 30, 40, 50]
        sa_wins = 0
        cso_wins = 0
        draws = 0
        
        for n in cases:
            self.bench_log.insert(tk.END, f"[*] BẢN ĐỒ {n} THÀNH PHỐ:\n")
            self.root.update()
            _, d_mat = generate_data(n)
            
            # Chạy thuật toán
            _, c_sa, _, t_sa = solve_tsp_sa(d_mat)
            _, c_cso, _, t_cso = solve_tsp_cso(d_mat)
            
            # In chi tiết Quãng đường và Thời gian
            self.bench_log.insert(tk.END, f" - SA : Quãng đường {c_sa:.2f} | {t_sa:.5f}s\n")
            self.bench_log.insert(tk.END, f" - CSO: Quãng đường {c_cso:.2f} | {t_cso:.5f}s\n")
            
            # Đánh giá độ chênh lệch
            if c_sa < c_cso:
                gap = c_cso - c_sa
                self.bench_log.insert(tk.END, f" => SA tìm đường ngắn hơn (Lệch {gap:.2f})\n")
                sa_wins += 1
            elif c_cso < c_sa:
                gap = c_sa - c_cso
                self.bench_log.insert(tk.END, f" => CSO tìm đường ngắn hơn (Lệch {gap:.2f})\n")
                cso_wins += 1
            else:
                self.bench_log.insert(tk.END, " => Hòa (Quãng đường bằng nhau)\n")
                draws += 1
                
            self.bench_log.insert(tk.END, "-"*45 + "\n")
            self.bench_log.see(tk.END)
            self.root.update()
            time.sleep(0.5) # Dừng một chút để tạo hiệu ứng phân tích
            
        # Tổng kết chung cuộc
        self.bench_log.insert(tk.END, "\n[ TỔNG KẾT TỈ SỐ ]\n")
        self.bench_log.insert(tk.END, f"SA thắng: {sa_wins} | CSO thắng: {cso_wins} | Hòa: {draws}\n")
        
        winner = "SA (Luyện Kim Giả Lập)" if sa_wins > cso_wins else "CSO (Bầy Đàn Con Gà)" if cso_wins > sa_wins else "Hai thuật toán"
        self.bench_log.insert(tk.END, f"=> CHUNG CUỘC: {winner} hiệu quả hơn.\n")
        self.bench_log.see(tk.END)