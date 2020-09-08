from pascal_voc_io import XML_EXT
from pascal_voc_io import PascalVocWriter
from pascal_voc_io import PascalVocReader
from yolo_io import YoloReader
from yolo_io import YOLOWriter
import os.path
import sys

try:
    from PyQt5.QtGui import QImage
except ImportError:
    from PyQt4.QtGui import QImage


# Search all pascal annotation (xml files) in this folder
def convert(image_path,annotation_path):

    save_path=os.path.join(os.path.dirname(annotation_path),"xml_converted")
    if not os.path.exists(save_path): os.makedirs(save_path)

    for file in os.listdir(annotation_path):
        if file.endswith(".xml"):
            annotation_no_xml = os.path.splitext(file)[0]

            imagePath = image_path + "/" + annotation_no_xml + ".jpg"

            image = QImage()
            image.load(imagePath)
            imageShape = [image.height(), image.width(), 1 if image.isGrayscale() else 3]
            imgFolderName = os.path.basename(image_path)
            imgFileName = os.path.basename(imagePath)

            writer = YOLOWriter(imgFolderName, imgFileName, imageShape, localImgPath=imagePath)

            # Read classes.txt
            classListPath = annotation_path + "/" + "classes.txt"
            classesFile = open(classListPath, 'r')
            classes = classesFile.read().strip('\n').split('\n')
            classesFile.close()

            # Read VOC file
            filePath = annotation_path + "/" + file
            tVocParseReader = PascalVocReader(filePath)
            shapes = tVocParseReader.getShapes()
            num_of_box = len(shapes)

            for i in range(num_of_box):
                label = classes.index(shapes[i][0])
                xmin = shapes[i][1][0][0]
                ymin = shapes[i][1][0][1]
                x_max = shapes[i][1][2][0]
                y_max = shapes[i][1][2][1]

                writer.addBndBox(xmin, ymin, x_max, y_max, label, 0)
        
            writer.save(targetFile= save_path + "/" + annotation_no_xml + ".txt")
    

if __name__=="__main__":

    image_path= "C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\own images\\combined\\final\\train_images" # should include the classes as well.
    annotation_path="C:\\Users\\gishy\\Dropbox\\My PC (LAPTOP-SQRN8N46)\\Desktop\\own images\\combined\\final\\train_labels_xml"
 
    convert(image_path,annotation_path)