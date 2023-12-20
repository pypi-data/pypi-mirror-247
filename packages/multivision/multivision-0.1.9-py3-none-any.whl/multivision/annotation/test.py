from autodistill.detection import CaptionOntology
from autodistill_grounding_dino import GroundingDINO  #for detetction images 
from autodistill_grounded_sam import GroundedSAM #for segmentation images
from google_images_downloader import GoogleImagesDownloader
import supervision as sv

def create_ontology_dict():
        ontology_input = input("Enter the ontology as a comma-separated list (e.g., car:car or more classes car:vehicle,person:human): ")

        if ":" in ontology_input:
            ontology_dict = dict(item.split(":") for item in ontology_input.split(","))
        else:
            ontology_dict = {ontology_input: ontology_input}

        return ontology_dict

def create_captions_det(ontology_dict, image_folder, dataset_folder):
        ontologyDet = CaptionOntology(ontology_dict)
        base_model = GroundingDINO(ontology=ontologyDet)
        #base_model = GroundedSAM(ontology=ontology)
        dataset = base_model.label(
            input_folder=image_folder,
            extension=".png",
            output_folder=dataset_folder
        )
        return dataset
def create_captions_seg(ontology_dict, image_folder, dataset_folder):
        ontology = CaptionOntology(ontology_dict)
        base_model = GroundedSAM(ontology=ontology)
        dataset = base_model.label(
            input_folder=image_folder,
            extension=".png",
            output_folder=dataset_folder
        )
        return dataset

ontology_dict=create_ontology_dict()
image_folder="images"
dataset_folder="dataset2"
#create_captions_det(ontology_dict, image_folder, dataset_folder)

create_captions_seg(ontology_dict, image_folder, dataset_folder)