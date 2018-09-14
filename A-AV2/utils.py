import pandas as pd
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

class DataFrame(object):
    def __init__(self, my_csv_file):
        self.csv_file = my_csv_file 
        self.data = pd.read_csv(self.csv_file)
        self.num = len(self.data)
        self.print_info()
    
    def print_info(self):
        print()
        print("csv filepath: ", self.csv_file)
        print("number of images: ", self.num)
        print("sample data: ")
        print(self.data.head())
        print()

    def distribution(self, my_bins):
        self.data.hist(bins=my_bins)
        
    def get_image(self, index):
        return mpimg.imread(self.data['NAME'][index])
    
    def get_steer(self, index):
        return self.data['STEER'][index]
            

def plot_three_images(img1, img2, img3, w, h):
    fig = plt.figure(figsize=(w,h))
    plt.subplot(131)
    plt.imshow(img1)
    plt.subplot(132)
    plt.imshow(img2)
    plt.subplot(133)
    plt.imshow(img3)