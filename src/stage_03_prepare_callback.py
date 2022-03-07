import argparse
import os
import logging
import tensorflow as tf
from src.utils.common import create_directories, read_yaml,get_unique_log_path
from src.utils.custom_callbacks import ThresholdAccuracy
import pickle

STAGE = "Callback Addition" ## <<< change stage name 
LOG_DIR = "logs"
LOG_FILENAME = "running_logs.log"

logging.basicConfig(
            filename = os.path.join(LOG_DIR, LOG_FILENAME), 
            level=logging.DEBUG, 
            format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
            filemode="a"
            )


def save_callbacks(callbacks_obj_lst, file_path):

    if(len(callbacks_obj_lst) > 0 and os.path.exists(file_path) ):
        file = open(file_path, 'w') 
        pickle.dump(callbacks_obj_lst, file)
        logging.info(f"Saved callbacks object list in file {file_path}")

def main(config_path):
    callbacks_obj_lst = [] # list to save callback object

    ## read config files
    config = read_yaml(config_path)
    cb_params = config["callbacks"] # callback related parameters 
    artifacts = config["artifacts"] # directory path info

    cblist = cb_params["cblist"] # list of callbacks defined 
    if(len(cblist) > 0):
        # when we have callbacks to prepare

        callbacks_dir = artifacts["CALLBACKS_DIR"] 
        create_directories([callbacks_dir])

        for callback in cblist:
            if (callback == "ModelCheckpoint"):

                checkpoint_dir = os.path.join(callbacks_dir,cb_params[callback]["CHECKPOINT_DIR"]) 
                create_directories([checkpoint_dir])

                filename = cb_params[callback]["filename"] #"weights.{epoch:02d}-{val_loss:.2f}.hdf5"
                checkpoint_filepath = os.path.join(checkpoint_dir,filename)

                model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
                                    filepath=checkpoint_filepath,
                                    save_weights_only=True,
                                    monitor='val_accuracy',
                                    mode='max',
                                    save_best_only=True)

                callbacks_obj = model_checkpoint_callback
            elif(callback == "ThresholdAccuracy"):

                ACCURACY_THRESHOLD = cb_params[callback]["ACCURACY_THRESHOLD"]
                callbacks_obj = ThresholdAccuracy(ACCURACY_THRESHOLD)

            elif(callback == "TensorBoardLog"):
                log_dir = get_unique_log_path(cb_params[callback]["TENSORBOARD_ROOT_LOG_DIR"])
                #%tensorboard --logdir logs/fit
                tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
                callbacks_obj = tensorboard_cb

            elif(callback == "EarlyStopping"):

                patience = cb_params[callback]["patience"]
                restore_best_weights = cb_params[callback]["restore_best_weights"]

                early_stopping_cb = tf.keras.callbacks.EarlyStopping(patience = patience,
                                    restore_best_weights = restore_best_weights)
                callbacks_obj = early_stopping_cb   

            elif(callback == "ReduceLROnPlateau"):

                monitor = cb_params[callback]["monitor"]
                factor = cb_params[callback]["factor"]
                patience = cb_params[callback]["patience"]
                mode = cb_params[callback]["mode"]
                verbose = cb_params[callback]["verbose"]

                lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(monitor=monitor, 
                                factor=factor, patience=patience, mode=mode, verbose=verbose)
                callbacks_obj = lr_scheduler

            else:
                logging.warning(f"{callable} not defined !!")
                continue

            callbacks_obj_lst.append(callbacks_obj)

        callbacksbyte_file = os.path.join(callbacks_dir,cb_params["CB_BYTECODE_FNAME"]) 
        logging.info(f"Saving list of callback objects .....\n{callbacks_obj_lst} ")
        save_callbacks(callbacks_obj_lst = callbacks_obj_lst,
                        file_path = callbacksbyte_file)
        
    else:
        logging.warning("No callback found in config file .....")


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config","-c",default="configs/config.yml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e