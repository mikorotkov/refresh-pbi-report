# Summary
This function receives dictionary that should contain arguments pbi_app (app name exactly as in PBI) and name (report name exactly as in PBI). 

It reads credentials (email and password) from environmental variables `PBI_USER`, `PBI_PASSWORD`, and `CLIENT_ID` that need to be defined in local or Google Composer environment (if used as Airflow task in Google Composer). 
It then makes a call to PBI API to first retrieve group_id based on the app name (function get_group_id) and
then retrieves dataset_id to be refreshed based on report name and group_id retrieved earlier (function get_dataset_id).

Finally it refreshes the dataset in PBI.

# Credentials for Microsoft API
I use PYPI package `msal` to use Microsoft API. Read the [documentation](https://pypi.org/project/msal/) about how to use it and set it up.