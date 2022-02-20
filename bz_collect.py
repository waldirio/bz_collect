#!/usr/bin/env python
"""
Code used to collect information from BZ via API

License .......: GPL3
Developer .....: Waldirio M Pinheiro <waldirio@gmail.com> | <waldirio@redhat.com>
Date ..........: 02/19/2022
Purpose .......: Extract the BZ information, the customer can see all the products available, pick one up
                 and generate the output file, that will be in CSV format. Note that this output will include
                 some fields from BZ, including also the # of cases attached to each BZ.
"""

# from email import header
import sys
import os
import json
import csv
from datetime import date
# from pydoc import doc
from time import sleep
import requests

TODAY = date.today()
TODAY_STR = TODAY.strftime("%Y-%m-%d")

bz_list = []
bz_final_list = []
product_list = []

header_dic = {}


def query(location):
    """
    Responsible to query the API endpoint and return all the objects found.
    """

    stage_lst = []

    r = requests.get(location, verify=True, headers=header_dic)
    result = json.loads(r.content)

    check_response = divmod(result['total_matches'], 20)
    print("# of BZs: {}".format(result['total_matches']))

    if check_response[1] == 0:
        num_of_pages = check_response[0] + 1
    else:
        num_of_pages = check_response[0] + 2

    offset_value = 0
    for position in range(1, num_of_pages):
        url = location + "&offset=" + str(offset_value) + "&limit=20"
        r = requests.get(url, verify=True, headers=header_dic)
        temporary = json.loads(r.content)

        for element in temporary['bugs']:

            stage_lst.append(element)
        print(url)

        offset_value = offset_value + 20

    return stage_lst


def print_file(product_name):
    """
    Def used to generate the output file / dataset
    By dafault, out.csv
    """

    print("saving the file")

    # Header
    stage_var = "load_data", \
                "bz_id", \
                "product", \
                "component", \
                "status", \
                "resolution", \
                "summary", \
                "version", \
                "keywords", \
                "creator", \
                "severity", \
                "create_time", \
                "close_time", \
                "customer_case_attached"

    bz_final_list.insert(0, stage_var)
    stage_var = ""

    # Setting the filename as the <product name>.csv
    OUTPUT_FILE_NAME = product_name + ".csv"

    with open(OUTPUT_FILE_NAME, 'w') as csvfile:
        for item in bz_final_list:
            f = csv.writer(csvfile)
            f.writerow(item)
    print("Done, file '{}' created.".format(OUTPUT_FILE_NAME))
    input("press any key to continue")


def check_links(bz_id):
    """
    Count the # of cases attached to the BZ
    """

    url = "https://bugzilla.redhat.com/rest/bug?id=" + str(bz_id) + "&include_fields=external_bugs"
    r = requests.get(url, verify=True, headers=header_dic)
    parse = json.loads(r.content)

    count = 0
    for bug in parse['bugs'][0]['external_bugs']:
        # print(bug)
        type_extenal_issue = bug['type'].get('description')
        # id_external_issue = bug.get('ext_bz_bug_id')
        # status_external_issue = bug.get('ext_status')
        if type_extenal_issue == "Red Hat Customer Portal":
            count = count + 1

    # Sending back the # of attached cases to this specific BZ
    return count


def count_external_links():
    """
    Check all the links associated to the BZ
    """

    print("Counting external links")
    stage_lst = []

    for element in bz_list:
        bz_id = element[1]
        print("Checking attached cases from BZ {}".format(bz_id))
        num_of_cases = check_links(bz_id)
        stage_lst = list(element)
        stage_lst.append(num_of_cases)

        bz_final_list.append(stage_lst)
        stage_lst = []


