from escpos.printer import Serial, Dummy
from escpos.capabilities import Profile
import json

epson_profile = Profile()
epson_profile_name = "TM-H6000III"

tab = "   "
list_data = []
subtotal = 0

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

d.set(align="center")
d.image("Artboard 7.png", center=True)

d.ln()
d.set(align="center", bold=True, double_height=True, double_width=True)
d.text("A QUEER.INK ZINE\n")

d.ln()

for item in list_data:
    name = item["name"].upper()
    name = name.ljust(30)
    name = name[:30]

    price = item["price"]
    subtotal += float(price)
    price = "£" + price
    price = price.rjust(7)

    d.set(
        align="left",
        bold=False,
        double_height=False,
        double_width=False,
        normal_textsize=True,
    )
    d.textln(tab + name + " " + price)

d.ln()

d.set(bold=True)

total = str(subtotal)
total = "£" + total
total = total.rjust(7)

d.textln(tab + str(len(list_data)).ljust(4) + "BALANCE DUE".ljust(27) + total)

d.set()
d.textln(tab + tab + " " + "Visa Debit".ljust(27) + total)
d.set(bold=True)
d.text("       contactless ")
d.set(font="b", bold=True)
d.text(")")
d.set(font="a", bold=True)
d.text(")\n")
d.set()
d.ln()

d.textln("Cardholder Device Verified")
d.ln()
d.textln(tab + tab + " " + "Change".ljust(27) + "£0.00".rjust(7))
d.ln()
d.set(font="b", bold=False)
d.textln("********************************************************")
d.set(font="a", align="center")
d.text("HOW DID WE DO?\nLET US KNOW AT ")
d.set(bold=True, align="center")
d.text("HTTPS://QUEER.INK/\n")
d.set(bold=False, align="center")
d.textln("FOR A CHANCE TO WIN A PANIC ATTACK!")
d.set(font="b")
d.textln("********************************************************")

d.set(align="center", font="a")
d.textln("PLEASE KEEP FOR YOUR RECORDS\nYOU ARE VALUED AND YOU ARE LOVED")
d.ln()
d.barcode("{Bhttps://queer.ink/", "CODE128", width=2, height=128, pos="off", function_type="B")
d.ln()
d.textln("Thank you for reading.")

d.cut()

s._raw(d.output)
