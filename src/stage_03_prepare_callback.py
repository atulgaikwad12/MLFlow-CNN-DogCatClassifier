import argparse
import os
import logging
import tensorflow as tf
from src.utils.common import create_directories, read_yaml,get_unique_log_path
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

class customCallback(tf.keras.callbacks.Callback):
    def __init__(self,ACCURACY_THRESHOLD) -> None:
        super().__init__()
        self.ACCURACY_THRESHOLD = ACCURACY_THRESHOLD
        logging.info("Preparing custom callbacks...")
    
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('acc') > self.ACCURACY_THRESHOLD):
            logging.info("\nReached %2.2f%% accuracy, so stopping training!!" %(self.ACCURACY_THRESHOLD*100))
            self.model.stop_training = True


def main(config_path):
    callbacks_lst = []

    ## read config files
    config = read_yaml(config_path)
    #config["callbacks"]
    artifacts = config["artifacts"]

    callbacks_dir = artifacts["CALLBACKS_DIR"] 
    create_directories([callbacks_dir])

    callbacksbyte_file = os.path.join(
    artifacts["CALLBACKS_DIR"],
    artifacts["CB_BYTECODE_FNAME"])

    # Need to add Callback part here 

    checkpoint_filepath = '/tmp/checkpoint'
    model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

    log_dir = get_unique_log_path(artifacts["BASE_LOG_DIR"])
    #%tensorboard --logdir logs/fit
    tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
    early_stopping_cb = tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True)
    lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="loss", factor=0.1, patience=3, mode="max", verbose=1
)

    ACCURACY_THRESHOLD = 0.95
    customCallback(ACCURACY_THRESHOLD)

    if(os.path.exists(callbacks_dir) and len(callbacks_lst) > 0):
        file = open(callbacksbyte_file, 'w') 
        pickle.dump(callbacks_lst, file)

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