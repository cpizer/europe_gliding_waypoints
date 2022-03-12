import sys
import datetime
from pathlib2 import *
import requests
import zipfile
import io
import codecs
import numpy as np

PATH_CUP_BELGIUM = "http://snapshots.openflightmaps.org/live/2006/cup/ebbu/latest/cup_eb.zip"
PATH_OA_BELGIUM = "http://snapshots.openflightmaps.org/live/2006/openair/ebbu/latest/openair_eb.zip"
PATH_CUP_GERMANY = "http://snapshots.openflightmaps.org/live/2006/cup/ed/latest/cup_germany.zip"
PATH_OA_GERMANY = "http://snapshots.openflightmaps.org/live/2006/openair/ed/latest/openair_ed.zip"
PATH_CUP_FINLAND = "http://snapshots.openflightmaps.org/live/2006/cup/efin/latest/cup_ef.zip"
PATH_CUP_FINLAND = "http://snapshots.openflightmaps.org/live/2006/openair/efin/latest/openair_ef.zip"
PATH_CUP_NEDERLAND = "http://snapshots.openflightmaps.org/live/2006/cup/ehaa/latest/cup_eh.zip"
PATH_OA_NEDERLAND = "http://snapshots.openflightmaps.org/live/2006/openair/ehaa/latest/openair_eh.zip"
PATH_CUP_DENMARK = "http://snapshots.openflightmaps.org/live/2006/cup/ekdk/latest/cup_ek.zip"
PATH_OA_DENMARK = "http://snapshots.openflightmaps.org/live/2006/openair/ekdk/latest/openair_ek.zip"
PATH_CUP_POLAND = "http://snapshots.openflightmaps.org/live/2006/cup/epww/latest/cup_ep.zip"
PATH_OA_POLAND = "http://snapshots.openflightmaps.org/live/2006/openair/epww/latest/openair_ep.zip"
PATH_CUP_SWEDEN = "http://snapshots.openflightmaps.org/live/2006/cup/esaa/latest/cup_es.zip"
PATH_OA_SWEDEN = "http://snapshots.openflightmaps.org/live/2006/openair/esaa/latest/openair_es.zip"
PATH_CUP_BULGARIA = "http://snapshots.openflightmaps.org/live/2006/cup/lbsr/latest/cup_bulgaria.zip"
PATH_OA_BULGARIA = "http://snapshots.openflightmaps.org/live/2006/openair/lbsr/latest/openair_lb.zip"
PATH_CUP_CROATIA = "http://snapshots.openflightmaps.org/live/2006/cup/ldzo/latest/cup_ld.zip"
PATH_OA_CROATIA = "http://snapshots.openflightmaps.org/live/2006/openair/ldzo/latest/openair_ld.zip"
PATH_CUP_GREECE = "http://snapshots.openflightmaps.org/live/2006/cup/lggg/latest/cup_lg.zip"
PATH_OA_GREECE = "http://snapshots.openflightmaps.org/live/2006/openair/lggg/latest/openair_lg.zip"
PATH_CUP_HUNGARY = "http://snapshots.openflightmaps.org/live/2006/cup/lhcc/latest/cup_hungary.zip"
PATH_OA_HUNGARY = "http://snapshots.openflightmaps.org/live/2006/openair/lhcc/latest/openair_lh.zip"
PATH_CUP_ITALY = "http://snapshots.openflightmaps.org/live/2006/cup/li/latest/cup_li.zip"
PATH_OA_ITALY = "http://snapshots.openflightmaps.org/live/2006/openair/li/latest/openair_li.zip"
PATH_CUP_SLOVENIA = "http://snapshots.openflightmaps.org/live/2006/cup/ljla/latest/cup_slovenia.zip"
PATH_OA_SLOVENIA = "http://snapshots.openflightmaps.org/live/2006/openair/ljla/latest/openair_lj.zip"
PATH_CUP_CZECH = "http://snapshots.openflightmaps.org/live/2006/cup/lkaa/latest/cup_lk.zip"
PATH_OA_CZECH = "http://snapshots.openflightmaps.org/live/2006/openair/lkaa/latest/openair_lk.zip"
PATH_CUP_AUSTRIA = "http://snapshots.openflightmaps.org/live/2006/cup/lovv/latest/cup_austria.zip"
PATH_OA_AUSTRIA = "http://snapshots.openflightmaps.org/live/2006/openair/lovv/latest/openair_lo.zip"
PATH_CUP_ROMANIA = "http://snapshots.openflightmaps.org/live/2006/cup/lrbb/latest/cup_romania.zip"
PATH_OA_ROMANIA = "http://snapshots.openflightmaps.org/live/2006/openair/lrbb/latest/openair_lr.zip"
PATH_CUP_SWITZERLAND = "http://snapshots.openflightmaps.org/live/2006/cup/lsas/latest/cup_switzerland.zip"
PATH_OA_SWITZERLAND = "http://snapshots.openflightmaps.org/live/2006/openair/lsas/latest/openair_ls.zip"
PATH_CUP_SLOVAKIA = "http://snapshots.openflightmaps.org/live/2006/cup/lzbb/latest/cup_lz.zip"
PATH_OA_SLOVAKIA = "http://snapshots.openflightmaps.org/live/2006/openair/lzbb/latest/openair_lz.zip"
PATH_CUP_FRANCE = "http://download.xcsoar.org/content/waypoint/country/FR.cup"
PATH_OA_FRANCE = ""

