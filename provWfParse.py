#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:21:09 2020

@author: ruyuexin
"""
#Parse workflow .t2flow file
import xml.dom.minidom

PROCESSORS_TAG = "processors"
ARTIFCAT_TAG = "artifact"
REST_TAG = "rest-activity"
NAME_TAG = "name"
EP_TAG = "urlSignature"
HTTP_TAG = "httpMethod"
ACTIVITIES_TAG = "activities"

DOMTree = xml.dom.minidom.parse("./Data/new_workflow.t2flow")
doc = DOMTree.documentElement
nodes = doc.getElementsByTagName(PROCESSORS_TAG)[0].childNodes
print(nodes)
servicelist = []
for i in range(len(nodes)):
    print(i)
    currNode = nodes[i]
    activity = currNode.getElementsByTagName(ACTIVITIES_TAG)[0].childNodes[0]
    type_ = activity.getElementsByTagName(ARTIFCAT_TAG)[0].childNodes[0].nodeValue
    if type_ == REST_TAG:
        name = currNode.getElementsByTagName(NAME_TAG)[0].childNodes[0].nodeValue
        endpoint = currNode.getElementsByTagName(EP_TAG)[0].childNodes[0].nodeValue
        http = currNode.getElementsByTagName(HTTP_TAG)[0].childNodes[0].nodeValue
        print(name, endpoint, http)
        servicelist.append((name, endpoint, http))
print(servicelist)
    

#Parsr provenance .ttl file
from rdflib import Graph
g = Graph()
g.parse("./Data/workflowrun.prov.ttl", format="ttl")
print(g)

service_name = "GETIMAGE"

queryExecutionTimes = "SELECT ?startTime ?endTime WHERE {" \
                "?y  rdfs:label  \"Processor execution " + service_name + "\"@en . " \
                "?y  prov:startedAtTime  ?startTime . " \
                "?y  prov:endedAtTime  ?endTime . " \
"}"
svExecution = g.query(queryExecutionTimes)
print(list(svExecution))

queryWorkflowExecution = "SELECT ?startTime ?endTime WHERE { " \
                    "?y  rdf:type wfprov:WorkflowRun . " \
                    "?y  prov:startedAtTime  ?startTime . " \
                    "?y  prov:endedAtTime  ?endTime . "  \
"}"
wfExecution = g.query(queryWorkflowExecution)
print(list(wfExecution))
