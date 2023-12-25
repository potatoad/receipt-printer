from escpos.printer import Serial, Dummy
from escpos.capabilities import Profile
import json

epson_profile = Profile()
epson_profile_name = "TM-H6000III"

with open("list.json") as json_list:
    list_data = json.load(json_list)

with open("EPSON.json") as json_profile:
    profile_data = json.load(json_profile)

    epson_profile.profile_data["codePages"] = profile_data[epson_profile_name][
        "codePages"
    ]
    epson_profile.profile_data["colors"] = profile_data[epson_profile_name]["colors"]
    epson_profile.features = profile_data[epson_profile_name]["features"]
    epson_profile.profile_data["fonts"] = profile_data[epson_profile_name]["fonts"]
    epson_profile.profile_data["media"] = profile_data[epson_profile_name]["media"]
    epson_profile.profile_data["name"] = profile_data[epson_profile_name]["name"]
    epson_profile.profile_data["vendor"] = profile_data[epson_profile_name]["vendor"]
    epson_profile.profile_data["notes"] = profile_data[epson_profile_name]["notes"]


s = Serial(
    devfile="COM7",
    baudrate=38400,
    bytesize=8,
    parity="N",
    stopbits=1,
    timeout=1.00,
    dsrdtr=True,
)

d = Dummy()