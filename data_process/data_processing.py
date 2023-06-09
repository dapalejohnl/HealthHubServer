from lxml import etree

import requests
import json
import datetime

BACKEND_HOST_IP = "127.0.0.1:8000" #Currently just on local machine
TIMESTAMP_STR_FORMAT = "%Y-%m-%d %H:%M:%S %z"

class ProcessData:
    def __init__(self, path, user_id) :
        """Class constructor."""
        self.file_path = path    # This is the class variable representing the title we're interestsed in.
        self.user_id = user_id
        self.parsed_root = None  # Class variable representing the parsed xml object.


    def parse_file(self):
        """Open the file via path and then parse it."""
        with open(self.file_path, 'rb') as f:
            # In case of faulty Apple Health tag, we can recover the data, which we set as the parser.
            tree = etree.parse(f, etree.XMLParser(recover=True))
            self.parsed_root = tree.getroot()


    def get_record_types(self):
        """Fetch the record types and return it as a set."""
        # Initialize a set for unique elements.
        type_set = set()

        # in case the parsed root is not a Nonetype file.
        if self.parsed_root is not None:
            for record in self.parsed_root.iter('Record'): 
                type_set.add(record.get('type'))
        return type_set


    def get_type_context(self):
        """
        Returns a dictionary of record types and the full attribute context.
        Example: {HeartRate: ['type', 'sourceName', 'sourceVersion', 'device', 'unit', 'creationDate', 'startDate', 'endDate', 'value']}
        """
        record_context = dict()
        type_array = list(self.get_record_types())

        for type in type_array:
            for record in self.parsed_root.iter('Record'):
                if (record.get('type') == type):
                    record_context[type] = record.attrib.keys() 

        return record_context
    

    def get_type_values(self, record_type):
        """Get the attribute values of record_type and write it to a file."""
        # Open up a file to write to.
        with open(record_type + '.txt', 'w') as f:
            # iterate through all the record tags.
            for record in self.parsed_root.iter('Record'):
                if (record.get('type') == record_type):
                    value_arr = record.attrib.values()
                    f.write('***'.join(value_arr) + '\n')

    def create_type_shelf(self, record_type):
        # Go through every record
        with shelve.open("shelves/" + record_type) as record_shelve:
            new_list = []
            for record in self.parsed_root.iter('Record'):
                # When the record is of the preferred type, we will extract the values.
                if (record.get('type') == record_type):
                    
                    # Put into python shelves here
                    new_list.append(dict(record.attrib))
            record_shelve[self.user_id] = new_list
            
    def create_server_health_events(self, record_type):
        event_list = []
        url = "http://{:s}/{:s}".format(BACKEND_HOST_IP, "users/logevents")
        
        for record in self.parsed_root.iter('Record'):
            # When the record is of the preferred type, we will extract the values.
            if (record.get('type') == record_type):
                record_type = record.get('type')
                record_value = record.get('value')
                start_str = record.get('startDate')
                end_str = record.get('endDate')
                
                start_timestamp = datetime.datetime.strptime(start_str, TIMESTAMP_STR_FORMAT).timestamp()
                end_timestamp = datetime.datetime.strptime(end_str, TIMESTAMP_STR_FORMAT).timestamp()
                
                new_event = {
                    "type": record_type,
                    "value": record_value,
                    "startTimestamp": int(start_timestamp),
                    "endTimestamp": int(end_timestamp)
                }
                event_list.append(new_event)
                
            if len(event_list) >= 5000:
                request_data = {
                    "userUID": self.user_id,
                    "events": event_list
                }
                response = requests.post(url, json=request_data, timeout=5)
                event_list = []
        
        if len(event_list) > 0:
            request_data = {
                "userUID": self.user_id,
                "events": event_list
            }
            response = requests.post(url, json=request_data, timeout=5)
            event_list = []