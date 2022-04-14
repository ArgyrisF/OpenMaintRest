#!/usr/bin/python3

import requests, json, pprint
import os,sys
from pprint import pprint
from prettytable import PrettyTable
from requests.auth import HTTPDigestAuth
import logging

def authenticate(openmaint_url,data):
    print ("***************************************************************")
    print ("*** Login and get authentication token ")
    print ("***************************************************************")
    auth_url=openmaint_url+"services/rest/v3/sessions?scope=service&returnId=true"     #the authentication url used to generate the sessionid
    headers = {'Content-type': 'application/json', 'Accept': '*/*'}
    r = requests.post(auth_url, data=json.dumps(data), headers=headers)         #sending a post request

    #print (r.json())                                                           #uncomment in case of error
    r1=r.json()
    sessionid=r1["data"]["_id"]
    print ("***************************************************************")
    print (" Authentication token is : " + sessionid)
    print ("***************************************************************")


    print ("***************************************************************")
    print ("*** Session info")
    print ("***************************************************************")

    session_url = auth_url+sessionid
    headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
    r = requests.get(session_url, data=json.dumps(data), headers=headers)
    #print (r.json())
    #pprint(r.json())
    return sessionid

def printClasses(openmaint_url,sessionid,data):
    print ("***************************************************************")
    print ("*** Classes ")
    print( "***************************************************************")

    class_url = openmaint_url+"services/rest/v3/classes/"
    headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
    r = requests.get(class_url, data=json.dumps(data), headers=headers)
    print ("There are " + str(r.json()["meta"]["total"]) + " results")
    #pprint(r.json())

    for value in r.json()["data"]:                                                  #loop through all the classes
     print ("\nTrying to get cards for : " + value["_id"] )
     id=value["_id"]

     print ("Getting id: " + id)

     print ("***************************************************************")
     print ("*** Class '"+id+"'")
     print( "***************************************************************")
     #Asset
     asset_url = class_url + id
     headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
     r = requests.get(asset_url, data=json.dumps(data), headers=headers)
     #pprint(r.json())                                                              #uncomment to print all classes

     print( "***************************************************************")
     print ("*** Class '"+id+"' attributes")
     print ("***************************************************************")

     getatt_url = asset_url + "/attributes"
     headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
     r = requests.get(getatt_url, data=json.dumps(data), headers=headers)
     print ("There are " + str(r.json()["meta"]["total"]) + " results for class " + id + " attributes ")
     #pprint(r.json())                                                              #uncomment to print all class attributes

     print ("***************************************************************")
     print ("*** Class '"+id+"' cards")
     print ("***************************************************************")
     cards_url = asset_url + "/cards"
     headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
     r = requests.get(cards_url, data=json.dumps(data), headers=headers)
     print( "There are " + str(r.json()["meta"]["total"]) + " results for class " + id + " cards ")
     #pprint(r.json())                                                                 #uncomment to print all cards

def main():
    username='admin'
    password='admin'
    data = {'username': username, 'password': password}
    openmaint_url = "http://192.168.100.22:8080/openmaint/"
    
    sessionid=authenticate(openmaint_url,data)
    
    printClasses(openmaint_url,sessionid,data)

if __name__ == "__main__":
    main()
