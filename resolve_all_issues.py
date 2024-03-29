#! /usr/local/bin/python

# Author: Sean Nicholson
# Script for resolving all Halo issues. This script is intended to clear out
# data related to Halo testing and issues created from a PoC
# Updated 2017/03/08 by Mark A. Aklian to add count, user input and progress


import json, io, requests
import cloudpassage
import yaml


def create_api_session(session):
    config_file_loc = "cloudpassage.yml"
    config_info = cloudpassage.ApiKeyManager(config_file=config_file_loc)
    session = cloudpassage.HaloSession(config_info.key_id, config_info.secret_key)
    return session


def resolve_issues(session):
    get_number_of_issues= cloudpassage.HttpHelper(session)
    number_of_issues = get_number_of_issues.get("/v2/issues")
    number_of_pages = int(number_of_issues['count'])
    number_of_pages = int(number_of_pages * .01)
    issues= cloudpassage.HttpHelper(session)
    list_of_issues_json = issues.get_paginated("/v2/issues", 'issues', number_of_pages)
    body = {"status": "resolved",}
    #print list_of_issues_json
    #loop list of issues and resolve them
    print "\n"
    print "##### There are %d issues to resolve #####" % len(list_of_issues_json)
    print "##### Hit <Enter> to proceed #####"
    proceed = raw_input("")
    print "\n"
    for issue in list_of_issues_json:
        print issue
        print "-"*20
        issueID = issue['id']
        issue_to_resolve = cloudpassage.HttpHelper(session)
        list_of_issues_json = issue_to_resolve.get("/v2/issues")
        reply = issue_to_resolve.put("/v2/issues/" + issueID, body)



def main():
    api_session = None
    api_session = create_api_session(api_session)
    resolve_issues(api_session)

if __name__ == "__main__":
        main()
