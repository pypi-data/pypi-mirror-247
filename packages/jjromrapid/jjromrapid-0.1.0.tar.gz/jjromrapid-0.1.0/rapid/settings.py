"""
rapid - settings.py

Default configuration connect to local docker resto endpoint 

Note that all variables can be superseeded with environnement variables with the same name

Copyright 2023 Jerome Gasperi
@author: jerome.gasperi@gmail.com
"""

config = {

    #  Endpoint to OGC API Processes service landing page
    'PROCESS_API_ENDPOINT': 'http://localhost:5252/oapi-p',
    
    # Authorization token to deploy process
    'PROCESS_API_AUTH_TOKEN': 'eyJzdWIiOiIxMDAiLCJpYXQiOjE3MDIzODg1OTIsImV4cCI6MjU2NjM4ODU5Mn0.qywT1iki4QsgZdPJTO3bWU2GuWTVf6UDs1ztaBodsk8',

}

