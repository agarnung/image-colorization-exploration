import cv2
import numpy as np
import argparse

def laplacian(img):
    kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    return cv2.filter2D(img, -1, kernel)

# Mayor lambda: más difusión y más rapida
# alpha: paso de descenso gradiente, muy grande causa inestabilidad
# gamma: mayor, menos difusión (bordes más nítidos)
#def variational_colorization(l_channel, ab_hint, mask, lambda_=100, gamma=0.0001, alpha=0.001, iterations=10000):
def variational_colorization(l_channel, ab_hint, mask, lambda_=100, gamma=0.0001, alpha=0.0001, iterations=2000):
    a_channel = ab_hint[:, :, 0].astype(np.float32)
    b_channel = ab_hint[:, :, 1].astype(np.float32)
    mask = mask.astype(np.float32)
    
    for i in range(iterations):
        laplacian_a = laplacian(a_channel)
        laplacian_b = laplacian(b_channel)
        
        a_update = alpha * (lambda_ * laplacian_a - gamma * (a_channel - ab_hint[:, :, 0]))
        b_update = alpha * (lambda_ * laplacian_b - gamma * (b_channel - ab_hint[:, :, 1]))
        
        # Opción 1: No imponer las condiciones de contorno en cada iteración
        a_channel = a_channel + a_update
        b_channel = b_channel + b_update
        
        # Opción 2: imposición de condiciones de contorno en cada iteración
        #a_channel = (1 - mask) * (a_channel + a_update) + mask * ab_hint[:, :, 0]
        #b_channel = (1 - mask) * (b_channel + b_update) + mask * ab_hint[:, :, 1]
        
        # Aplicar clamp para mantener los valores dentro del rango [-128, 127]
        a_channel = np.clip(a_channel, -128, 127)
        b_channel = np.clip(b_channel, -128, 127)
        
        # Visualización en tiempo real cada 10 iteraciones
        if i % 10 == 0:
            a_uint8 = (a_channel + 128).astype(np.uint8)
            b_uint8 = (b_channel + 128).astype(np.uint8)
            lab_colorized = np.stack([l_channel, a_uint8, b_uint8], axis=-1)
            colorized_image = cv2.cvtColor(lab_colorized, cv2.COLOR_Lab2BGR)
            cv2.imshow("Colorized Image (Evolution)", colorized_image)
            cv2.waitKey(1)  # Espera 1 ms para actualizar la ventana
    
    a_uint8 = (a_channel + 128).astype(np.uint8)
    b_uint8 = (b_channel + 128).astype(np.uint8)
    return a_uint8, b_uint8

def load_mask_as_lab(mask_path, target_shape):
    mask = cv2.imread(mask_path, cv2.IMREAD_COLOR)
    mask = cv2.resize(mask, (target_shape[1], target_shape[0]))
    lab_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2Lab)
    ab_hint = lab_mask[:, :, 1:].astype(np.float32) - 128.0  # Ajuste de rango
    mask_combined = (np.abs(ab_hint[:, :, 0]) > 1e-3) | (np.abs(ab_hint[:, :, 1]) > 1e-3)
    mask = mask_combined.astype(np.float32)
    return ab_hint, mask

def colorize_image(image_path, mask_path, output_path):
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    mask_rgb = cv2.imread(mask_path, cv2.IMREAD_COLOR)

    # Redimensionamos la imagen de escala de grises
    l_channel = cv2.resize(gray_image, (512, 512)).astype(np.uint8)  # L en 0-255
    mask_rgb = cv2.resize(mask_rgb, (512, 512))  # Ajustamos el tamaño de la máscara

    # Creamos una versión en 3 canales de la imagen en escala de grises
    gray_3channel = cv2.cvtColor(l_channel, cv2.COLOR_GRAY2BGR)

    # Creamos la máscara combinada: los píxeles que no sean (0,0,0) en la máscara sobrescriben la imagen gris
    mask_binary = np.any(mask_rgb != [0, 0, 0], axis=-1)  # Detectar píxeles no negros
    maskcombined = gray_3channel.copy()
    maskcombined[mask_binary] = mask_rgb[mask_binary]  # Sobreescribimos solo donde la máscara no es negra

    # Aquí deberías definir `load_mask_as_lab` y `variational_colorization`
    ab_hint, mask = load_mask_as_lab(mask_path, l_channel.shape)
    a_colorized, b_colorized = variational_colorization(l_channel, ab_hint, mask)

    # Convertimos la imagen a color usando el modelo Lab
    lab_colorized = np.stack([l_channel, a_colorized, b_colorized], axis=-1)
    colorized_image = cv2.cvtColor(lab_colorized, cv2.COLOR_Lab2BGR)

    # Guardamos la imagen final
    cv2.imwrite(output_path, colorized_image)

    # Mostramos las imágenes
    cv2.imshow("Mask Combined", maskcombined)
    cv2.imshow("Final Colorized Image", colorized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Colorización variacional de imágenes')
    parser.add_argument('--input', required=True, help='Ruta de la imagen en escala de grises')
    parser.add_argument('--mask', required=True, help='Ruta de la máscara de color')
    parser.add_argument('--output', required=True, help='Ruta de salida para la imagen colorizada')
    
    args = parser.parse_args()
    
    colorize_image(args.input, args.mask, args.output)
