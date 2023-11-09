# BEGIN: 8j3d9fj3d9fj
import cv2
import numpy as np
import os

def localize_artwork(image):
    

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply adaptive thresholding to segment the image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the largest area
    max_area = 0
    max_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    # Get the bounding box of the contour
    x, y, w, h = cv2.boundingRect(max_contour)

    # Get the corners of the bounding box
    corners = np.float32([[x, y], [x + w, y], [x, y + h], [x + w, y + h]])

    # Define the desired output size of the warped image
    output_size = (w, h)

    # Define the desired output corners of the warped image
    output_corners = np.float32([[0, 0], [output_size[0], 0], [0, output_size[1]], [output_size[0], output_size[1]]])

    # Get the perspective transformation matrix
    M = cv2.getPerspectiveTransform(corners, output_corners)

    # Warp the image to a top-down view
    warped = cv2.warpPerspective(image, M, output_size)

    return warped

def match_artwork(warped_artwork, database_path):
    # Load the database images into memory
    database_images = []
    database_title=[]
    for root, dirs, files in os.walk(database_path):
        for filename in files:
            print(root+"/"+filename)
            #image_path = os.path.join(database_path, filename)
            image = cv2.imread(root+"/"+filename)
            database_images.append(image)
            title=filename.split("_")[1]
            title=title.split(".")[0]
            new_string = title.replace("-", " ")
            print(new_string)
            database_title.append(new_string)


    '''
    # Compute keypoints and descriptors for the warped artwork image
    gray = cv2.cvtColor(warped_artwork, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    
    # Match descriptors with each database image
    matcher = cv2.FlannBasedMatcher_create()
    best_match_distance = float('inf')
    best_match_index = -1
    for i, descriptors_db in enumerate(database_descriptors):
        matches = matcher.match(descriptors_db, descriptors)
        distance = sum([match.distance for match in matches])
        if distance < best_match_distance:
            
            best_match_distance = distance
            best_match_index = i
            print("best_match_index",best_match_index)
            cv2.imshow('Image', database_images[best_match_index])

            # Wait for 1 second
            cv2.waitKey(1000)

            # Close the window
            cv2.destroyAllWindows()
            
    # Return the best match image
    return database_images[best_match_index]
    '''
    detector = cv2.SIFT_create()
    extractor = cv2.SIFT_create()
    database_keypoints = []
    database_descriptors = []
    for image in database_images:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints, descriptors = detector.detectAndCompute(gray, None)
        database_keypoints.append(keypoints)
        database_descriptors.append(descriptors)

    # Compute keypoints and descriptors for the warped artwork image
    gray = cv2.cvtColor(warped_artwork, cv2.COLOR_BGR2GRAY)
    keypoints, descriptors = detector.detectAndCompute(gray, None)

    # Match descriptors with each database image
    matcher = cv2.FlannBasedMatcher_create()
    best_match_distance = float('inf')
    best_match_index = -1
    for i, descriptors_db in enumerate(database_descriptors):
        matches = matcher.match(descriptors_db, descriptors)
        distance = sum([match.distance for match in matches])
        if distance < best_match_distance:
            best_match_distance = distance
            best_match_index = i
            print("best_match_index",best_match_index)
            #cv2.imshow('Image', database_images[best_match_index])

            # Wait for 1 second
            #cv2.waitKey(1000)

            # Close the window
            #cv2.destroyAllWindows()

    # Return the best match image
    return database_images[best_match_index],database_title[best_match_index]
    

# Example usage
image_path = '/home/monica/repositories/opencv_challenge/IMG_20231109_125348.jpg'

#image_path="/media/monica/One Touch/dataset_art/wikiart/Art_Nouveau_Modern/sample/a.y.-jackson_skeena-crossing-1926.jpg"
image = cv2.imread(image_path)

# Get the original image dimensions
height, width = image.shape[:2]

# Set the desired width
new_width = 640

# Calculate the scaling factor
scale_factor = new_width / width

# Calculate the new height
new_height = int(height * scale_factor)

# Resize the image while maintaining its aspect ratio
resized_image = cv2.resize(image, (new_width, new_height))
'''
# Display the resized image
cv2.imshow('Resized Image', resized_image)
cv2.waitKey(1000)
cv2.destroyAllWindows()
'''
warped_artwork = localize_artwork(resized_image)

cv2.imshow('warped_artwork', warped_artwork)
cv2.waitKey(1000)
cv2.destroyAllWindows()
#cv2.imshow('warped_artwork', warped_artwork)
#cv2.waitKey(0)
best_match = match_artwork(warped_artwork, '/media/monica/One Touch/dataset_art/wikiart/Art_Nouveau_Modern/sample')

print(best_match[1])
cv2.imshow('Best Match', best_match[0])
# Wait for 1 second
cv2.waitKey(3000)

# Close the window
cv2.destroyAllWindows()

