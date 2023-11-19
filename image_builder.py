import cv2
import svg_to_png
import util
import numpy as np
import math
import random
import os

# name of the piece
NAME = "16x30"
# the margin kept when cropping an image
CROP_MARGIN = 500


def main():
    # convert to png
    svg_path = f".\\SVGs\\{NAME}.svg"
    png_path = f".\\PNGs\\{NAME}.png"
    try:
        os.mkdir(f".\\outputs\\{NAME}") 
    except FileExistsError:
        pass
    try:
        os.mkdir(f".\\outputs\\{NAME}\\raw") 
    except FileExistsError:
        pass
    try:
        os.mkdir(f".\\outputs\\{NAME}\\divided") 
    except FileExistsError:
        pass
    output_raw_path = f".\\outputs\\{NAME}\\raw\\{NAME}.png"
    output_divided_path = f".\\outputs\\{NAME}\\divided\\"
    svg_to_png.svg_to_png(svg_path,png_path)

    # open the image
    img = cv2.imread(png_path)

    # convert to gray
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # apply threshold
    _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # make it bigger on both sides to allow for better margins
    x = np.shape(img)[1]
    y = np.shape(img)[0]
    temp = np.zeros(shape=(y+2*CROP_MARGIN,x+2*CROP_MARGIN),dtype=img.dtype)
    temp[CROP_MARGIN:-CROP_MARGIN, CROP_MARGIN:-CROP_MARGIN] = img
    img = temp
    # split into individual pieces:

    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(img)

    black = np.zeros_like(img)

    max_dim = 0
    all_pieces = []
    all_coordinates = []

    for i in range(1,retval):

        #filter the piece
        piece = black.copy()
        piece[labels == i] = 255

        stat = stats[i]

        y0 = stat[cv2.CC_STAT_TOP] - CROP_MARGIN
        x0 = stat[cv2.CC_STAT_LEFT] - CROP_MARGIN
        y1 = stat[cv2.CC_STAT_TOP] + stat[cv2.CC_STAT_HEIGHT] + CROP_MARGIN
        x1 = stat[cv2.CC_STAT_LEFT] + stat[cv2.CC_STAT_WIDTH] + CROP_MARGIN

        max_dim = max(max_dim, y1-y0)
        max_dim = max(max_dim, x1-x0)



        # crop the piece
        piece = piece[y0:y1,x0:x1]


        # get the coordinates of the corners of the piece
        x = (x0+x1)/2
        y = (y0+y1)/2
        p1,p2,p3,p4 = get_4_points(y,x)

        p1 = (p1[0]-x0, p1[1] - y0)
        p2 = (p2[0]-x0, p2[1] - y0)
        p3 = (p3[0]-x0, p3[1] - y0)
        p4 = (p4[0]-x0, p4[1] - y0)

        # draw corner for debug
        """
        piece = cv2.line(piece,p1,p2,color=125,thickness=10)
        piece = cv2.line(piece,p2,p3,color=125,thickness=10)
        piece = cv2.line(piece,p3,p4,color=125,thickness=10)
        piece = cv2.line(piece,p4,p1,color=125,thickness=10)
        cv2.imshow("",cv2.resize(piece,(400,400)))
        cv2.waitKey(0)
        """

        # save the result with the coordinates

        cv2.imwrite(output_divided_path+str(i-1)+".jpeg",piece)

        f = open(output_divided_path+str(i-1)+".txt",'w')

        f.write(f"p1: [{p1[0]}, {p1[1]}]\n")
        f.write(f"p2: [{p2[0]}, {p2[1]}]\n")
        f.write(f"p3: [{p3[0]}, {p3[1]}]\n")
        f.write(f"p4: [{p4[0]}, {p4[1]}]")

        f.close()

        #rotate the piece
        piece = util.rotate_image(piece)

        all_pieces.append(piece)

        #cv2.imshow("",piece)
        #cv2.waitKey(0)

    random.shuffle(all_pieces)

    num_of_pieces = len(all_pieces)

    pieces_per_side = math.ceil(np.sqrt(num_of_pieces))
    side_len =  (pieces_per_side)*max_dim+1

    result_image = np.zeros(shape=(side_len,side_len),dtype=np.uint8)

    i = 0

    for x in range(pieces_per_side):
        for y in range(pieces_per_side):

            try:
                paste_from = all_pieces[i]
            except: 
                break

            result_image = util.paste_on_top(result_image,paste_from,x*max_dim,y*max_dim)

            i+=1

    cv2.imwrite(output_raw_path,result_image)


# from the center of a piece, this function return his 4 corners
def get_4_points(y_center,x_center, dpi = 1200):
    
    y_center -= CROP_MARGIN
    x_center -= CROP_MARGIN

    SIDE_ONE_PIECE = 18 #mm

    SIDE_ONE_PIECE_INC = SIDE_ONE_PIECE * 0.0393701

    coordinate_x = (x_center*1.0/dpi)/SIDE_ONE_PIECE_INC
    coordinate_y = (y_center*1.0/dpi)/SIDE_ONE_PIECE_INC

    coordinate_x = int(coordinate_x)
    coordinate_y = int(coordinate_y)

    x_start = coordinate_x *SIDE_ONE_PIECE_INC*dpi
    x_end = x_start + SIDE_ONE_PIECE_INC*dpi

    y_start = coordinate_y *SIDE_ONE_PIECE_INC*dpi
    y_end = y_start + SIDE_ONE_PIECE_INC*dpi

    x_start = int(x_start) + CROP_MARGIN
    x_end = int(x_end) + CROP_MARGIN
    y_start = int(y_start) + CROP_MARGIN
    y_end = int(y_end) + CROP_MARGIN
    

    print(f"x: {coordinate_x}, y: {coordinate_y}")

    # return the 4 coordinates of the piece
    return (x_start,y_start), (x_end,y_start), (x_end,y_end), (x_start,y_end)

if __name__ == "__main__":
    main()