import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Circle


def make_img_list(path, prefix, suffix, number_of_images):
    imgs = []
    before = path + prefix
    
    for i in range(0, number_of_images):
        complete = before + str(i) + suffix
        img = mpimg.imread(complete)
        imgs.append(img)
        
    return imgs


def make_cropped_list(img_list, ystart, ystop):
    
    cropped_list = []
    
    for img in img_list:
        strip = img[ystart:ystop, :, :]
        cropped_list.append(strip)
    
    return cropped_list


def make_debug_imgs(img_list, birds_eye):
    debug_raw_imgs, debug_sky_imgs = [], []
    
    for img in img_list:
        
        raw_img = birds_eye.debug_raw(img)
        sky_img = birds_eye.debug_skyview(img)
        
        debug_raw_imgs.append(raw_img)
        debug_sky_imgs.append(sky_img)
    
    return debug_raw_imgs, debug_sky_imgs


def plot_three_images(img1, img2, img3, w, h):
    fig = plt.figure(figsize=(w,h))
    plt.subplot(131)
    plt.imshow(img1)
    plt.subplot(132)
    plt.imshow(img2)
    plt.subplot(133)
    plt.imshow(img3)
    

def plot_six_images(img1, img2, img3, img4, img5, img6, w=17, h=10):
    fig = plt.figure(figsize=(w,h))
    plt.subplot(231)
    plt.imshow(img1)
    plt.subplot(232)
    plt.imshow(img2)
    plt.subplot(233)
    plt.imshow(img3)
    plt.subplot(234)
    plt.imshow(img4)
    plt.subplot(235)
    plt.imshow(img5)
    plt.subplot(236)
    plt.imshow(img6)


def show_dotted_image(this_image, points, thickness = 1, color = [0, 0, 0], d = 3):
    
    image = this_image.copy()
    
    cv2.line(image, points[0], points[1], color, thickness)
    cv2.line(image, points[2], points[3], color, thickness)
    
    fig, ax = plt.subplots(1)
    
    ax.set_aspect('equal')
    ax.imshow(image)
    
    for (x, y) in points:
        dot = Circle((x, y), d)
        dot.set_facecolor(color)
        ax.add_patch(dot)

        
def make_debug_image(this_image, points, thickness = 1, color = [0, 0, 0], r = 6):

    image = this_image.copy()
    
    cv2.line(image, points[0], points[1], color, thickness)
    cv2.line(image, points[2], points[3], color, thickness)
    
    for point in points: 
        cv2.circle(image, point, r, color, -1)

    return image


class BirdsEye(object):
    
    def __init__(self,source_points, dest_points):
        self.spoints = source_points
        self.dpoints = dest_points
        
        src_points = np.array(source_points, np.float32)
        dest_points = np.array(dest_points, np.float32)

        self.warp_matrix = cv2.getPerspectiveTransform(src_points, dest_points)
        
        # Use this matrix to warp img from sky perspective to vehicle perspective
        #self.inv_warp_matrix = cv2.getPerspectiveTransform(dest_points, src_points)

    def skyview(self, img):
        shape = (img.shape[1], img.shape[0])
        warp_img = cv2.warpPerspective(img, self.warp_matrix, shape, flags = cv2.INTER_LINEAR)
        return warp_img
    
    def debug_skyview(self, img):
        warped_img = self.skyview(img)
        img = make_debug_image(warped_img, self.dpoints)
        return img

    def debug_raw(self, img):
        return make_debug_image(img, self.spoints)

    def show_raw_dotted(self, img):
        show_dotted_image(img, self.spoints)
    
    def show_skyview_dotted(self, img):
        warped_img = self.skyview(img)
        show_dotted_image(warped_img, self.dpoints)
        
        
def compare_birdseye(birdseye, img):
    birdseye.show_raw_dotted(img)
    birdseye.show_skyview_dotted(img)
    plt.show()