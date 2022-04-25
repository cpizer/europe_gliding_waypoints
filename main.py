import sys
import datetime
from pathlib2 import *
import requests
import zipfile
import io
import codecs
import os
import numpy as np
import ofm_utils

current_airac_id = str(ofm_utils.get_current_airac_id())

PATH_CUP_FRANCE = "http://download.xcsoar.org/content/waypoint/country/FR.cup"
PATH_OPENAIR_FRANCE = "https://drive.google.com/uc?id=1O6sPeB8da9xTH7VNeFekM4j71HrB4Ywk&export=download"

PATH_CWD = Path.cwd()

def parse_line(line, styles = []):
    line = line.replace("\r", "")
    line = line.replace("\n", "")
    
    line = line.replace("Ä", "Ae").replace("ä", "ae").replace("Ö", "oe").replace("ö", "oe").replace("Ü", "Ue").replace("ü", "ue")
    
    split_line = line.split(",")
    tmp_name = ""
    tmp_code = ""
    tmp_country = ""
    tmp_lat = ""
    tmp_lon = ""
    tmp_elev = ""
    tmp_style = ""
    tmp_rwdir = ""
    tmp_rwylen = ""
    tmp_freq = ""
    tmp_desc = ""
    fields = []
    if len(split_line) == 11:
        for tmp_field in split_line:
            fields.append(tmp_field)
    else:
        in_double_quotes = False
        composed_field = ""
        for tmp_field in split_line:
            if "\"" in tmp_field or in_double_quotes:
                for tmp_char in tmp_field:
                    composed_field = composed_field + tmp_char
                    if tmp_char == "\"" and not in_double_quotes:
                        in_double_quotes = True
                    elif tmp_char == "\"" and in_double_quotes:
                        in_double_quotes = False
                        fields.append(composed_field)
                        composed_field = ""
            else:
                fields.append(tmp_field)
    
    tmp_style = prepare_field(fields[6])

    if styles and tmp_style.isnumeric():
        if not int(tmp_style) in styles:
            return ""

    for field_ind in range(11):
        if field_ind == 0:
            tmp_name = prepare_field(fields[field_ind], True)
        elif field_ind == 1:
            tmp_code = prepare_field(fields[field_ind], True)
        elif field_ind == 2:
            tmp_country = prepare_field(fields[field_ind])
        elif field_ind == 3:
            tmp_lat = prepare_field(fields[field_ind])
        elif field_ind == 4:
            tmp_lon = prepare_field(fields[field_ind])
        elif field_ind == 5:
            tmp_elev = prepare_field(fields[field_ind])
        elif field_ind == 7:
            tmp_rwdir = prepare_field(fields[field_ind])
        elif field_ind == 8:
            tmp_rwylen = prepare_field(fields[field_ind])
            tmp_len_m = 0
            if "ft" in tmp_rwylen:
                tmp_len_ft = float(tmp_rwylen[:tmp_rwylen.find("ft")])
                tmp_len_m = np.round(tmp_len_ft * 0.3048)
                tmp_rwylen = "{}m".format(int(tmp_len_m))
        elif field_ind == 9:
            tmp_freq = prepare_field(fields[field_ind])
            decimal_ind = tmp_freq.find(".")
            if decimal_ind - 3 >= 0 and decimal_ind + 4 <= len(tmp_freq):
                tmp_freq = tmp_freq[decimal_ind-3:decimal_ind+4]
        elif field_ind == 10:
            tmp_desc = prepare_field(fields[field_ind], True)
    
    new_line = "{},{},{},{},{},{},{},{},{},{},{}".format(tmp_name, tmp_code, tmp_country, tmp_lat, tmp_lon, tmp_elev, tmp_style, tmp_rwdir, tmp_rwylen, tmp_freq, tmp_desc)
    return new_line

