import cv2
import numpy as np

def laplacian(img):
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    return cv2.filter2D(img, -1, kernel)

def variational_colorization(l_channel, ab_hint, mask, lambda_=50, gamma=100, alpha=0.1, iterations=200):
    a_channel = ab_hint[:, :, 0].astype(np.float32)
    b_channel = ab_hint[:, :, 1].astype(np.float32)
    mask = (mask > 0).astype(np.float32)  # Crear una máscara binaria
    
    for _ in range(iterations):
        laplacian_a = laplacian(a_channel)
        laplacian_b = laplacian(b_channel)
        
        a_update = alpha * (lambda_ * laplacian_a - gamma * (a_channel - ab_hint[:, :, 0]))
        b_update = alpha * (lambda_ * laplacian_b - gamma * (b_channel - ab_hint[:, :, 1]))
        
        a_channel = (1 - mask) * (a_channel + a_update) + mask * ab_hint[:, :, 0]
        b_channel = (1 - mask) * (b_channel + b_update) + mask * ab_hint[:, :, 1]
        
        a_channel = np.clip(a_channel, -128, 127)
        b_channel = np.clip(b_channel, -128, 127)
    
    return a_channel.astype(np.uint8), b_channel.astype(np.uint8)

def load_mask_as_lab(mask_path, target_shape):
    mask = cv2.imread(mask_path, cv2.IMREAD_COLOR)
    mask = cv2.resize(mask, (target_shape[1], target_shape[0]))
    lab_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2Lab)
    mask_gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)  # Para definir las zonas coloreadas
    return lab_mask[:, :, 1:].astype(np.float32), mask_gray

def colorize_image(image_path, mask_path, output_path):
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    mask_rgb = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
    l_channel = cv2.resize(gray_image, (512, 512)).astype(np.float32)
    
    ab_hint, mask = load_mask_as_lab(mask_path, l_channel.shape)
    a_colorized, b_colorized = variational_colorization(l_channel, ab_hint, mask)
    
    lab_colorized = np.stack([l_channel, a_colorized, b_colorized], axis=-1).astype(np.uint8)
    colorized_image = cv2.cvtColor(lab_colorized, cv2.COLOR_Lab2BGR)

    cv2.imwrite(output_path, colorized_image)
    cv2.imshow("Original Image", gray_image)
    cv2.imshow("Mask", mask_rgb)
    cv2.imshow("Colorized Image", colorized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_path = "./peppers512.png"
    mask_path = "./mask.png"
    output_path = "./colorized_result.png"
    colorize_image(image_path, mask_path, output_path)

