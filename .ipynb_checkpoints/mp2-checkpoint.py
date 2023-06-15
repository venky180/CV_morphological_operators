from PIL import Image
import numpy as np
files = ["palm.bmp","gun.bmp"]
def dialation(p,kernel_size,padd,kernel):
    # This function performs dilation operation on an image
    # Inputs:
    # - p: image to perform dilation on
    # - kernel_size: size of the kernel to use for dilation
    # - padd: amount of padding to apply to the image before performing dilation
    # - kernel: the kernel to use for dilation
    # Outputs:
    # - p: the dilated image
    # - count: the number of pixels in the image that were changed during dilation
    p=np.pad(p,(padd,padd), 'constant', constant_values=(0))
    count=0
    for i in range(padd-1,p.shape[0]-padd):
        for j in range(padd-1,p.shape[1]-padd):
            filter_kernel = 0
            for k in range(kernel_size):
                for l in range(kernel_size):
                    if kernel[k,l] == p[i-padd+1+k,j-padd+1+l]:
                        filter_kernel = 1
                        break
            if filter_kernel == 1:
                p[i,j] = 255
                count+=1
            else:
                p[i,j] = 0
    print(count)
    return p

# This function performs erosion operation on a binary image represented by p using a kernel of size kernel_size. 
# padd specifies the padding required for the image. The function counts the number of times the kernel can fit into 
# the image such that all the pixels of the kernel overlap with the corresponding pixels of the image, and sets the central
# pixel of the kernel to 1 if all the pixels of the kernel overlap with the corresponding pixels of the image, otherwise sets 
# it to 0. The function returns the eroded binary image.

def erosion(p,kernel_size,padd,kernel):
    unique, counts = np.unique(np.array(kernel), return_counts=True)
    ones=dict(zip(unique, counts))
    kernel_ones=ones[1]
    p=np.pad(p,(padd-1,padd-1), 'constant', constant_values=(0))
    count=0
    for i in range(padd-1,p.shape[0]-padd):
        for j in range(padd-1,p.shape[1]-padd):
            filter_kernel = 0
            for k in range(kernel_size):
                for l in range(kernel_size):
                    if kernel[k,l] == p[i-padd+1+k,j-padd+1+l]:
                        filter_kernel += 1
            if filter_kernel == kernel_ones:
                p[i,j] = 1
                count+=1
            else:
                p[i,j] = 0
    print(count)
    return p



def opening(p):
    kernel_size=5
    padd=int((kernel_size+1)/2)
    kernel = np.array([[1,1,1,1,1], [1,0,1,0,0],  [0,1,1,0,0], [0,0,0,0,0],  [0,0,0,0,0]])
    # kernel = np.ones((kernel_size,kernel_size),dtype=int)
    p1=erosion(p,kernel_size,padd,kernel)
    
    kernel_size=5
    padd=int((kernel_size+1)/2)
    kernel = np.ones((kernel_size,kernel_size),dtype=int)
    p2=dialation(p1,kernel_size,padd,kernel)
    return p2

def closing(p):
    kernel_size=13
    padd=int((kernel_size+1)/2)
    kernel = np.ones((kernel_size,kernel_size),dtype=int)
    # kernel = np.array([[0,1,0],[1,0,1],[0,1,0]])
    p1=dialation(p,kernel_size,padd,kernel)
    
    kernel_size=3
    padd=int((kernel_size+1)/2)
    # kernel = np.array([[1,1,1,1,1], [1,0,1,0,0],  [1,0,1,0,0], [0,0,0,0,0],  [0,0,0,0,0]])
    kernel = np.array([[1,1,0],[0,1,0],[0,0,0]])
    p2=erosion(p1,kernel_size,padd,kernel)
    return p2

def boundary_following(image):
    boundaries = []
    visited = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i, j] and not visited[i, j]:
                boundary = []
                current_pixel = (i, j)
                direction = (-1, 0) 
                while current_pixel != (i, j) or not boundary:
                    boundary.append(current_pixel)
                    visited[current_pixel] = 1
                    k = None
                    for l in range(8):
                        next_pixel = (current_pixel[0] + direction[0], current_pixel[1] + direction[1])
                        if (0 <= next_pixel[0] < image.shape[0]) and (0 <= next_pixel[1] < image.shape[1]) and image[next_pixel] and not visited[next_pixel]:
                            k = l
                            break
                        direction = (direction[1], -direction[0]) # Rotate direction counterclockwise
                    current_pixel = (current_pixel[0] + direction[0], current_pixel[1] + direction[1])
                    direction = (direction[1], -direction[0]) # Rotate direction counterclockwise
                    if k is not None:
                        direction = (direction[0], direction[1]) # Rotate direction clockwise k times
                boundaries.append(boundary)
                boundary_image = np.zeros_like(image)
                for pixel in boundary:
                    boundary_image[pixel] = 1
                boundary_image = 1 - boundary_image
                boundary_image = Image.fromarray(np.uint8(boundary_image * 255), mode='L')
                filen = "ero-"+file+".png"
                boundary_image.save(filen)

    return boundaries

for file in files:
    im = Image.open(file)
    p = np.array(im)
    p=p.astype(int)
    p=closing(p)
    p[p==1]=255
    img = Image.fromarray(p.astype(np.uint8))
    filen = "clo-"+file+".png"
    img.save(filen)
    
for file in files:
    kernel_size=7
    padd=int((kernel_size+1)/2)
    kernel = np.ones((kernel_size,kernel_size),dtype=int)
    # kernel = np.array([[0,1,0],[0,1,0],[0,1,0]])
    im = Image.open(file)
    p = np.array(im)
    p=p.astype(int)
    p=dialation(p,kernel_size,padd,kernel)
    p[p==1]=255
    img = Image.fromarray(p.astype(np.uint8))
    filen = "dia-"+file+".png"
    img.save(filen)
    

for file in files:
    im = Image.open(file)
    p = np.array(im)
    p=p.astype(int)
    p=opening(p)
    p[p==1]=255
    img = Image.fromarray(p.astype(np.uint8))
    filen = "ope-"+file+".png"
    img.save(filen)
    
for file in files:
    kernel_size=5
    padd=int((kernel_size+1)/2)
    kernel = np.array([[1,1,1,1,1], [1,0,1,0,0],  [1,0,1,0,0], [0,0,0,0,0],  [0,0,0,0,0]])
    # kernel = np.array([[1,1,1,1,1], [0,0,0,0,0],  [0,0,0,0,0], [0,0,0,0,0],  [0,0,0,0,0]])
    # kernel = np.array([[1,1,1,1,1], [0,0,0,0,0],  [0,0,0,0,0], [0,0,0,0,0],  [0,0,0,0,0]])
    # kernel = np.array([[1,1,1,1,1], [0,0,0,0,0],  [0,0,0,0,0], [0,0,0,0,0],  [0,0,0,0,0]])
    im = Image.open(file)
    p = np.array(im)
    p=p.astype(int)
    p=erosion(p,kernel_size,padd,kernel)
    p[p==1]=255
    img = Image.fromarray(p.astype(np.uint8))
    filen = "ero-"+file+".png"
    img.save(filen)
    
files = ["clo-palm.bmp.png","cl-gun.bmp.png"]
for file in files:
    im = Image.open(file)
    p = np.array(im)
    p=p.astype(int)
    b=boundary_following(p,file)