def prepare_field(raw_field, double_quotes_required = False):
    len_raw_field = len(raw_field)
    if len_raw_field == 0:
        if double_quotes_required:
            return "\"\""
        else:
            return ""
    
    started_information = False
    processed_field = ""
    for tmp_ind in range(len_raw_field):
        if not started_information and raw_field[tmp_ind] == " ":
            continue
        elif not started_information and not raw_field[tmp_ind] == " ":
            started_information = True
        processed_field = processed_field + raw_field[tmp_ind]
    
    len_processed_field = len(processed_field)
    tmp_ind = -1
    while -1*tmp_ind <= len_processed_field:
        if not processed_field[tmp_ind] == " ":
            break
        tmp_ind -= 1
    if not tmp_ind == -1:
        processed_field = processed_field[:tmp_ind+1]
    
    if not double_quotes_required:
        field_without_double_qoutes = ""
        for tmp_char in processed_field:
            if not tmp_char == "\"":
                field_without_double_qoutes = field_without_double_qoutes + tmp_char
        return field_without_double_qoutes
    else:
        field_without_double_qoutes = ""
        for tmp_char in processed_field:
            if not tmp_char == "\"":
                field_without_double_qoutes = field_without_double_qoutes + tmp_char
        field_with_double_qoutes = "\"" + field_without_double_qoutes + "\""
        return field_with_double_qoutes

