import logging
import os
import shutil
import imghdr
from PIL import Image 
from src.utils.common import create_directories

def validate_imgdata(config: dict) -> None:
    '''
    Author       : atul.gaikwad
    Description  : Function to validate image data files (file formate, color band) and archive invalid files in bad data directory
    Input params : Configuration dictionary to define data directories 
    '''
    
    PARENT_DATA_DIR = os.path.join(
        config["data"]["unzip_data_dir"],
        config["data"]["parent_data_dir"]
    )

    BAD_DATA_DIR = os.path.join(
        config["data"]["bad_data_dir"]
    )

    create_directories(BAD_DATA_DIR)

    for dir in os.listdir(PARENT_DATA_DIR):

        sub_dir = os.path.join(PARENT_DATA_DIR, dir)

        for imgfile in os.listdir(sub_dir):

            img_path =  os.path.join(sub_dir,imgfile)

            try:
                img = Image.open(img_path)
                img.verify()

                # validation for image file having file formate other than jpeg and png & invalid color band not in RGB
                if( len(img.getbands()) !=3 or imghdr.what(img_path) not in ['jpeg','png']):
                    
                    logging.warning(f"{img_path} Invalid image file format or color band length")
                    archive_bad_file(imgfile, img_path)
                    continue
            except Exception as e:
                logging.warning(f"{img_path} Invalid image file ")
                logging.exception(e)
                archive_bad_file(imgfile, img_path)

        
        def archive_bad_file(filename: str, src_file_path: str) -> None:
            '''
            Author : atul.gaikwad
            Description : function to move file in bad data directory 
            Input params : file name and source file path 
            '''
            bad_data_path = os.path.join(BAD_DATA_DIR,filename)
            shutil.move(src_file_path,bad_data_path)
            logging.warning(f"{filename} file moved to {bad_data_path}")

   










