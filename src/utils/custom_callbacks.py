import tensorflow as tf
import logging

class ThresholdAccuracy(tf.keras.callbacks.Callback):
    # to stop trainning on acheiving accuracy > threshold defined
    def __init__(self,ACCURACY_THRESHOLD) -> None:
        super().__init__()
        self.ACCURACY_THRESHOLD = ACCURACY_THRESHOLD
        logging.info("Preparing custom callbacks...")
    
    def on_epoch_end(self, epoch, logs={}):
        if(logs.get('acc') > self.ACCURACY_THRESHOLD):
            logging.info("\nReached %2.2f%% accuracy, so stopping training!!" %(self.ACCURACY_THRESHOLD*100))
            self.model.stop_training = True