PATH_CWD = Path.cwd()

path_list = [PATH_CUP_FRANCE, PATH_CUP_AUSTRIA, PATH_CUP_BELGIUM, PATH_CUP_BULGARIA, PATH_CUP_CROATIA, 
    PATH_CUP_CZECH, PATH_CUP_DENMARK, PATH_CUP_FINLAND, PATH_CUP_GERMANY, PATH_CUP_GREECE,
    PATH_CUP_HUNGARY, PATH_CUP_ITALY, PATH_CUP_NEDERLAND, PATH_CUP_POLAND, PATH_CUP_ROMANIA,
    PATH_CUP_SLOVAKIA, PATH_CUP_SLOVENIA, PATH_CUP_SWEDEN, PATH_CUP_SWITZERLAND, 
    PATH_OA_AUSTRIA, PATH_OA_BELGIUM, PATH_OA_BULGARIA, PATH_OA_CROATIA, PATH_OA_CZECH, PATH_OA_DENMARK, 
    PATH_OA_GERMANY, PATH_OA_GREECE, PATH_OA_HUNGARY, PATH_OA_ITALY, PATH_OA_NEDERLAND, PATH_OA_POLAND, 
    PATH_OA_ROMANIA, PATH_OA_SLOVAKIA, PATH_OA_SLOVENIA, PATH_OA_SWEDEN, PATH_OA_SWITZERLAND]

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
    FILENAME_OUTPUT_FILE = "worldwide_{}.cup".format(datetime.date.today().isoformat().replace("-","_"))
    PATH_RES_OUTPUT_FILE = PATH_RES_OUTPUT / Path(FILENAME_OUTPUT_FILE)

    waypoint_styles = []
    if len(sys.argv) > 1:
        for i in range(2,len(sys.argv)):
            if sys.argv[i].isnumeric():
                waypoint_styles.append(int(sys.argv[i]))
            else:
                print("WARNING: '{}' is not a valid command line argument!!!")
    
    if not PATH_RES_INPUT.is_dir():
        PATH_RES_INPUT.mkdir(parents = True)
    
    if not PATH_RES_OUTPUT.is_dir():
        PATH_RES_OUTPUT.mkdir(parents = True)
    
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
    with codecs.open(PATH_RES_OUTPUT_FILE,"w+","utf-8") as tmp_file:
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
    print("...finished\nSaved file under\n{}".format(PATH_RES_OUTPUT_FILE))
