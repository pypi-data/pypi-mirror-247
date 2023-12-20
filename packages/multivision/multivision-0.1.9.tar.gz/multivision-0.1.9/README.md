# MultiVisionToolkit

MultiVisionToolkit is a Python package that provides tools for object detection and segmentation, specifically using the YOLOv8 model. It includes real-time detection on camera video, visualization metrics, and the ability to convert reports to document and PDF files.

## Installation

```bash
pip install multivision
```
##  Usage
Object Detection with YOLOv8

![](screenshot.png)

[Detailed feature showcase with images](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features):

## Download images for created dataset
```
#download images form internet
#using class name and count for images more than 500 images for best training 
from multivision.dataset import dataset as ds
class_name='dog'
count=100
ds.download_images(class_name,count)
```

## Extract imges from any video 
```
from multivision.dataset import dataset as ds
video_path="video.mp4"
images_folder_path="images"
frame_strid=10
ds.extract_images_video(video_path,images_folder_path,frame_strid)
```
## download video from youtube and extract to images
```
from multivision.dataset import dataset as ds
video_url="https://www.youtube.com/shorts/6eb9-P6KHN0"

#ds.download_yt(video_url, output_path='.')
#or
output_path="images"
ds.download_yt(video_url, output_path)
```

## Annotation auto label for dataset without any manual tools
```
from multivision.annotation import autolabel as auto
ontology_dict=auto.create_ontology_dict() #create caption for custom dataset
image_folder=path_of_images_folder"
dataset_folder="dataset_folder_to_save_train,val with images labels "
auto.create_captions(ontology_dict, image_folder, dataset_folder)


```

## training custom datatset with yaml data file for detection training

```
from multivision.train import yolov8 as y8
model_det_name="yolov8n.pt"
epochs_no=5
data_yaml_path="E:/multivision/dataset/data.yaml"
y8.y8d_train(model_det_name,epochs_no,data_yaml_path)
```
## training custom  datatset with yaml data file for segmentation training

```

model_seg_name="yolov8n-seg.pt"
epochs_no=10
y8.y8s_train(model_name,epochs_no,data_yaml_path)
```


## Visualization Metrics

```
from multivsion.visualize import vis as vis
vis.images_google_colab(folder_path)
vis.display_images_cv(folder_path,scale_factor)
vis.display_images_with_grid(folder_path, rows, cols)
vis.plot(annotation_path,images_dir_path,yaml_path,samples_no)
```
## Convert Report to Document and PDF

```
# Example Usage:
folder_path = "images"
output_docx = "output_document.docx"
title = "My Document Title"
author = "Your Name"
pdf_path="book.pdf"
copyright_notice = "© 2023 Falah.G.Salieh"

conclusion = "This is the conclusion of the document."
from multivision.docx import document as doc
from multivision.docx import document as pdf
doc.create_word_document(folder_path, output_docx, title, author, conclusion)
pdf.images_to_pdf(folder_path, pdf_path, title, copyright_notice)
```
## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Citation
If you find MultiVisionToolkit helpful in your work, please consider citing it. You can use the following BibTeX entry:
```
@software{multivisiontoolkit,
  author = {Falah.G.Salieh},
  title = {MultiVisionToolkit},
  year = {2023},
  url = {https://github.com/falahgs/multivisiontoolkit},
}
```

