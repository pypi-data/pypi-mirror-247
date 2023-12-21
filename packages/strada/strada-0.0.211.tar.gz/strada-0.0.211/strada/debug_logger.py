import inspect
from enum import Enum
import json

class HttpObjectType(Enum):
    REQUEST = 'REQUEST'
    RESPONSE = 'RESPONSE'
    
class LogType(Enum):
    FUNCTION_CALL = 'FUNCTION_CALL'
    HTTP_OBJECT = 'HTTP_OBJECT'
    
class DebugLogger:
    @staticmethod
    def log_http_object(http_object_type, log_entry):
        # log_entry must be a dictionary
        try:
            log_entry['log_type'] = LogType.HTTP_OBJECT.name
            log_entry['http_object_type'] = http_object_type
            
            # Convert log entry to JSON
            formatted_entry = json.dumps(log_entry)

            # Print the log entry
            print(f'<LOG>{formatted_entry}</LOG>', flush=True)

        except Exception as e:
            # todo: Log the error
            pass
        
    @staticmethod
    def log_function_call(log_entry, instance_name=None, app_name=None):
        # print('<LOG>instance_name: ', instance_name, '</LOG>')
        frame = inspect.currentframe()
        # log_entry must be a dictionary
        try:
            function_name = None
            for name, val in frame.f_back.f_globals.items():
                # print('<LOG>name: ', name, '</LOG>')
                # print('<LOG>val: ', val, '</LOG>')
                if (val is not None) and (val.__class__.__name__ == instance_name):
                    function_name = name
                    break

            # Add the function name to the log information
            log_entry['app_name'] = app_name
            log_entry['instance_name'] = instance_name
            log_entry['log_type'] = LogType.FUNCTION_CALL.name
            log_entry['function_name'] = function_name
            
            # Convert log entry to JSON
            formatted_entry = json.dumps(log_entry)
            
            print(f'<LOG>{formatted_entry}</LOG>', flush=True)

        finally:
            del frame