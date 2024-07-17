import numpy as np
from scipy.linalg import svd
import cv2

def image_tampering_detection(image_path):
    # Bước 1: Phân hoạch ảnh A thành các khối chờm nhau có kích thước 8x8.
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    h, w = img.shape
    blocks = [img[j:j+8, i:i+8] for j in range(0, h, 8) for i in range(0, w, 8)]
    print("Done-1")

    # Bước 2: Áp dụng phép phân tích SVD trên từng khối ảnh 8x8, sau đó lấy một số giá trị đầu tiên trên đường chéo của ma trận s làm các giá trị đặc trưng.
    features = []
    for block in blocks:
        print("Analyzing...")
        U, s, V = svd(block)
        feature = s[:4] # Chỉ lấy 4 giá trị đặc trưng đầu tiên
        features.append(feature)
    print("Done-2")

    # Bước 3: Đặc trưng của mỗi khối được sắp vào thành một hàng của một ma trận, sau đó các hàng được sắp xếp lại theo thứ tự từ điển.
    feature_matrix = np.array(features)
    sorted_features = np.lexsort(feature_matrix.T)
    print("Done-3")

    # Bước 4: Dựa trên các hàng giống nhau, xác định các khối giống nhau tương ứng.
    group_indices = []
    prev_feature = feature_matrix[sorted_features[0]]
    group_indices.append([sorted_features[0]])
    for i in sorted_features[1:]:
        print("Analyzing...")
        if np.array_equal(feature_matrix[i], prev_feature):
            group_indices[-1].append(i)
        else:
            group_indices.append([i])
            prev_feature = feature_matrix[i]
    print("Done-4")
    # Bước 5: Nếu xác định được hai nhóm gổm một số đủ lớn các cặp khối tương ứng giống nhau thì có thể kết luận là ảnh đã bị chỉnh sửa
    tampered = False
    for group in group_indices:
        print("Analyzing...")
        if len(group) >= 8: # Chỉ cần 8 cặp khối giống nhau để kết luận ảnh bị chỉnh sửa
            tampered = True
            break
    print("Done-5")
    return tampered

print(image_tampering_detection('test.jpg'))