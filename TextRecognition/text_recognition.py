# USAGE
# python text_recognition.py --east frozen_east_text_detection.pb --image images/example_01.jpg
# python text_recognition.py --east frozen_east_text_detection.pb --image images/example_04.jpg --padding 0.05

# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import pytesseract
import argparse
import cv2


class RecognitionEngine:
    def __init__(self, image_path, width=320, height=320, east="frozen_east_text_detection.pb"):
        """
        Constructs a RecognitionEngine object

        :param image_path: a path to an image in which to recognise a text
        :param width: nearest multiple of 32 for resized width
        :param height: nearest multiple of 32 for resized height
        :param east: path to the EAST text detector
        """
        self._image_path = image_path
        self._width = width
        self._height = height
        self._east = east

        # load the input image and grab the image dimensions
        image = cv2.imread(self._image_path)
        self._orig = image.copy()
        (self._origH, self._origW) = image.shape[:2]

        # set the new width and height and then determine the ratio in change
        # for both the width and height
        (newW, newH) = (self._width, self._height)
        self._rW = self._origW / float(newW)
        self._rH = self._origH / float(newH)

        # resize the image and grab the new image dimensions
        self._image = cv2.resize(image, (newW, newH))
        (self._H, self._W) = self._image.shape[:2]

        # define the two output layer names for the EAST detector model that
        # we are interested -- the first is the output probabilities and the
        # second can be used to derive the bounding box coordinates of text
        self._layerNames = [
            "feature_fusion/Conv_7/Sigmoid",
            "feature_fusion/concat_3"]

        # load the pre-trained EAST text detector
        print("[INFO] loading EAST text detector...")
        self._net = cv2.dnn.readNet(self._east)

    def perform_recognition(self, min_confidence=0.5, padding=0.1):
        """
        Performing recognition of the text in the image
        :return: a dictionary including: coordinates of the bounding boxes of the text, a flag indicating whether any
            caption is recognised, and the caption itself
        """
        # construct a blob from the image and then perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv2.dnn.blobFromImage(self._image, 1.0, (self._W, self._H),
                                     (123.68, 116.78, 103.94), swapRB=True, crop=False)
        self._net.setInput(blob)
        (scores, geometry) = self._net.forward(self._layerNames)

        # decode the predictions, then  apply non-maxima suppression to
        # suppress weak, overlapping bounding boxes
        (rects, confidences) = self._decode_predictions(scores, geometry, min_confidence)
        boxes = non_max_suppression(np.array(rects), probs=confidences)

        # initialize the list of results
        results = []

        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios
            startX = int(startX * self._rW)
            startY = int(startY * self._rH)
            endX = int(endX * self._rW)
            endY = int(endY * self._rH)

            # in order to obtain a better OCR of the text we can potentially
            # apply a bit of padding surrounding the bounding box -- here we
            # are computing the deltas in both the x and y directions
            dX = int((endX - startX) * padding)
            dY = int((endY - startY) * padding)

            # apply padding to each side of the bounding box, respectively
            startX = max(0, startX - dX)
            startY = max(0, startY - dY)
            endX = min(self._origW, endX + (dX * 2))
            endY = min(self._origH, endY + (dY * 2))

            # extract the actual padded ROI
            roi = self._orig[startY:endY, startX:endX]

            # in order to apply Tesseract v4 to OCR text we must supply
            # (1) a language, (2) an OEM flag of 4, indicating that the we
            # wish to use the LSTM neural net model for OCR, and finally
            # (3) an OEM value, in this case, 7 which implies that we are
            # treating the ROI as a single line of text
            config = ("-l eng --oem 1 --psm 7")
            text = pytesseract.image_to_string(roi, config=config)

            # add the bounding box coordinates and OCR'd text to the list
            # of results
            results.append({
                               "text_coordinates": {
                                   "x_tl": startX,
                                   "y_tl": startY,
                                   "x_br": endX,
                                   "y_br": endY
                               },
                               "text_caption": text
                           }
            )

        return results

    def _decode_predictions(self, scores, geometry, min_confidence):
        # grab the number of rows and columns from the scores volume, then
        # initialize our set of bounding box rectangles and corresponding
        # confidence scores
        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        # loop over the number of rows
        for y in range(0, numRows):
            # extract the scores (probabilities), followed by the
            # geometrical data used to derive potential bounding box
            # coordinates that surround text
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            # loop over the number of columns
            for x in range(0, numCols):
                # if our score does not have sufficient probability,
                # ignore it
                if scoresData[x] < min_confidence:
                    continue

                # compute the offset factor as our resulting feature
                # maps will be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                # extract the rotation angle for the prediction and
                # then compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                # use the geometry volume to derive the width and height
                # of the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                # compute both the starting and ending (x, y)-coordinates
                # for the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                # add the bounding box coordinates and probability score
                # to our respective lists
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        # return a tuple of the bounding boxes and associated confidences
        return (rects, confidences)


if __name__ == "__main__":
    input_img_path = "example_06.jpg"
    recognition_engine = RecognitionEngine(input_img_path)
    recognition_results = recognition_engine.perform_recognition()

    # Visualise the results
    orig = cv2.imread(input_img_path)
    for result in recognition_results:
        output = orig.copy()
        x_tl = result["text_coordinates"]["x_tl"]  # tl = top left
        y_tl = result["text_coordinates"]["y_tl"]
        x_br = result["text_coordinates"]["x_br"]  # br = bottom right
        y_br = result["text_coordinates"]["y_br"]
        cv2.rectangle(output, (x_tl, y_tl), (x_br, y_br), (0, 0, 255), 2)

        print("Recognised text: {}".format(result["text_caption"]))
        cv2.imshow("Text Detection", output)
        cv2.waitKey(0)

    exit(0)
