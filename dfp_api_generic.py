import datetime
import os
import sys
import ast
import csv
import argparse
import dfp_config
from googleads import dfp, oauth2
from suds.sudsobject import asdict
import json

import ConfigParser
config = ConfigParser.ConfigParser()
config.read('dfp_param.py')
print config.sections()
#print config.get('Order','columns')

def recursive_asdict(d):
    """Convert Suds object into serializable format."""
    out = {}
    for k, v in asdict(d).iteritems():
        if hasattr(v, '__keylist__'):
            out[k] = recursive_asdict(v)
        elif isinstance(v, list):
            out[k] = []
            for item in v:
                if hasattr(item, '__keylist__'):
                    out[k].append(recursive_asdict(item))
                else:
                    out[k].append(item)
        else:
            out[k] = v
    return out

HOME = os.path.expanduser('~')

parser = argparse.ArgumentParser(description='Generic script for XSM data download.')
parser.add_argument('-a','--api_name', help='This is the api name, for example: Proposal',required=True)
args = parser.parse_args()
print ("api name: %s" % args.api_name)

#DEFAULT_API_VERSION = 'v201403'
page_size = 500
offset, result_set_size = 0, 0

def _ConvertDateFormat(date_time_value):
  """Converts Dict of date to datetime format suitable for Teradata"""
  if date_time_value is None:
    date_time_obj = ''
  else:
    date_time_obj = datetime.datetime(int(date_time_value['date']['year']),
                                      int(date_time_value['date']['month']),
                                      int(date_time_value['date']['day']),
                                      int(date_time_value['hour']),
                                      int(date_time_value['minute']),
                                      int(date_time_value['second']))
  return date_time_obj

"""col = config.get('Order','columns').split('|')
print col
cols = []
for i in col:
  cols.append([i])
"""

def loop_thru(results):
  #if args.api_name == 'Order':
    f = open(config.get(args.api_name,'filename'), "wb+")
    for res in results:
        # -- recursive_asdict is used for serializing a suds object. The result is a Json --
        data = recursive_asdict(res)
        #input = eval('cols')
        if args.api_name == 'Order':
          input = [data['advertiserId'],data['id'],data['name'].encode('utf8'),data['traffickerId'],data.get('secondaryTraffickerIds',''),data.get('salespersonId',''),data['totalClicksDelivered'],data['totalImpressionsDelivered'],_ConvertDateFormat(data['startDateTime']),_ConvertDateFormat(data.get('endDateTime',None)),_ConvertDateFormat(data['lastModifiedDateTime']),data['currencyCode'],data['status']]
        #print "%s,%s,%s,%s" % (data['id'],data['name'],getattr(data,'secondaryTraffickerIds',''),_ConvertDateFormat(data['lastModifiedDateTime']))
        if args.api_name == 'Advertiser':
          input = [data['id']]
	tmp = [[]]
	for i in input:
    	  if isinstance(i, list):
            tmp = [j+[k] for j in tmp for k in i]
          else:
            tmp = [j+[i] for j in tmp]
	#output = ["|".join(i) for i in tmp]
	output = ["|".join(map(str, i)) for i in tmp] 
        print output
	for doutput in output:
          f.write("%s\n" % doutput)

DEFAULT_API_VERSION = config.get('DEFAULT','API_VERSION')
PAGESIZE = config.get('DEFAULT','page_size')
#OFFSET = config.get('DEFAULT','offset')
print 'Using DFP Api Version: %s , Page size : %s , Starting Offset ' % (DEFAULT_API_VERSION,PAGESIZE)

service_stmt = config.get(args.api_name,'dfpservice')
#dfpresponse = getCompaniesByStatement
dfpstmt = config.get(args.api_name,'dfpstmt')
service = eval('dfp_config.client.GetService(\'%s\', version=DEFAULT_API_VERSION)' % service_stmt)
print service
while True:
  filter_statement = {'query': 'WHERE lastModifiedDateTime > \'2014-03-20T17:00:00\' LIMIT %s OFFSET %s' % (page_size,offset) }
  #filter_statement = {'query': 'WHERE Id in ( 201777742, 173301622, 158356102,158355982) and lastModifiedDateTime > \'2014-03-16T17:00:00\' LIMIT %s OFFSET %s' % (page_size,offset) }
  #filter_statement = {'query': 'WHERE lastModifiedDateTime > \'2014-03-16T17:00:00\' LIMIT %s OFFSET %s' % (page_size,offset) }
  print filter_statement
  response = eval('service.%s(filter_statement)' % dfpstmt)
  print response
  if not response:
    sys.exit(1)
  results = response['results']
  loop_thru(results)
  result_set_size = len(results)
  offset += result_set_size
  if result_set_size != page_size:
	break
  if offset == 0:
    print 'No records Found'
    sys.exit(1)

print 'Number of results found: %d' % offset
