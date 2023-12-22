def is_polygon_closed(points):
    # Kiểm tra xem danh sách điểm tạo thành một đa giác kín hay không
    # Để đa giác là kín, điểm đầu tiên và điểm cuối cùng phải trùng nhau
    return points[0] == points[-1]

def is_point_inside_polygon(points, point):
    # Kiểm tra xem điểm A có nằm trong đa giác hay không
    # Sử dụng thuật toán kiểm tra điểm trong đa giác
    n = len(points)
    inside = False
    p1x, p1y = points[0]
    for i in range(n+1):
        p2x, p2y = points[i % n]
        if point[1] > min(p1y, p2y):
            if point[1] <= max(p1y, p2y):
                if point[0] <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (point[1]-p1y) * (p2x-p1x) / (p2y-p1y) + p1x
                        if p1x == p2x or point[0] <= xinters:
                            inside = not inside
        p1x, p1y = p2x, p2y
    return inside

# Đọc thông tin từ tệp dữ liệu
with open("BAI02.INP", "r") as file:
    lines = file.readlines()
    line1 = lines[0].strip()
    line2 = lines[1].strip()

# Chuyển đổi thông tin thành danh sách các điểm và tọa độ điểm A
points = [tuple(map(float, point.split(','))) for point in line1.split()]
pointA = tuple(map(float, line2.split(',')))
def r():
    # Kiểm tra và ghi kết quả vào tệp kết quả
    with open("BAI02.OUT", "w") as file:
        if is_polygon_closed(points):
            file.write("1\n")
            if is_point_inside_polygon(points, pointA):
                file.write("1\n")
            else:
                file.write("0\n")
        else:
            file.write("0\n0\n")