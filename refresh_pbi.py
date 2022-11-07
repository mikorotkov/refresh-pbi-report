from msal import PublicClientApplication
import requests
import os
#from airflow.models import Variable

def refresh_pbi_report(**kwargs):
    # TO DO combine  get_group_id and get_dataset_id
    def get_group_id(app_name,header):
        """ Receives app_name (written exactly as in PBI interface) and header for HTTP request. Returns group_id if match for the name is found
        """
        #TO DO: Add error handling if name doesn't match 
        request_url='https://api.powerbi.com/v1.0/myorg/groups'
        r = requests.get(url=request_url, headers=header)
        r.raise_for_status()
        groups_json=r.json().get('value')
        for app in groups_json:
            if app_name.lower()==app['name'].lower():
                return app['id']
            else:
                continue

    def get_dataset_id(group_id,dataset_name,header):
        """ Receives dataset_name (written exactly as in PBI interface), group_id of the group in which the dataset is present and header for HTTP request. 
        Returns dataset_id if match for the name is found
        """
        #TO DO: Add error handling if name doesn't match 
        request_url=f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets'
        r = requests.get(url=request_url, headers=header)
        r.raise_for_status()
        datasets_json=r.json().get('value')
        for dataset in datasets_json:
            if dataset_name.lower()==dataset['name'].lower():
                return dataset['id']
            else:
                continue


    app_name=kwargs['pbi_app']
    dataset_name=kwargs['name']

    authority_url='https://login.microsoftonline.com/organizations/'
   

    #set password and user in os variables https://www.youtube.com/watch?v=IolxqkL7cD8
    username = os.environ.get('PBI_USER')
    password = os.environ.get('PBI_PASSWORD')
    client_id = os.environ.get('CLIENT_ID')



    context=PublicClientApplication(client_id=client_id,authority=authority_url)
    scope=['https://analysis.windows.net/powerbi/api/Dataset.ReadWrite.All','https://analysis.windows.net/powerbi/api/Report.Read.All']
    token = context.acquire_token_by_username_password(  scopes=scope,
                                                        username=username,
                                                        password=password)                                                    
    access_token = token.get('access_token')
    header = {'Authorization': f'Bearer {access_token}'}



    group_id=get_group_id(app_name,header)
    dataset_id=get_dataset_id(group_id,dataset_name,header)


    refresh_url = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/refreshes'

    r = requests.post(url=refresh_url, headers=header) #POST to refresh the report
    r.raise_for_status()