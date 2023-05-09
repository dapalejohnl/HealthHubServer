import data_processing as dp

if __name__ == '__main__':
    # Initialize parser object for each xml dataset.
    jeff_parser = dp.ProcessData("export_nguyen.xml")
    feiyang_parser =  dp.ProcessData("export_feiyang.xml")
    john_parser = dp.ProcessData("export_johnL.xml")
    kaylie_parser = dp.ProcessData("export_kaylie.xml")

    # Parse the file and store a tree root.
    jeff_parser.parse_file()
    # feiyang_parser.parse_file()
    # john_parser.parse_file()
    # kaylie_parser.parse_file()

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

    for type in jeff_record_types:
        jeff_parser.get_type_values(type)

    # jeff_parser.get_type_values('HKQuantityTypeIdentifierStepCount')