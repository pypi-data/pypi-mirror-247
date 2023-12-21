import cv2
from pathlib import Path

def check_image_conditions(image_path):
    try:
        # Đọc ảnh từ tệp đầu vào
        img = cv2.imread(image_path)

        # Kiểm tra kích thước tệp đầu vào
        file_size = Path(image_path).stat().st_size
        if file_size/1024 <= 500:
            return -1

        # Detect khuôn mặt trong ảnh
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(200, 200))

        # Kiểm tra số lượng khuôn mặt trong ảnh
        if len(faces) != 1:
            return -2

        # Kiểm tra kích thước khuôn mặt
        (x, y, w, h) = faces[0]
        if w < 200 or h < 200:
            return -3

        # Tất cả điều kiện đều đúng
        return 0

    except:
        # Lỗi khi đọc hoặc xử lý ảnh
        return -1

# Đường dẫn tệp ảnh đầu vào
image_path = "BAI03.PNG"

def r():
    # Kiểm tra và ghi kết quả vào tệp kết quả
    result = check_image_conditions(image_path)
    with open("BAI03.OUT", "w") as file:
        file.write(str(result))