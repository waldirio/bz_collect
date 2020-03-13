#!/usr/bin/env python
"""
Code used to collect information from BZ via API
"""

import json
import csv
from datetime import date
import requests
from postgres import Postgres

URL = "https://bugzilla.redhat.com/rest/bug?"
# URL_AUX="https://bugzilla.redhat.com/rest/bug?id=1771508,1209702"
URL_AUX = "https://bugzilla.redhat.com/rest/bug?product=Red Hat Satellite 6&status=all closed&version=6.7.0"
SAT_65 = "%sproduct=Red Hat Satellite 6&status=all open,all closed&version=6.5.0" % URL
SAT_66 = "%sproduct=Red Hat Satellite 6&status=all open,all closed&version=6.6.0" % URL
SAT_67 = "%sproduct=Red Hat Satellite 6&status=all open,all closed&version=6.7.0" % URL

TODAY = date.today()
TODAY_STR = TODAY.strftime("%Y-%m-%d")

bz_list = []

# print("DATE: {}".format(date.today()))


def query(location):
    """
    Def used to execute the query on the remote website
    """

    r = requests.get(location, verify=False)
    parse = json.loads(r.content)
    return parse


def print_file():
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
                "close_time"

    bz_list.insert(0, stage_var)

    with open('out.csv', 'w') as csvfile:
        for item in bz_list:
            #print("here: {}".format(item))
            f = csv.writer(csvfile)
            f.writerow(item)
        print("Done, file saved.")


def dump_db():
    """
    Def used to save the data on Postgres DB/Table
    Note, here you can see the info as below
    "postgresql://bz_user:bz_user_00@server_running_postgres/bz" where
    ---
    Username ........: bz_user
    Password ........: bz_user_00
    Server FQDN .....: server_running_postgres
    Database ........: bz
    ---
    """

    print("Updating DB")
    db = Postgres(url='postgresql://bz_user:bz_user_00@server_running_postgres/bz')
    db.run("delete from bz_info")
    for item in bz_list:
        print("ID here: {}".format(item[1]))
        db.run("insert into bz_info values('" + TODAY_STR +
               "','" + str(item[1]) +
               "','" + str(item[2]) +
               "','" + str(item[3]) +
               "','" + str(item[4]) +
               "','" + str(item[5]) +
               "','" + str(item[6]) +
               "','" + str(item[7]) +
               "','" + str(item[8]) +
               "','" + str(item[9]) +
               "','" + str(item[10]) +
               "','" + str(item[11]) +
               "','" + str(item[12]) +
               "')")


def main():
    """
    Main definition

    The main idea of this code is request the BZ's opened and closed
    of Satellite 6.5, 6.6 and 6.7
    """

    for sat_ver in [SAT_65, SAT_66, SAT_67]:
    # for sat_ver in [URL_AUX]:
        print("Collecting from: {}".format(sat_ver))
        obj = query(sat_ver)
        for data in obj['bugs']:
            # print("id: {}".format(data['id']))
            # print("product: {}".format(data['product']))

            aux = str(data['component'])
            component_str = aux.replace("'", "")
            # print("component: {}".format(component_str))

            # print("status: {}".format(data['status']))
            # print("resolution: {}".format(data['resolution']))

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
            # print("severity: {}".format(data['severity']))

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

    print_file()
#    dump_db()


if __name__ == "__main__":
    main()
