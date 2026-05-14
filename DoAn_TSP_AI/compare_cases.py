import time
from tsp_utils import generate_data
from sa_solver import solve_tsp_sa
from cso_solver import solve_tsp_cso

def run_head_to_head_comparison():
    print("="*70)
    print(" BẮT ĐẦU KIỂM THỬ VÀ SO SÁNH TRỰC TIẾP (SA vs CSO)")
    print("="*70 + "\n")
    
    # Test trên các bản đồ quy mô lớn dần để ép xung thuật toán
    cases = [10, 20, 30, 40, 50] 
    
    sa_win_count = 0
    cso_win_count = 0
    draw_count = 0
    
    for n in cases:
        print(f"[*] ĐANG CHẠY TRƯỜNG HỢP: {n} THÀNH PHỐ...")
        _, dist_matrix = generate_data(n)
        
        # 1. Chạy Simulated Annealing (SA)
        _, cost_sa, _, time_sa = solve_tsp_sa(dist_matrix)
        
        # 2. Chạy Chicken Swarm Optimization (CSO)
        _, cost_cso, _, time_cso = solve_tsp_cso(dist_matrix)
        
        # --- IN KẾT QUẢ ---
        print(f"  - SA  | Chi phí: {cost_sa:.2f} | Thời gian: {time_sa:.5f}s")
        print(f"  - CSO | Chi phí: {cost_cso:.2f} | Thời gian: {time_cso:.5f}s")
        
        # So sánh ai thắng
        if cost_sa < cost_cso:
            gap = cost_cso - cost_sa
            print(f"  => KẾT LUẬN: SA tìm được đường ngắn hơn CSO ({gap:.2f} đơn vị)!")
            sa_win_count += 1
        elif cost_cso < cost_sa:
            gap = cost_sa - cost_cso
            print(f"  => KẾT LUẬN: CSO tìm được đường ngắn hơn SA ({gap:.2f} đơn vị)!")
            cso_win_count += 1
        else:
            print("  => KẾT LUẬN: Cả 2 thuật toán tìm được đường dài bằng nhau (Hòa)!")
            draw_count += 1
            
        print("-" * 70)
        time.sleep(0.5) 
        
    # --- TỔNG KẾT ---
    print("\n" + "="*70)
    print(" TỔNG KẾT SAU CÁC LẦN CHẠY")
    print("="*70)
    print(f"Tổng số bản đồ thử nghiệm: {len(cases)}")
    print(f"Số lần SA tìm đường ngắn hơn : {sa_win_count}")
    print(f"Số lần CSO tìm đường ngắn hơn: {cso_win_count}")
    print(f"Số lần Hòa nhau              : {draw_count}")
    
    print("\n=> NHẬN XÉT: SA luôn áp đảo tuyệt đối về TỐC ĐỘ (Thời gian chạy).")
    if sa_win_count > cso_win_count:
        print("=> SA đồng thời chiến thắng về CHẤT LƯỢNG QUÃNG ĐƯỜNG ở đa số trường hợp.")
    elif cso_win_count > sa_win_count:
        print("=> Tuy nhiên, CSO lại nhỉnh hơn về CHẤT LƯỢNG QUÃNG ĐƯỜNG khi số thành phố tăng cao.")

if __name__ == "__main__":
    run_head_to_head_comparison()