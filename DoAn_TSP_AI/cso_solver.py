import random
import time
from tsp_utils import calculate_total_distance

# Hàm lai ghép (Order Crossover - OX) để gà mái học hỏi lộ trình của gà trống
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [-1] * size
    
    # Lấy một đoạn gen của gà mái
    child[start:end] = parent1[start:end]
    
    # Lấp đầy các thành phố còn thiếu dựa trên lộ trình của gà trống
    p2_idx = 0
    for i in range(size):
        if child[i] == -1:
            while parent2[p2_idx] in child:
                p2_idx += 1
            child[i] = parent2[p2_idx]
    return child

def solve_tsp_cso(dist_matrix, num_chickens=30, iterations=150, G=10, r_ratio=0.2, h_ratio=0.5):
    start_time = time.time()
    num_cities = len(dist_matrix)
    
    # Phân chia số lượng bầy gà theo tỷ lệ
    r_num = max(1, int(num_chickens * r_ratio))     # Số gà trống
    h_num = max(1, int(num_chickens * h_ratio))     # Số gà mái
    c_num = num_chickens - r_num - h_num            # Số gà con
    
    # Khởi tạo bầy gà ngẫu nhiên
    swarm = []
    for _ in range(num_chickens):
        route = list(range(num_cities))
        random.shuffle(route)
        swarm.append(route)
        
    best_route = None
    best_cost = float('inf')
    history = []
    
    roosters = []
    hens = []
    chicks = []
    hen_mate = []  # Lưu index gà trống mà gà mái đi theo
    chick_mom = [] # Lưu index gà mẹ mà gà con đi theo
    
    for t in range(iterations):
        # 1. Tính độ thích nghi (Fitness) của từng con gà
        fitness = [(calculate_total_distance(route, dist_matrix), route) for route in swarm]
        fitness.sort(key=lambda x: x[0]) # Sắp xếp từ giỏi đến kém
        
        # Cập nhật gà xuất sắc nhất
        if fitness[0][0] < best_cost:
            best_cost = fitness[0][0]
            best_route = fitness[0][1][:]
            
        # 2. Chu kỳ cập nhật phân cấp (Học hỏi từ code của bạn)
        if t % G == 0:
            roosters = [f[1] for f in fitness[:r_num]]
            hens = [f[1] for f in fitness[r_num:r_num+h_num]]
            chicks = [f[1] for f in fitness[r_num+h_num:]]
            
            # Phân công: Gà mái nào theo gà trống nào, gà con nào theo gà mẹ nào
            hen_mate = [random.choice(roosters) for _ in range(h_num)]
            chick_mom = [random.choice(hens) for _ in range(c_num)]
            
        new_swarm = []
        
        # 3. Di chuyển đàn gà (Đã dịch sang tối ưu rời rạc TSP)
        
        # - Gà trống đi tìm mồi (Tráo đổi 2 điểm - Local search)
        for r in roosters:
            new_r = r[:]
            i, j = random.sample(range(num_cities), 2)
            new_r[i], new_r[j] = new_r[j], new_r[i]
            # Gà trống chỉ bước đi nếu chỗ mới nhiều thức ăn hơn (Fitness tốt hơn)
            if calculate_total_distance(new_r, dist_matrix) < calculate_total_distance(r, dist_matrix):
                new_swarm.append(new_r)
            else:
                new_swarm.append(r)
                
        # - Gà mái đi theo gà trống (Dùng Crossover bắt chước đường đi)
        for idx, h in enumerate(hens):
            target_rooster = hen_mate[idx] # Đi theo con gà trống đã được phân công
            new_h = crossover(h, target_rooster)
            new_swarm.append(new_h)
            
        # - Gà con lon ton theo mẹ (Đột biến hoán đổi vị trí từ lộ trình của mẹ)
        for idx, c in enumerate(chicks):
            mother_hen = chick_mom[idx]    # Bám theo con gà mẹ đã được phân công
            new_c = mother_hen[:]
            i, j = random.sample(range(num_cities), 2)
            new_c[i], new_c[j] = new_c[j], new_c[i] # Gà con chạy lăng xăng quanh mẹ
            new_swarm.append(new_c)
            
        # Cập nhật lại bầy đàn cho thế hệ tiếp theo
        swarm = new_swarm
        history.append((best_route[:], best_cost))
        
    exec_time = time.time() - start_time
    return best_route, best_cost, history, exec_time
