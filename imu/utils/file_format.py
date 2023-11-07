import os


def prepend_multiple_lines(file_name, list_of_lines):
    """Insert given list of strings as a new lines at the beginning of a file"""
    # define name of temporary dummy file
    aux_file = file_name + '.sto'
    # open given original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(aux_file, 'w') as write_obj:
        # Iterate over the given list of strings and write them to dummy file as lines
        for line in list_of_lines:
            write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(aux_file, file_name)


def format_to_sto(column_name, data_frame):

    #remove []
    data_frame[column_name] = data_frame[column_name].str.strip('[]')
    #remove first white space
    data_frame[column_name] = data_frame[column_name].str.lstrip()
    data_frame[column_name] = data_frame[column_name].str.rstrip()
    # create list spliting by whitespace
    data_frame[column_name] = data_frame[column_name].str.split(' +')
    #convert list to string removing space
    data_frame[column_name] = [','.join(map(str, l)) for l in data_frame[column_name]]
