import cv2
import svg_to_png
import util
import numpy as np

# name of the piece
NAME = "8x8"

# the margin kept when cropping an image
CROP_MARGIN = 500


def main():



    # convert to png
    svg_path = f".\\SVGs\\{NAME}.svg"
    png_path = f".\\PNGs\\{NAME}.png"
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



    for i in range(1,retval):

        #filter the piece
        piece = black.copy()
        piece[labels == i] = 255

        stat = stats[i]

        y0 = stat[cv2.CC_STAT_TOP] - CROP_MARGIN
        x0 = stat[cv2.CC_STAT_LEFT] - CROP_MARGIN
        y1 = stat[cv2.CC_STAT_TOP] + stat[cv2.CC_STAT_HEIGHT] + CROP_MARGIN
        x1 = stat[cv2.CC_STAT_LEFT] + stat[cv2.CC_STAT_WIDTH] + CROP_MARGIN

        # crop the piece
        piece = piece[y0:y1,x0:x1]

        cv2.imshow("",piece)
        cv2.waitKey(0)


if __name__ == "__main__":
    main()