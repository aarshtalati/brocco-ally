#!/usr/bin/python

import sys
import requests
import constants
from datetime import datetime


def fun_loc(get_http_status_code = False):
    http_status, json  = http_get_request(constants.LOC_URL)
    if (http_status != 200):
        return http_status, json
    message = "The ISS current location at {time} is {lat}, {long}".format(
        time=datetime.fromtimestamp(json["timestamp"]).ctime()
        , lat=json["iss_position"]["latitude"]
        , long=json["iss_position"]["longitude"])
    return (http_status, message) if get_http_status_code else message
    


def fun_pass(pass_longitude, pass_latitude, get_http_status_code = False):
    http_status, json = http_get_request(constants.PASS_URL.format(
        lat=pass_latitude, lon=pass_longitude))
    if (http_status != 200):
        return http_status, json
    message = "The ISS will be overhead ({lat}, {long}) at {time} for {duration} seconds.".format(
        lat=pass_latitude
        , long=pass_longitude
        , time=datetime.fromtimestamp(json["response"][0]["risetime"]).ctime()
        , duration=json["response"][0]["duration"])
    return (http_status, message) if get_http_status_code else message
    

def fun_people(get_http_status_code = False):
    http_status, json  = http_get_request(constants.PEOPLE_URL)
    if (http_status != 200):
        return http_status, json
    number_of_astronauts = int(json["number"])
    if (number_of_astronauts > 0):
        craft_name = json["people"][0]["craft"]
        astronaut_names = ", ".join([x["name"] for x in json["people"]])
    if number_of_astronauts == 0:
        message = "Houston, we have a problem!"
    else:
        message = "There are {number_of_astronauts} people aboard the {craft_name}. They are {astronaut_names}".format(
            number_of_astronauts=number_of_astronauts, astronaut_names=astronaut_names, craft_name=craft_name
        )

    return (http_status, message) if get_http_status_code else message


def http_get_request(request_string):
    response = requests.get(request_string)
    if(response.status_code != 200):
        print("Error processing the API request. \n\n>>> Error Code: {0}\n".format(response.status_code))
        return response.status_code, response.content
    else:
        return response.status_code, response.json()


def main():
    number_sys_args = len(sys.argv)
    sys_args = sys.argv

    switcher = {
        "loc": fun_loc,
        "pass": fun_pass,
        "people": fun_people
    }

    if (number_sys_args < 2):
        print("Invalid comamnd. Please pass loc, pass or people. Terminating.")
        return 0

    func = switcher.get(sys_args[1].lower(),
                        lambda: "Invalid operation. Terminating")

    if (number_sys_args == 4 and sys_args[1].lower() == "pass"):
        pass_latitude, pass_longitude = sys_args[2:4]
        print(func(pass_longitude, pass_latitude))
    else:
        print(func())


if __name__ == "__main__":
    main()
