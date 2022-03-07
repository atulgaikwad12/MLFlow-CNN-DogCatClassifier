import io
import logging 
import os
from src.utils.common import read_yaml
import pickle

def getCallbackList(config_path):
    callback_lst = []

    try:

        config = read_yaml(config_path)
        callbacksbyte_file = os.path.join(
        config["artifacts"]["CALLBACKS_DIR"],
        config["callbacks"]["CB_BYTECODE_FNAME"])

        if(os.path.isfile(callbacksbyte_file)):
            file = open(callbacksbyte_file, 'r') 
            obj = pickle.load(file)

            if(obj.dtype == list):
                callback_lst = obj
                logging.info(f"found callbacks list - {obj}")
            else:
                logging.warning(f"{obj.dtype} :unexpected data type of callback list object")
            logging.info(f"loaded pickle file {callbacksbyte_file}")
        else:
            logging.warning(f"not found callback object pickle file {callbacksbyte_file}")
    except Exception as e:
        logging.error("Failed to load callback byte code file")
        logging.error(e)

    return callback_lst

def log_model_summary(model):
    '''
    Description : using lambda function to write each line of summary to IO stream 
    and then return value of stream for logging purpose  
    '''

    with io.StringIO() as stream:
        model.summary(
            print_fn=lambda x: stream.write(f"{x}\n")
        )

        summary_details = stream.getvalue()
        
    return summary_details