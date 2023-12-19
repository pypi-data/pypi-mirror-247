from enum import Enum
import json

class HttpObjectType(Enum):
    REQUEST = 'REQUEST'
    RESPONSE = 'RESPONSE'
    
class HttpLogger:
    @staticmethod
    def log_http_object(http_object_type, log_entry):
        # log_entry must be a dictionary
        try:
            # Add the http_object_type to the log entry
            log_entry['http_object_type'] = http_object_type.name
            
            # Convert log entry to JSON
            formatted_entry = json.dumps(log_entry)

            # Print the log entry
            print(f'<>{formatted_entry}')

        except Exception as e:
            # todo: Log the error
            pass