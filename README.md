# bz_collect

This project will help you to collect BugZilla information via API.

You can download the binary version in the Releases area (right side). In this case, no virtual environment or additional steps will be necessary.

About the use, please, proceed as below

 - Download the BZ API key from [here](https://bugzilla.redhat.com/userprefs.cgi?tab=apikey)
 - Download the latest version of the binary [here](https://github.com/waldirio/bz_collect/releases/latest)
 - Create a file in your home directory, called `~/.bz_api_key` and add ONLY your `API Key` to this file.

 At this moment, you will be good to go and run the app.

 ```
 $ ./bz_collect
 ```
 and it will result in an output as below
 ```
 #######################
# 1. List all the Products available on BugZilla
# 2. Export the BZ information
#
# 0. Exit
#######################
Type your Selection: 
 ```

The first step is type `1` and press enter. This option will bring back the whole products available on Bugzilla.
```
######################
# 1. List all the Products available on BugZilla
# 2. Export the BZ information
#
# 0. Exit
#######################
Type your Selection: 1
retrieving the list of products
id    status          product
  172 Internal        AMS
  555 Red Hat         AROS
  296 Internal        Automation Portal
  288 Internal        Brewtap
  ...
  379 Community       softwarecollections.org
  427 oVirt           vdsm
  428 oVirt           vdsm-jsonrpc-java
Please, take the ID above from the product that you would like to export.
Also, feel free to copy/paste the information above, then you can
export content of different products.

Total of 225 products
press any key to continue
```
Keep in mind that you can copy/paste the list above and if you would like to export more than 1 product, you just need to know the `id` presented above. After that, you can press enter and it will return to the main menu.

The next step will be typing 2 and pressing enter. After, you can type the `id` of the product you would like to export and press enter once again. Below we can see an example.
```
#######################
# 1. List all the Products available on BugZilla
# 2. Export the BZ information
#
# 0. Exit
#######################
Type your Selection: 2
Exporting
Please, type the product id and press enter: 286
https://bugzilla.redhat.com/rest/bug?product=Gofer&status=all open,all closed
# of BZs: 16
https://bugzilla.redhat.com/rest/bug?product=Gofer&status=all open,all closed&offset=0&limit=20
Counting external links
Checking attached cases from BZ 799057
Checking attached cases from BZ 799061
Checking attached cases from BZ 799064
Checking attached cases from BZ 829767
Checking attached cases from BZ 952251
Checking attached cases from BZ 1022428
Checking attached cases from BZ 1023420
Checking attached cases from BZ 1097732
Checking attached cases from BZ 1100821
Checking attached cases from BZ 1100864
Checking attached cases from BZ 1101520
Checking attached cases from BZ 1102749
Checking attached cases from BZ 1107244
Checking attached cases from BZ 1129828
Checking attached cases from BZ 1192563
Checking attached cases from BZ 1737814
saving the file
Done, file 'Gofer.csv' created.
press any key to continue
```
Note. If you would like to export data about a different product, just type `2` once again, type the code and press enter.

Great, at this moment, a file with the product name will be created. Here we can see `Gofer.csv` and checking the content of this file, we can see some fields. Below it's an example.
```
$ cat Gofer.csv 
load_data,bz_id,product,component,status,resolution,summary,version,keywords,creator,severity,create_time,close_time,customer_case_attached
2022-02-19,799057,Gofer,[Security],VERIFIED,,[RFE] Add support for HMAC message authentication,[unspecified],[],jortel@redhat.com,unspecified,2012-03-01T16:42:11Z,,0
2022-02-19,1192563,Gofer,[python-gofer],MODIFIED,,[RFE] Validate certificate path and report when files do not exists or have insufficient permissions.,[unspecified],[],jortel@redhat.com,medium,2015-02-13T17:29:32Z,,0
2022-02-19,1737814,Gofer,[goferd],NEW,,False alarms raised by qdrouterd when stopping or restarting goferd,[unspecified],[Triaged],pmoravec@redhat.com,medium,2019-08-06T09:28:02Z,,5
...
```
After that, you can import this data in your best SpreadSheet and play with it.




If you would like to play with the code and/or contribute, I really recommend you to prepare a virtual environment, install all the python modules according to the `requirement.txt` file and then voilá, you will be able to run it.

Note, there is a script called `start_here.sh` where this will load the virtual environment and will run the script. Attention, some changes on the file will be required.


I really hope you enjoy it.

Waldirio
