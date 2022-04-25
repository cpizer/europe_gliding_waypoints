import requests
from bs4 import BeautifulSoup
import datetime
import io
import xml.etree.ElementTree as ET

def get_regions_hrefs():
    #This function retrieves all regions' hrefs based on the dropdown menu on the openflightmaps-start-page
    while True:
        tmp_response = requests.get("https://www.openflightmaps.org/")
        if tmp_response.ok:
            break
    
    regions_hrefs = []

    soup = BeautifulSoup(tmp_response.text, features="html.parser")
    li_list = soup.find_all("li")
    for tmp_li in li_list:
        if tmp_li.find_all("a", id="regionsTitle"):
            a_list = tmp_li.find_all("a")
            for tmp_a in a_list:
                if "href" in tmp_a.attrs:
                    regions_hrefs.append(tmp_a.attrs["href"])
    
    return regions_hrefs

def get_regions_codes():
    #This function retrieves all regions' codes and returns them as a list of strings
    region_hrefs = get_regions_hrefs()
    region_codes = []

    for href in region_hrefs:
        #print("Get region code of {}...".format(href))
        while True:
            tmp_response = requests.get(href)
            if tmp_response.ok:
                break

        soup = BeautifulSoup(tmp_response.text, features="html.parser")
        script_list = soup.find_all("script")
        for tmp_script in script_list:
            tmp_script_str = str(tmp_script)
            #print(tmp_script_str)
            if "var regionCode" in tmp_script_str:
                #print(tmp_script_str)
                for tmp_line in tmp_script_str.split("\n"):
                    if "var regionCode" in tmp_line:
                        region_code_begin = tmp_line.find("\"")+1
                        region_code_end = region_code_begin + tmp_line[region_code_begin:].find("\"")
                        region_code = tmp_line[region_code_begin:region_code_end]
                        region_codes.append(region_code)
                        break
    
    return region_codes

def get_current_airac_id():
    #This function generates the current AIRAC-ID and returns it as an integer
    dateVal = datetime.date.today()
    cDate = datetime.date(2003, 1, 23)
    counter = 0
    lastCount = 0
    year = dateVal.year
    while cDate < dateVal:
        if cDate.year == dateVal.year - 1:
            lastCount = lastCount + 1
        if cDate.year == dateVal.year:
            counter = counter + 1
        cDate = cDate + datetime.timedelta(days=28)
    if counter == 0:
        year = year - 1
        counter = lastCount
    id = int(str(year)[2:])*100 + counter
    return id

def get_region_product_list(regionCode):
    #This creates a dict containing all download links of a region's products
    airac = str(get_current_airac_id())
    currentdate = datetime.datetime.now()
    xml_url = 'http://snapshots.openflightmaps.org/publicationServices/' + regionCode + '_' + airac + '.xml?time=' + str(currentdate.minute) + str(currentdate.second)
    tmp_response = requests.get(xml_url)
    while True:
        if tmp_response.ok:
            break
    tmp_response.encoding = 'utf-8'
    xml_hdl = io.StringIO(tmp_response.text)
    tree = ET.parse(xml_hdl)
    root = tree.getroot()
    product_list = {}
    for tmp_item in root.findall("item"):
        tmp_type = tmp_item.get("type")
        if tmp_type == "downloads":
            for tmp_section in tmp_item.findall("section"):
                if tmp_section.get("type") == "data":
                    for tmp_product in tmp_section.findall("product"):
                        if tmp_product.find("download"):
                            tmp_type = tmp_product.get("type")
                            tmp_download_url = tmp_product.find("download").get("URL")
                            product_list[tmp_type] = tmp_download_url
    return product_list

def get_global_product_dict():
    #This function creates a dict with a nested dict for each region containing links for all available products
    print("Retrieve region codes...")
    region_codes = get_regions_codes()
    products_dict = {}
    for region_code in region_codes:
        print("Generate product list for region with code {}".format(region_code))
        product_list = get_region_product_list(region_code)
        products_dict[region_code] = product_list
    return products_dict