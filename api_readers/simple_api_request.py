import requests
import logging as log
import urllib
from urllib.request import urlopen
import json
from os import path, name
import datetime
import time

class simpleAPIRequest():

    animalList = []
    urlTemplate = ''
    apiName = ''
    jsonData = ''
    finalJSON = []

    def __init__(self):
        pass

    def cleanJson(self):
        cleanedJson = []

        # Topannonces API
        if self.apiName == 'topannonces':
            annonces = self.jsonData['resultats']['annonces']
            
            for annonce in annonces:
                if annonce['idAnnonce'] != '1': 
                    cleanedJson.append({
                        'titre' : annonce['titre'],
                        'commune' : annonce['commune'],
                        'texte' : annonce['texte'],
                        'url': 'https://www.topannonces.fr{}'.format(annonce['url'])
                    })
        return cleanedJson

    def launchAnalysis(self):
        try: 
            for animal in self.animalList:
                # Format URL
                tmpURL = self.urlTemplate.format(urllib.parse.urlencode({'q' : animal[0]}))  
                log.info(tmpURL)
                # Get response from request
                response = requests.get(tmpURL)
                #
                if response.status_code == 200:
                    # Get JSON
                    self.jsonData = response.json()
                    # Get only the intersting part of results
                    tmpJson = self.cleanJson()
                    self.finalJSON.append({animal[0]: tmpJson})
                #
                elif response.status_code == 403:
                    log.warning('Not authorized ?')
                #
                elif response.status_code == 404:
                    log.warning('Not existing)')
                time.sleep(2)
        # Throw error if json is malfromatted
        except json.decoder.JSONDecodeError as e:
            log.error('Malformatted json : {}'.format(e) )
        # Other technical errors
        except TypeError as e:
            log.error('Error : {}'.format(e))