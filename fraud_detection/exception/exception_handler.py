import os
import sys

class CustomException(Exception):
    def __init__(self, error_message: Exception, error_detail: sys):

        super().__init__(error_message)
        self.error_message= CustomException.error_message_detail(error_message,error_detail=error_detail)

    @staticmethod
    def error_message_detail(error:Exception, error_detail:sys):
        _, _, exc_tb = error_detail.exc_info()
        #extracting file name from exception traceback
        file_name = exc_tb.tb_frame.f_code.co_filename 

        #preparing error message
        error_message = f"Error occurred python script name [{file_name}]" \
                        f" line number [{exc_tb.tb_lineno}] error message [{error}]."
        
        return error_message
    
    def __repr__(self):
        return CustomException.__name__.__str__()

    def __str__(self):
        return self.error_message