import io
import logging 

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