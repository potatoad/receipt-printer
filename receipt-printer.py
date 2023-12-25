from escpos.printer import Serial, Dummy
from escpos.capabilities import Profile
import json
import PySimpleGUI as sg
from PIL import Image, ImageTk

epson_profile = Profile()
epson_profile_name = "TM-H6000III"

tab = "   "
# list_data = []

# with open("list.json") as json_list:
#     list_data = json.load(json_list)

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


def print_receipt(logo, list):
    list = eval(list)
    
    subtotal = 0
    
    d.set(align="center")
    d.image(logo, center=True)

    d.ln()
    d.set(align="center", bold=True, double_height=True, double_width=True)
    d.text("A QUEER.INK ZINE\n")

    d.ln()

    print(list)

    for item in list:
        print(item)
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

    d.textln(tab + str(len(list)).ljust(4) + "BALANCE DUE".ljust(27) + total)

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
    d.barcode(
        "{Bhttps://queer.ink/",
        "CODE128",
        width=2,
        height=128,
        pos="off",
        function_type="B",
    )
    d.ln()
    d.textln("Thank you for reading.")

    d.cut()

    s._raw(d.output)


def main():
    sg.theme("LightBrown8")

    # Define layout
    layout = [
        [
            sg.Text("Select Image File"),
            sg.InputText(key="-IMAGE_FILE-", enable_events=True),
            sg.FileBrowse(),
        ],
        [sg.Image(key="-IMAGE_VIEW-")],
        [sg.Button("Remove Image")],
        [
            sg.Text("Select List File"),
            sg.InputText(key="-LIST_FILE-", enable_events=True),
            sg.FileBrowse(),
        ],
        [sg.Multiline(key="-LIST_VIEW-", size=(56, 15))],
        [sg.Button("Remove List")],
        [sg.Button("Print")],
    ]

    # Create window
    window = sg.Window("Image and Data Entry", layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "Remove Image":
            window["-IMAGE_FILE-"].update("")
            window["-IMAGE_VIEW-"].update(data=None)

        if event == "Remove List":
            window["-LIST_FILE-"].update("")
            window["-LIST_VIEW-"].update("")

        # Update image preview when a file is selected
        if event == "-IMAGE_FILE-":
            file_path = values["-IMAGE_FILE-"]
            try:
                image = Image.open(file_path)
                image.thumbnail((512, 512))
                photo = ImageTk.PhotoImage(image)
                window["-IMAGE_VIEW-"].update(data=photo)
            except Exception as e:
                print(f"Error loading image: {e}")

        if event == "-LIST_FILE-":
            # file_path = values["-LIST_FILE-"]
            # file = open(file_path, "r")
            # file_content = json.load(file.read())

            with open(values["-LIST_FILE-"]) as json_list:
                list_data = json.load(json_list)

            try:
                window["-LIST_VIEW-"].update(value=list_data)
            except Exception as e:
                print(f"Error loading list: {e}")

        # Print values
        if event == "Print":
            print_receipt(values["-IMAGE_FILE-"], values["-LIST_VIEW-"])

    window.close()


if __name__ == "__main__":
    main()
