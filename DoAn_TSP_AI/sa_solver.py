import math
import random
import time
from tsp_utils import calculate_total_distance

def solve_tsp_sa(dist_matrix, initial_temp=1000, cooling_rate=0.99, min_temp=0.1):
    start_time = time.time()
    num_cities = len(dist_matrix)
    
    current_route = list(range(num_cities))
    random.shuffle(current_route)
    current_cost = calculate_total_distance(current_route, dist_matrix)
    
    best_route = current_route[:]
    best_cost = current_cost
    history = [] # Lưu trữ cả đường đi và chi phí để vẽ Animation
    
    temp = initial_temp
    while temp > min_temp:
        neighbor = current_route[:]
        i, j = random.sample(range(num_cities), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        
        neighbor_cost = calculate_total_distance(neighbor, dist_matrix)
        delta = neighbor_cost - current_cost
        
        if delta < 0 or random.random() < math.exp(-delta / temp):
            current_route = neighbor[:]
            current_cost = neighbor_cost
            
            if current_cost < best_cost:
                best_route = current_route[:]
                best_cost = current_cost
        
        # Lưu lại trạng thái tốt nhất của vòng lặp này
        history.append((best_route[:], best_cost))
        temp *= cooling_rate
        
    exec_time = time.time() - start_time
    return best_route, best_cost, history, exec_time