if __name__ == "__main__":
    PATH_RES = PATH_CWD / Path("res")
    PATH_RES_INPUT = PATH_RES / Path("input")
    PATH_RES_OUTPUT = PATH_RES / Path("output")
    WAYPOINTS_FILENAME_OUTPUT_FILE = "europe_{}.cup".format(datetime.date.today().isoformat().replace("-","_"))
    AIRSPACES_FILENAME_OUTPUT_FILE = "europe_openair_{}.txt".format(datetime.date.today().isoformat().replace("-","_"))
    PATH_RES_WAYPOINTS_OUTPUT_FILE = PATH_RES_OUTPUT / Path(WAYPOINTS_FILENAME_OUTPUT_FILE)
    PATH_RES_AIRSPACES_OUTPUT_FILE = PATH_RES_OUTPUT / Path(AIRSPACES_FILENAME_OUTPUT_FILE)

    print("Create all  files based on AIRAC-ID {}".format(current_airac_id))

    waypoint_styles = []
    build_files_only = False
    if len(sys.argv) > 1:
        for i in range(1,len(sys.argv)):
            if sys.argv[i].isnumeric():
                waypoint_styles.append(int(sys.argv[i]))
            elif "--build" in sys.argv[i]:
                build_files_only = True
                print("Only build the files...")
            else:
                print("WARNING: '{}' is not a valid command line argument!!!")
    
    if not build_files_only:
        if not PATH_RES_INPUT.is_dir():
            PATH_RES_INPUT.mkdir(parents = True)
        
        if not PATH_RES_OUTPUT.is_dir():
            PATH_RES_OUTPUT.mkdir(parents = True)
        
        path_list = []
        product_dict = ofm_utils.get_global_product_dict()
        for region_code, products in product_dict.items():
            if "OPENAIR" in products:
                path_list.append(products["OPENAIR"])
            if "CUP" in products:
                path_list.append(products["CUP"])
        #path_list.append(PATH_OPENAIR_FRANCE)
        path_list.append(PATH_CUP_FRANCE)

        for tmp_path in path_list:
            print("Download {}...".format(tmp_path))
            while True:
                tmp_response = requests.get(tmp_path)
                if tmp_response.ok:
                    break
            print("...finished")
            if "zip" in tmp_path:
                tmp_zip = zipfile.ZipFile(io.BytesIO(tmp_response.content))
                tmp_zip.extractall(path = PATH_RES_INPUT)
            else:
                tmp_content = tmp_response.text
                tmp_posix_path = PurePosixPath(tmp_path)
                tmp_filename = tmp_posix_path.stem
                tmp_input_file_path = PATH_RES_INPUT / Path("cup_{}".format(tmp_filename)) / Path("embedded")
                if not tmp_input_file_path.is_dir():
                    tmp_input_file_path.mkdir(parents = True)
                tmp_input_file_path = tmp_input_file_path / Path("{}.cup".format(tmp_filename))
                try:
                    with codecs.open(tmp_input_file_path,"w+","ISO-8859-1") as tmp_file:
                        tmp_file.write(tmp_content)
                except:
                    with codecs.open(tmp_input_file_path,"w+","utf-8") as tmp_file:
                        tmp_file.write(tmp_content)
    
    #Create the waypoint-file
    input_files_list = []
    for tmp_dir in PATH_RES_INPUT.glob("*/*"):
        if "embedded" in str(tmp_dir) and "cup" in str(tmp_dir):
            tmp_dir_list = list(tmp_dir.glob("**/*.cup"))
            tmp_dir_file = tmp_dir_list[0]
            input_files_list.append(tmp_dir_file)
    
    FIRST_LINE = "name,code,country,lat,lon,elev,style,rwdir,rwlen,freq,desc"
    
    output_lines = []
    output_lines.append(FIRST_LINE)
    
    for input_file in input_files_list:
        print("Add Waypoints from {} to list...".format(input_file))
        with codecs.open(input_file,"r","ISO-8859-1") as tmp_file:
        #with codecs.open(input_file,"r","utf-8") as tmp_file:
            content = tmp_file.read()
            linewise_content = content.split("\n")
            for line_num, line in enumerate(linewise_content):
                if line_num == 0:
                    continue
                else:
                    if not line in output_lines:
                        output_lines.append(line)
        print("...finished")
    
    print("Write waypoints to target-file...")
    with codecs.open(PATH_RES_WAYPOINTS_OUTPUT_FILE,"w+","utf-8") as tmp_file:
        for line_num, line in enumerate(output_lines):
            if not line_num == 0:
                try:
                    parsed_line = parse_line(line, waypoint_styles)
                    if parsed_line:
                        tmp_file.write("{}\n".format(parsed_line))
                except:
                    print("WARNING: Parsing the following line failed:\n{} (this line might be empty)".format(line))
            else:
                tmp_file.write("{}\n".format(line))
    print("...finished\nSaved file under\n{}".format(PATH_RES_WAYPOINTS_OUTPUT_FILE))

    #Create the airspace file
    input_files_list = []
    for tmp_dir in PATH_RES_INPUT.glob("*/*"):
        if "embedded" in str(tmp_dir) and "openair_" in str(tmp_dir):
            tmp_dir_list = list(tmp_dir.glob("**/*.txt"))
            for tmp_file in tmp_dir_list:
                if "seeyou.openair" in str(tmp_file):
                    input_files_list.append(tmp_file)
    
    airspaces_definitions = []
    airspaces_names = []
    duplicates_counter = 0

    for input_file in input_files_list:
        print("Add airspaces from {} to list...".format(input_file))
        with codecs.open(input_file,"r","ISO-8859-1") as tmp_file:
            content = tmp_file.read()
            first_airspace_occurence = content.find("AC ")
            content = content[first_airspace_occurence:]
            blockwise_content = content.split("\r\nAC")
            for airspace_block in blockwise_content:
                if not airspace_block[0:2] == "AC":
                    airspace_block = "AC{}".format(airspace_block)
                airspace_name_begin = airspace_block.find("AN")
                airspace_name_end = airspace_block[airspace_name_begin:].find("\r\n") + airspace_name_begin
                airspace_name = airspace_block[airspace_name_begin+3:airspace_name_end]
                if not airspace_name in airspaces_names:
                    airspaces_names.append(airspace_name)
                    airspaces_definitions.append(airspace_block)
                elif not airspace_block in airspaces_definitions:
                    airspaces_names.append(airspace_name)
                    airspaces_definitions.append(airspace_block)
                    print("WARNING: {} appeared multiple times!".format(airspace_name))
                else:
                    duplicates_counter = duplicates_counter + 1
        print("...finished")

    airspaces_in_list = len(airspaces_definitions)
    print("{} airspaces in list and {} duplicates were found.".format(airspaces_in_list, duplicates_counter))

    print("Write airspaces to target-file...")
    with codecs.open(PATH_RES_AIRSPACES_OUTPUT_FILE,"w+","utf-8") as tmp_file:
        blocks_written = 0
        for airspace_block in airspaces_definitions:
            tmp_file.write("{}\n\n".format(airspace_block))
            blocks_written = blocks_written + 1
            if blocks_written % 100 == 0:
                print("{}/{} written to target file...".format(blocks_written, airspaces_in_list))
    print("...finished\nSaved file under\n{}".format(PATH_RES_AIRSPACES_OUTPUT_FILE))