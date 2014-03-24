from googleads import dfp, oauth2
oauth2_client = oauth2.GoogleRefreshTokenClient(
        client_id='THIS_IS_THE_CLIENT_ID_GENERATED_DURING_THE_OAUTH_PROCESS',
        client_secret='THIS_IS_CLIENT_SECRET',
        refresh_token='this_is_refresh_token_required_for_refreshing_access_token'
       )
client = dfp.DfpClient(oauth2_client, 'google_dfp_prod')
networks = client.GetService('NetworkService').getAllNetworks()
network = networks[0]['networkCode']
print "Network code : %s" % network
client = dfp.DfpClient(oauth2_client,'google_dfp_prod', network)
