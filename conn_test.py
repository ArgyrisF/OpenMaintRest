#!/usr/bin/python3

import requests, json, pprint
import os,sys
from random import randint
from datetime import datetime
from pprint import pprint
from prettytable import PrettyTable
from requests.auth import HTTPDigestAuth
import logging


def authenticate(openmaint_url,data):
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~ Login and get session id ")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    auth_url=openmaint_url+"services/rest/v3/sessions?scope=service&returnId=true"     #the authentication url used to generate the sessionid
    #in order to get back the sessionid you need to add the returnID=true
    headers = {'Content-type': 'application/json', 'Accept': '*/*'}
    r = requests.post(auth_url, data=json.dumps(data), headers=headers)         #sending a post respuest

    #print (r.json())                                                           #uncomment in case of error
    resp=r.json()
    sessionid=resp["data"]["_id"]                                               # returns session id
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print (" Authentication token is : " + sessionid)
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~ Session info")
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    session_url = auth_url+sessionid
    headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
    r = requests.get(session_url, data=json.dumps(data), headers=headers)
    #print (r.json())
    #pprint(r.json())
    return sessionid

def printClasses(openmaint_url,sessionid,data):
    print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print ("~~~ Classes ")
    print( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    class_url = openmaint_url+"services/rest/v3/classes/"
    headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
    r = requests.get(class_url, data=json.dumps(data), headers=headers)
    print ("There are " + str(r.json()["meta"]["total"]) + " results")
    #pprint(r.json())

    for value in r.json()["data"]:                                                  #loop through all the classes
     print ("\nTrying to get cards for : " + value["_id"] )
     id=value["_id"]

     print ("Getting id: " + id)

     print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
     print ("~~~ Class '"+id+"'")
     print( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
     #Asset
     asset_url = class_url + id
     headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
     r = requests.get(asset_url, data=json.dumps(data), headers=headers)
     #pprint(r.json())                                                              #uncomment to print all classes

     print( "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
     print ("~~~ Class '"+id+"' attributes")
     print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

     getatt_url = asset_url + "/attributes"
     headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
     r = requests.get(getatt_url, data=json.dumps(data), headers=headers)
     print ("There are " + str(r.json()["meta"]["total"]) + " results for class " + id + " attributes ")
     #pprint(r.json())                                                              #uncomment to print all class attributes

     print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
     print ("~~~ Class '"+id+"' cards")
     print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
     cards_url = asset_url + "/cards"
     headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
     r = requests.get(cards_url, data=json.dumps(data), headers=headers)
     print( "There are " + str(r.json()["meta"]["total"]) + " results for class " + id + " cards ")
     #pprint(r.json())                                                                 #uncomment to print all cards

def saveValue(openmaint_url,sessionid,data,value,mcode,meterno,itemno):                #pass the value, the name and number of the meter you will be using
    cards_url= openmaint_url + 'services/rest/v3/classes/Meter/cards'
    id_new = randint(100000, 999999)                                #generate random id for the meters value                                                  #the name of the meter you will be using
    today = datetime.now()                                             #get date
    Date = today.strftime("%Y-") + str(today.month).zfill(2) + \
    today.strftime("-%dT%H:%M:%SZ")                                     #format it
    url_to_send = cards_url + '/' + str(id_new)
    Data_send_new = {"Date": Date, "Item": itemno, "Meter": meterno,
                 "Value": value, "Meter_code": mcode, 
                 "_type": 'MeterReading', "_user": 'admin'}
    headers = {'Content-type': 'application/json',
           'Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    r = requests.post(cards_url, data=json.dumps(Data_send_new),
                  headers=headers)  # A new value gets sent
        
def printMeters(openmaint_url,sessionid,data,classid):
    #documentation of this API is not the best, alot of times you will have to get all the data of the class
    #you want to use in order to make sense of how it is structured. Use this function to grab any class's information
    class_url = openmaint_url + "services/rest/v3/classes/"
                                                           #you can print all items of any class, just change the id
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ Class '" + classid + "'")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    asset_url = class_url + classid
    headers = {'Content-type': 'application/json',
               'Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    r = requests.get(asset_url, data=json.dumps(data), headers=headers)
    pprint(r.json())

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ Class '" + classid + "' attributes")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    getatt_url = asset_url + "/attributes"
    headers = {'Content-type': 'application/json',
               'Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    r = requests.get(getatt_url, data=json.dumps(data), headers=headers)
    print("There are " + str(r.json()
           ["meta"]["total"]) + " results for class " + classid + " attributes ")
    pprint(r.json())

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ Class '" + classid + "' cards")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    cards_url = asset_url + "/cards"
    headers = {'Content-type': 'application/json',
               'Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    r = requests.get(cards_url, data=json.dumps(data), headers=headers)
    print("There are " + str(r.json()
                ["meta"]["total"]) + " results for class " + classid + " cards ")
    pprint(r.json())
        
def checkMaint(openmaint_url,sessionid,data):
    process_url = openmaint_url + "services/rest/v3/processes/MaintRequest/instances"

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ processes ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    headers = {'Content-type': 'application/json',
               'Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    r = requests.get(process_url, data=json.dumps(data), headers=headers)
    print("There are " + str(r.json()["meta"]["total"]) + " results")
    pprint(r.json())
       
def findActivity(openmaint_url,sessionid,data,idA):
    process_url = openmaint_url + "services/rest/v3/processes/MaintRequest/instances/"+str(idA)+'/activities'
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ activities ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    headers = {'Content-type': 'application/json',
               'Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    r = requests.get(process_url, data=json.dumps(data), headers=headers)
    pprint(r.json())
    print(r.json()["data"][0]["_id"])
    return(r.json()["data"][0]["_id"])

def assignTask(openmaint_url,sessionid,data,idA,activityId):
    process_url = openmaint_url + "services/rest/v3/processes/MaintRequest/instances/"+str(idA)
    today = datetime.now()                                             #get date
    Date = today.strftime("%Y-") + str(today.month).zfill(2) + \
    today.strftime("-%dT%H:%M:%SZ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ assign ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    headers = {'Content-type': 'application/json',
               'Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    data_to_send = {'_activity' : activityId, '_advance' : True, 'Action' : 261333,
                    'Category' : 283236, 'Subcategory': 283245, 'Team': 278572}
    r = requests.put(process_url, data=json.dumps(data_to_send), headers=headers)
    pprint(r.json())

def deleteTask(openmaint_url,sessionid,data,idA):
    process_url = openmaint_url + "services/rest/v3/processes/MaintRequest/instances/"+idA
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("~~~ delete ")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    headers = {'Content-type': 'application/json',
               'Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    r = requests.delete(process_url, data=json.dumps(data), headers=headers)
    pprint(r.json())

def createTask(openmaint_url,sessionid,data):
    today = datetime.now()
    Date = today.strftime("%Y-") + str(today.month).zfill(2) + \
        today.strftime("-%dT%H:%M:%SZ")
    url_send = openmaint_url + 'services/rest/v3/processes/MaintRequest/instances/'
    Data_to_send = {'_advance' : True,'OpeningDate': Date,'Priority': 118,
                    'Requester': 277826,'ShortDescr': 'Test999','Site': 277632,'Type': 261331,
           '_CI_code': '101ΑΣ1',
           '_CI_description': '101ΑΣ1 - ΑΣΑΝΣΕΡ 1',
           '_FlowStatus_code': 'open.running',
           '_FlowStatus_description': 'Running',
           '_FlowStatus_description_translation': 'Running',
           '_Priority_code': '2',
           '_Priority_description': 'High',
           '_Priority_description_translation': 'High',
           '_Requester_code': '101Υ1',
           '_Requester_description': 'Ιωαννου Κωστας',
           '_Site_code': '101',
           '_Site_description': '101 - Μαρμελαδα',
           '_Type_code': 'Breakdown',
           '_Type_description': 'Breakdown',
           '_Type_description_translation': 'Breakdown','_beginDate':Date,'_status_description': 'Running',
           '_type': 'MaintRequest',
           '_user': 'admin','status': 1}
    headers = {'Content-type': 'application/json','Accept': '*/*', 'CMDBuild-Authorization': sessionid}
    r = requests.post(url_send, data=json.dumps(Data_to_send),headers=headers)
    #pprint(r.json())
    print(r.json()["data"]["_id"])
    return(r.json()["data"]["_id"])

def main():
    username='admin'                                            #default values
    password='admin'                                            #change with yours
    data = {'username': username, 'password': password}
    openmaint_url = "http://127.0.0.1:8080/openmaint/"
    ReadingfromSensor =  29                                     #read from sensor or any input you want
    
    sessionid=authenticate(openmaint_url,data)                  #authenticate the user, returns session id
    input("Press Enter to continue with task creation...")
    
    #printClasses(openmaint_url,sessionid,data)                  #prints all the classes and their attributes
    
    #saveValue(openmaint_url,sessionid,data,ReadingfromSensor,'M1',299387,277953)     #saves a value (eg reading from a sensor) to a meter

    #printMeters(openmaint_url,sessionid,data,'Meter')           #prints all the existing meters attributes, returns all the info you need
                                                                #to pass to the saveValue function
    #checkMaint(openmaint_url,sessionid,data)                    #prints all existing maintenance request instances

    idA=createTask(openmaint_url,sessionid,data)                    #creates a maintenance task and returns its id
    input("Press Enter to continue...")
    
    activityId = findActivity(openmaint_url,sessionid,data,idA)     #find the activityID
    input("Press Enter to continue with task assignment...")
    
    assignTask(openmaint_url,sessionid,data,idA,activityId)         #assign task to team & worker using the activityID

    #deleteTask(openmaint_url,sessionid,data,idA)                   #delete task (must pass the task id)

if __name__ == "__main__":
    main()
