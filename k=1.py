# -*- coding: utf-8 -*-
"""K=1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11jeAq6FS22vCdMmdSNexy3-EFrV9o6LY
"""

from google.colab.patches import cv2_imshow
import numpy as np
import cv2
import pywt

# set the gain factor for embedding
k = 1

# read in the cover object
file_name = '/content/drive/MyDrive/Lena.jpg'
cover_object = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

#display Cover Image
print("Cover image".title())
cv2_imshow( cover_object)

# determine size of watermarked image
Mc, Nc = cover_object.shape

# read in the message image and reshape it into a vector
file_name = '/content/drive/MyDrive/Watermark_obj.jpeg'
message = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

#display Watermark Object
print("WaterObject object".title())
cv2_imshow( message)

Mm, Nm = message.shape
message_vector = np.round(np.reshape(message, (Mm*Nm, 1)) / 256)

# Calculate Dwt cofficients
coeffs = pywt.dwt2(cover_object, 'haar')
cA1, (cH1, cV1, cD1) = coeffs

# add pn sequences to H1 and V1 componants when message = 0
for kk in range(len(message_vector)):
    pn_sequence_h = np.round(2 * (np.random.rand(Mc//2, Nc//2) - 0.5))
    pn_sequence_v = np.round(2 * (np.random.rand(Mc//2, Nc//2) - 0.5))
    if message_vector[kk] == 0:
        cH1 += k * pn_sequence_h
        cV1 += k * pn_sequence_v

# perform IDWT
watermarked_image = pywt.idwt2((cA1, (cH1, cV1, cD1)), 'haar')

# convert back to uint8
watermarked_image_uint8 = np.uint8(watermarked_image)

# write watermarked image to file
cv2.imwrite('dwt_watermarked.jpg', watermarked_image_uint8)

# display watermarked image
print("Watermarked image".title())
cv2_imshow( watermarked_image_uint8)
cv2.waitKey(0)
cv2.destroyAllWindows()

type(watermarked_image)
watermarked_image.shape

import numpy as np
import cv2
from skimage.metrics import structural_similarity as compare_ssim
# save start time
start_time = cv2.getTickCount()

# read in the watermarked object
file_name = 'dwt_watermarked.jpg'
watermarked_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE).astype(float)

# determine size of watermarked image
Mw, Nw = watermarked_image.shape

# read in original watermark
file_name = '/content/drive/MyDrive/Watermark_obj.jpeg'
orig_watermark = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE).astype(float)

# determine size of original watermark
Mo, No = orig_watermark.shape

# initialize message to all ones
message_vector = np.ones((Mo * No,))

# apply DWT to the watermarked image
coeffs = pywt.dwt2(watermarked_image, 'haar')
cA1, (cH1, cV1, cD1) = coeffs

# add pn sequences to H1 and V1 components
correlation = np.zeros((Mo * No,))
for kk in range(len(message_vector)):
    pn_sequence_h = np.round(2 * (np.random.rand(Mw // 2, Nw // 2) - 0.5))
    pn_sequence_v = np.round(2 * (np.random.rand(Mw // 2, Nw // 2) - 0.5))
    correlation_h = np.corrcoef(cH1.flatten(), pn_sequence_h.flatten())[0, 1]
    correlation_v = np.corrcoef(cV1.flatten(), pn_sequence_v.flatten())[0, 1]
    correlation[kk] = (correlation_h + correlation_v) / 2

# recover message from correlations
for kk in range(len(message_vector)):
    if correlation[kk] > np.mean(correlation):
        message_vector[kk] = 0

# reshape the message vector and display recovered watermark
message = np.reshape(message_vector, (Mo, No))
cv2_imshow(message)
cv2.waitKey(0)
cv2.destroyAllWindows()

# display processing time
elapsed_time = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
print('Elapsed time: {:.2f} s'.format(elapsed_time))

# calculate similarity of two images
X = cv2.imread('/content/drive/MyDrive/Watermark_obj.jpeg', cv2.IMREAD_GRAYSCALE)
Y = message.astype(np.uint8)
ssim = compare_ssim(X, Y)
psnr = cv2.PSNR(X, Y)
print('SSIM: {:.4f}, PSNR: {:.4f}'.format(ssim, psnr))

import numpy as np

def Acc_rate(X,Y):
    X = np.double(X)
    Y = np.double(Y)
    H1, W1 = X.shape[:2]
    H2, W2 = Y.shape[:2]
    np = 0
    np1 = 0
    np2 = 0
    np3 = 0
    count_Or = 0
    count_Ex = 0
    for i in range(H1):
        if (X[i]>=1):
            np = np+1
        else:
            np = np
        for j in range(W1):
            if (X[j]>=1):
                np1 = np1+1
            else:
                np1 = np1
    count_Or = np+np1
    for i in range(H2):
        if (Y[i]>=1):
            np2 = np2+1
        else:
            np2 = np2
        for j in range(W2):
            if (Y[j]>=1):
                np3 = np3+1
            else:
                np3 = np3
    count_Ex = np2+np3
    AR = (count_Ex/count_Or)*100
    return AR

import numpy as np

def psnr(image, image_prime, M, N):
    # convert to floats
    image = image.astype(float)
    image_prime = image_prime.astype(float)

    # check for identical images
    if np.array_equal(image, image_prime):
        raise ValueError("Input images must not be identical")

    # calculate MSE
    mse = np.sum(np.square(image - image_prime)) / (M * N)

    # calculate PSNR
    psnr = 10 * np.log10(255**2 / mse)

    return psnr

import cv2
import numpy as np

# Read in the images
X = cv2.imread('/content/drive/MyDrive/Lena.jpg')
Y = cv2.imread('dwt_watermarked.jpg')

# Convert the images to grayscale
X = cv2.cvtColor(X, cv2.COLOR_RGB2GRAY)
Y = cv2.cvtColor(Y, cv2.COLOR_RGB2GRAY)

# Calculate the correlation coefficient
I = np.corrcoef(X.ravel(), Y.ravel())[0, 1]

# Calculate the standard deviation
I1 = np.std(I)

print(I)
print(I1)