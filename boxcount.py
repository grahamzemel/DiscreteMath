import numpy as np
import matplotlib.pyplot as plt

def box_count(image, box_size):
    count = 0
    for i in range(0, image.shape[0], box_size):
        for j in range(0, image.shape[1], box_size):
            if np.sum(image[i:i+box_size, j:j+box_size]) > 0:
                count += 1
    print(count)
    return count

def fractal_dimension(image):
    sizes = 2**np.arange(0, int(np.log2(min(image.shape[:2]))))
    print(sizes)
    counts = []
    for size in sizes:
        counts.append(box_count(image, size))
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return -coeffs[0]

# Example usage
# image = np.random.randint(0, 2, size=(512, 512))
image = plt.imread("fractal.png")
fd = fractal_dimension(image)
print("Fractal dimension:", fd)