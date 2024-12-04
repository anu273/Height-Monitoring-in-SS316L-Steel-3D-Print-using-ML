import os
import cv2
import csv
import numpy as np
import matplotlib.pyplot as plt 

def extract_object(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    lower_gray = np.array([0], dtype=np.uint8)
    upper_gray = np.array([125], dtype=np.uint8)
    mask_gray = cv2.inRange(gray, lower_gray, upper_gray)

    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    _, thresholded = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)
    bright = cv2.countNonZero(thresholded)
    
    if bright>0:
    # Find contours in the binary mask
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Identify the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
    # Mask for the largest contour
        mask_white = np.zeros_like(gray)
        cv2.drawContours(mask_white, [largest_contour], -1, 255, cv2.FILLED)
    
    else:
        mask_white = cv2.inRange(gray, lower_gray, upper_gray)

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lower_lab = np.array([100,168,50])
    upper_lab = np.array([200,250, 150])
    mask_lab = cv2.inRange(lab, lower_lab, upper_lab)

    lower_bound = np.array([0, 0, 0])  # R, G, B
    upper_bound = np.array([255, 75, 255])
    rgb_mask = cv2.inRange(image, lower_bound, upper_bound)

    # Combine all masks
    combined_mask = cv2.bitwise_or(mask_gray, cv2.bitwise_or(rgb_mask,cv2.bitwise_or(mask_white,mask_lab)))
    extracted_object = cv2.bitwise_and(image, image, mask=combined_mask)

    return extracted_object



def find_extracted_object_height(extracted_object, x_points):
    h = []
    gray = cv2.cvtColor(extracted_object, cv2.COLOR_BGR2GRAY)
    actual_nozzle_length = 13.4 #in mm
    pixel_length = 394
    factor = 13.4/394

    for i in range(len(x_points)):
        x = x_points[i]
        count = cv2.countNonZero(gray[:, x])
        h.append(count*factor)
    return h


def process_files_in_folder(folder_path):
    # Get a list of all images in the folder
    files = os.listdir(folder_path)
    files.sort()
    # Create a list to store file paths
    file_paths = []

    # Process each file
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)

        # Check if the path is a file
        if os.path.isfile(file_path):
            file_paths.append(file_path)
    return file_paths


def is_printing(image):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY)

    bright = cv2.countNonZero(thresholded)
    return bright

def sample_is_right(image):
    img = cv2.imread(image)
    cropped_img = img[600:900,900:1700]
    return cropped_img


def sample_is_left(image):
    img = cv2.imread(image)
    cropped_img = img[300:550,400:1200]
    return cropped_img
     

folder_path = r"C:\Users\anami\Pictures\DC project\P5_10mm"
files_list = process_files_in_folder(folder_path)

x_points = []
n = int(input("heights at n points : "))
for i in range(n):
    x = int(input(f"x{1+i} : "))
    x_points.append(x)

heights = []
layer = []
l = 0
a = 0
h = [0,0]
for i in range(1,len(files_list)):
    image = files_list[i]
    img = cv2.imread(image)
    

    if is_printing(image) > (10**5):
        heights.append(h)
        layer.append(0)
        continue

    else:
        if is_printing(files_list[i-1]) > (10**5):
            l = l+1
            x = x+10
        
        crop = img[480-a:860,350:1500]
        layer.append(l)  
        extracted_object = extract_object(crop)
        extracted_object_height = find_extracted_object_height(extracted_object, x_points)
        heights.append(extracted_object_height)



def write_lists_to_csv(rearranged_lists, filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(rearranged_lists)

output_directory = r"C:\Users\anami\Downloads"# Change this to your desired directory
filename = os.path.join(output_directory, "heights1.csv")
write_lists_to_csv(heights, filename)




#csv_file_path = r"C:\Users\anami\Downloads\Height_3.csv"
#header = ['Layer no.', 'Height']
#data = list(zip(layer, heights))
#Open the CSV file in write mode
#with open(csv_file_path, 'w', newline='') as csv_file:
#    csv_writer = csv.writer(csv_file)

#    csv_writer.writerow(header)

#    csv_writer.writerows(data)