def collecting_exporting_data():
    """
    Collecting the information via API
    """

    global bz_list
    global bz_final_list
    bz_list = []
    bz_final_list = []

    if len(product_list) == 0:
        print("You have to 'List all the Products available on BugZilla' first, after that, pick the number and return to this option")
        sleep(3)
    else:

        product_id = int(input("Please, type the product id and press enter: "))

        count = 0
        for id in product_list:
            if product_id == int(id[0]):
                product_name = id[2]
                count = count + 1

        if count == 0:
            print("Invalid ID, please, try again")
            sleep(3)
        else:

            GENERIC_URL = "https://bugzilla.redhat.com/rest/bug?product=" + str(product_name) + "&status=all open,all closed"

            print(GENERIC_URL)
            obj = query(GENERIC_URL)
            for data in obj:

                aux = str(data['component'])
                component_str = aux.replace("'", "")
                # print("component: {}".format(component_str))

                aux = str(data['summary'])
                summary_str = aux.replace("'", "''")
                # print("summary: {}".format(summary_str))

                aux = str(data['version'])
                version_str = aux.replace("'", "")
                # print("version: {}".format(version_str))

                aux = str(data['keywords'])
                keywords_str = aux.replace("'", "")
                # print("keywords: {}".format(keywords_str))

                aux = str(data['creator'])
                creator_str = aux.replace("'", "''")
                # print("creator: {}".format(creator_str))

                stage_var = TODAY_STR, \
                    data['id'], \
                    data['product'], \
                    component_str, \
                    data['status'], \
                    data['resolution'], \
                    summary_str, \
                    version_str, \
                    keywords_str, \
                    creator_str, \
                    data['severity'], \
                    data['creation_time'], \
                    data['cf_last_closed']

                bz_list.append(stage_var)

            count_external_links()
            print_file(product_name)


def query_list_of_products():
    print("retrieving the list of products")
    location = "https://bugzilla.redhat.com/rest/product_accessible"


    # location = "https://bugzilla.redhat.com/rest/product?ids=286&ids=564"

    # stage_lst = []

    # r = requests.get(location, verify=False)
    r = requests.get(location, verify=True, headers=header_dic)
    # r = requests.get(url, verify=True, headers = header_dic)

    # r = requests.get(location, verify=False, auth=(USER, PASSWORD))
    result = json.loads(r.content)

    #  For debug purpose
    # result = {
    #             "ids": [
    #                 "286",
    #                 "564"
    #             ]
    #             }

    # total_items = parse['total_matches']

    # response = query(location)
    count = 0
    print("id    status          product")
    for product_id in result['ids']:
        location = "https://bugzilla.redhat.com/rest/product?ids=" + str(product_id)
        r = requests.get(location, verify=True, headers=header_dic)
        result = json.loads(r.content)
        status = result['products'][0]['classification']
        product_name = result['products'][0]['name']

        if status != "Retired":
            product_list.append([product_id, status, product_name])
            print("{:5} {:15} {}".format(product_id, status, product_name))
            count = count + 1


    print("Please, take the ID above from the product that you would like to export.")
    print("Also, feel free to copy/paste the information above, then you can")
    print("export content of different products.")
    print("")
    print("Total of {} products".format(count))
    input("press any key to continue")


def user_menu():
    """
    User menu to help during the data extraction
    """
    while True:
        os.system("clear")
        print("#######################")
        print("# 1. List all the Products available on BugZilla")
        print("# 2. Export the BZ information")
        print("#")
        print("# 0. Exit")
        print("#######################")
        opt = int(input("Type your Selection: "))

        if opt == 0:
            print("Exiting ...")
            sys.exit()
        elif opt == 1:
            query_list_of_products()
        elif opt == 2:
            print("Exporting")
            # bz_list = []
            # bz_final_list = []
            collecting_exporting_data()
        else:
            print("Unknown option")
            sleep(3)


def read_api_key():
    """
    Responsible for read the conf file and consume the API KEY
    """
    global header_dic

    print("Reading the file ~/.bz_api_key")
    home = os.path.expanduser("~")
    CONF_FILE = home + "/.bz_api_key"
    try:
        with open(CONF_FILE, "r") as file:
            for line in file:
                # print(line)
                API_KEY = line.rstrip()
        header_dic = {"Authorization": "Bearer " + API_KEY}
    except:
        print("file not found")
        sys.exit(2)

    try:
        location = "https://bugzilla.redhat.com/rest/product?ids=286"
        r = requests.get(location, verify=True, headers=header_dic)
        result = json.loads(r.content)
        status = result['products'][0]['classification']
    except:
        print("Please, use a valid API key")
        print("exiting ....")
        sys.exit(3)


def main():
    """
    Main definition

    The main idea of this code is request the BZ's opened and closed
    of Red Hat Satellite 6
    """

    read_api_key()
    user_menu()


if __name__ == "__main__":
    main()
