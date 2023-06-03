import data_processing as dp

if __name__ == '__main__':
    # Initialize parser object for each xml dataset.
    jeff_parser = dp.ProcessData("export_nguyen.xml", "95dca675-e9eb-4436-8ff7-024293cf493c")
    feiyang_parser =  dp.ProcessData("export_feiyang.xml", "d17cf85b-ef97-4a7d-86e2-326c32b7d22f")
    john_parser = dp.ProcessData("export_johnL.xml", "2f3d0461-caa7-470d-b79f-deea2408f304")
    kaylie_parser = dp.ProcessData("export_kaylie.xml", "eb419891-fbee-44bc-a7a6-63c8a808fd5d")

    # Parse the file and store a tree root.
    jeff_parser.parse_file()
    feiyang_parser.parse_file()
    john_parser.parse_file()
    kaylie_parser.parse_file()

    """
    # Get the full context of attributes associated to each type of record stored by the data. 
    # This is stored as a dictionary {Type: Array[Attribute_1, Attribute_2, ..., Attribute_n]}
    jeff_record_context = jeff_parser.get_type_context()
    feiyang_record_context = feiyang_parser.get_type_context()
    john_record_context = john_parser.get_type_context()
    kaylie_record_context = kaylie_parser.get_type_context()

    full_context_set = set(jeff_record_context.keys()) & set(feiyang_record_context.keys()) & set(john_record_context.keys()) & set(kaylie_record_context.keys())

    full_record_context = dict()
    full_record_context.update(jeff_record_context)
    full_record_context.update(feiyang_record_context)
    full_record_context.update(john_record_context)
    full_record_context.update(kaylie_record_context)
    """

    jeff_record_types = jeff_parser.get_record_types()
    feiyang_record_types = feiyang_parser.get_record_types()
    john_record_types = john_parser.get_record_types()
    kaylie_record_types = kaylie_parser.get_record_types()

    print("== jeff events ==")
    for type in jeff_record_types:
        print("Creating log events for type:", type)
        jeff_parser.create_server_health_events(type)
    
    print("== feiyang events ==")
    for type in feiyang_record_types:
        print("Creating log events for type:", type)
        feiyang_parser.create_server_health_events(type)
    
    print("== john events ==")
    for type in john_record_types:
        print("Creating log events for type:", type)
        john_parser.create_server_health_events(type)
    
    print("== kaylie events ==")
    for type in kaylie_record_types:
        print("Creating log events for type:", type)
        kaylie_parser.create_server_health_events(type)