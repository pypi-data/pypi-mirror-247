"""
rapid - process.py
Copyright 2023 Jerome Gasperi
@author: jerome.gasperi@gmail.com
"""
import requests
import jwt
import json
import os
import rapid.settings as settings

class ProcessAPI():
    
    def __init__(self, config=None):
        """
        Initialize Process class - access to resto OGC API Processes

        @params
            config          --  Superseed settings.config / environnment variables
                                Allowed variables are :
                                    RESTO_API_ENDPOINT
                                    RESTO_PROCESS_API_AUTH_TOKEN
                                    RESTO_PROCESS_API_S3_HOST
                                    RESTO_PROCESS_API_S3_BUCKET
                                    RESTO_PROCESS_API_S3_KEY
                                    RESTO_PROCESS_API_S3_SECRET
                                    RESTO_PROCESS_API_S3_REGION
        """
        
        self.config = {}
        
        configKeys = [
            'RESTO_API_ENDPOINT',
            'RESTO_PROCESS_API_AUTH_TOKEN',
            'RESTO_PROCESS_API_S3_HOST',
            'RESTO_PROCESS_API_S3_BUCKET',
            'RESTO_PROCESS_API_S3_KEY',
            'RESTO_PROCESS_API_S3_SECRET',
            'RESTO_PROCESS_API_S3_REGION'
        ]
        for key in configKeys:
            self.config[key] = os.environ.get(key) if os.environ.get(key) else settings.config[key]
            if config and key in config:
                self.config[key] = config[key]
        
        self.processAPIUrl = self.config['RESTO_API_ENDPOINT'] + '/oapi-p'
        
        
    def deploy(self, application_package):
        """
        Deploy input process as an Application Package to resto endpoint

        @params
            application_package     -- Application package
        """
        return requests.post(self.processAPIUrl + '/processes',
        	data=json.dumps(application_package),
        	headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + (self.config['RESTO_PROCESS_API_AUTH_TOKEN'] if self.config['RESTO_PROCESS_API_AUTH_TOKEN'] != None else 'none')
            }
        )

    def replace(self, process_id, application_package):
        """
        Replace process 

        @params
            process_id              -- Process identifier
            application_package     -- Application package
            
        """
        return requests.put(self.processAPIUrl + '/processes/' + process_id,
        	data=json.dumps(application_package),
        	headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + (self.config['RESTO_PROCESS_API_AUTH_TOKEN'] if self.config['RESTO_PROCESS_API_AUTH_TOKEN'] != None else 'none')
            }
        )
        
    def undeploy(self, process_id):
        """
        Undeploy process

        @params
            process_id              -- Process identifier
        """
        
        return requests.delete(self.processAPIUrl + '/processes/' + process_id,
        	headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + (self.config['RESTO_PROCESS_API_AUTH_TOKEN'] if self.config['RESTO_PROCESS_API_AUTH_TOKEN'] != None else 'none')
            }
        )
        
    def updateJob(self, token, _body):
        """
        Update a job

        @params
            token                   -- Job Process identifier
            body                    -- Job properties to update
        """
        
        # Set body from valid inputs
        body = {}
        for property in ['status', 'progress', 'result']:
            if property in _body and _body[property] != None:
                body[property]= _body[property]
        
        # Decode token to retrieve callback url
        callback = None
        try:
            jwt.decode(token, options={"verify_signature": False})
            payload = jwt.decode(token, options={"verify_signature": False})
            if 'data' in payload and 'callback' in payload['data']:
                callback = payload['data']['callback']
        except:
            pass
        
        if callback is None:
            print('[ERROR] Invalid authorization token')
            return None
        
        return requests.put(callback,
            params={'token':token},
            data=json.dumps(body),
        	headers={
                'Content-Type': 'application/json'
            }
        )