from pdf2image import convert_from_path
import matplotlib.pyplot as plt
import cv2
import pytesseract
import numpy as np


class OCR:
    def __init__(self, pdf_file):
        self.images = convert_from_path(pdf_file)

    def up_scale_image(image, dpi, d=2):
        """
        Adjust the display size of an image without changing the actual image resolution.
        """
        if d == 3:
            height, width, dimension = image.shape
        elif d == 2:
            height, width = image.shape
        fig_size = width / float(dpi), height / float(dpi)
        return fig_size

    def display(image, fig_size=[6.4, 4.8]):
        """
        Display the image at a larger size based on the desired DPI.
        """
        plt.figure(figsize=fig_size)
        plt.axis("off")
        plt.imshow(image, cmap="grey")
        plt.show()

    def preprocessed(img):
        im_h, im_w, im_d = img.shape
        base_image = img.copy()

        # Preprocessing
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(grey, (7, 7), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        roi = thresh[152:2100, :]
        doc = pytesseract.image_to_string(roi, lang="vie")
        return doc, roi

    def pdf_to_string(self):
        for i in range(len(self.images)):
            self.images[i] = np.array(self.images[i])

        doc_list = []

        for i in range(len(self.images)):
            doc, processed = OCR.preprocessed(self.images[i])
            doc_list.append(doc)

        return doc_list
