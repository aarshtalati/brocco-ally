#!/usr/bin/python

import sys
import requests
import constants
from datetime import datetime


def fun_loc():
    response = http_get_request(constants.LOC_URL)
    json = response.json()
    return "The ISS current location at {time} is {lat}, {long}".format(
        time=datetime.fromtimestamp(json["timestamp"]).ctime(), lat=json["iss_position"]["latitude"], long=json["iss_position"]["longitude"]
    )


def fun_pass():
    # http://open-notify.org/Open-Notify-API/ISS-Pass-Times/
    # http://api.open-notify.org/iss-pass.json?lat=48.7107&lon=-75.8450
    # http://api.open-notify.org/iss-pass.json?lat=LAT&lon=LON
    print("pass")
    print(sys.argv)
    pass


def fun_people():
    response = http_get_request(constants.PEOPLE_URL)
    json = response.json()
    number_of_astronauts = int(json["number"])
    if (number_of_astronauts > 0):
        craft_name = json["people"][0]["craft"]
        astronaut_names = ", ".join([x["name"] for x in json["people"]])
    if number_of_astronauts == 0:
        message = "No humans on ISS, just aliens!"
    else:
        message = "There are {number_of_astronauts} people aboard the {craft_name}. They are {astronaut_names}".format(
            number_of_astronauts=number_of_astronauts, astronaut_names=astronaut_names, craft_name=craft_name
        )
    return message


def http_get_request(request_string):
    response = requests.get(request_string)
    if(response.status_code != 200):
        print("Error processing the API request. Error Code: {0}".format(
            response.status_code))
    return response


def main():
    number_sys_args = len(sys.argv)
    sys_args = sys.argv

    if (number_sys_args < 2):
        print("Invalid comamnd. Please pass loc, pass or people. Terminating.")

    switcher = {
        "loc": fun_loc,
        "pass": fun_pass,
        "people": fun_people
    }

    func = switcher.get(sys_args[1].lower(),
                        lambda: "Invalid operation. Terminating")
    print(func())


if __name__ == "__main__":
    main()
