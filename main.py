import data_process.data_processing as dp

if __name__ == '__main__':
    # Initialize parser object for each xml dataset.
    jeff_parser = dp.ProcessData("export_nguyen.xml", "jeff1")
    feiyang_parser =  dp.ProcessData("export_feiyang.xml", "feiyang1")
    john_parser = dp.ProcessData("export_johnL.xml", "john1")
    kaylie_parser = dp.ProcessData("export_kaylie.xml", "kaylie1")

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

    # for type in jeff_record_types:
    kaylie_parser.get_type_values('HKQuantityTypeIdentifierHeight')
    kaylie_parser.get_type_values('HKQuantityTypeIdentifierBodyMass')


    # for type in feiyang_record_types:
    #     feiyang_parser.get_type_values(type)

    # for type in john_record_types:
    #     john_parser.get_type_values(type)

    # for type in kaylie_record_types:
    #     kaylie_parser.get_type_values(type)

    # for type in jeff_record_types:
    #     print("Creating shelve for type:", type)
    #     jeff_parser.create_type_shelf(type)

    # for type in feiyang_record_types:
    #     print("Creating shelve for type:", type)
    #     feiyang_parser.create_type_shelf(type)