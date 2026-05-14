import math
import random


def generate_data(num_cities=15):
    names = []
    # Nếu số lượng yêu cầu nhỏ hơn hoặc bằng danh sách gốc -> Chọn ngẫu nhiên
    for i in range(0, num_cities):
        names.append(f"TP {i+1}")
    random.shuffle(names) # Xáo trộn ngẫu nhiên danh sách tên
    
    # Tạo tọa độ (x, y) và gán tên cho từng thành phố
    cities_data = [(random.uniform(0, 100), random.uniform(0, 100), names[i]) for i in range(num_cities)]
    
    # Tạo ma trận khoảng cách
    dist_matrix = [[0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                # Tính khoảng cách Euclidean
                dist_matrix[i][j] = math.dist((cities_data[i][0], cities_data[i][1]), 
                                              (cities_data[j][0], cities_data[j][1]))
                
    return cities_data, dist_matrix

def calculate_total_distance(route, dist_matrix):
    """
    Hàm Fitness (Đánh giá độ thích nghi):
    Tính tổng quãng đường của một lộ trình dựa trên ma trận khoảng cách.
    """
    total_cost = 0
    for i in range(len(route) - 1):
        total_cost += dist_matrix[route[i]][route[i+1]]
    total_cost += dist_matrix[route[-1]][route[0]]
    return total_cost

def get_distance_matrix_string(cities_data, dist_matrix):
    # Tạo chuỗi text hiển thị ma trận
    matrix_string = "Distance Matrix:\n\t"
    matrix_string += "\t".join(city[2][:5] for city in cities_data) + "\n"
    for i, row in enumerate(dist_matrix):
        matrix_string += cities_data[i][2][:5] + "\t" + "\t".join(f"{dist:.1f}" for dist in row) + "\n"
    return matrix_string

def calculate_total_distance(route, dist_matrix):
    """
    Hàm Fitness (Đánh giá độ thích nghi):
    Tính tổng quãng đường của một lộ trình dựa trên ma trận khoảng cách.
    """
    total_cost = 0
    # Cộng dồn khoảng cách giữa các thành phố liên tiếp
    for i in range(len(route) - 1):
        total_cost += dist_matrix[route[i]][route[i+1]]
    
    # Cộng thêm khoảng cách từ thành phố cuối quay về thành phố đầu (Chu trình)
    total_cost += dist_matrix[route[-1]][route[0]]
    
    return total_cost