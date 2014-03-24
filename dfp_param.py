[Order]
dfpservice = OrderService
dfpstmt = getOrdersByStatement
#columns = 'advertiserId','id','name','traffickerId','secondaryTraffickerIds','salespersonId','totalClicksDelivered','totalImpressionsDelivered','startDateTime','endDateTime','lastModifiedDateTime','currencyCode','status'
#columns = data['advertiserId']|data['id']|data['name'].encode('utf8')|data['traffickerId']|data.get('secondaryTraffickerIds','')|data.get('salespersonId','')|data['totalClicksDelivered']|data['totalImpressionsDelivered']|_ConvertDateFormat(data['startDateTime'])|_ConvertDateFormat(data.get('endDateTime',None))|_ConvertDateFormat(data['lastModifiedDateTime'])|data['currencyCode']|data['status']
filename = order.output

[Advertiser]
dfpservice = CompanyService
dfpstmt = getCompaniesByStatement
columns = [a['id']]
filename = advertiser.out

[DEFAULT]
API_VERSION = v201403
page_size = 500
offset = 0
