from escpos.printer import Serial, Dummy

import PySimpleGUI as sg
from PIL import Image, ImageTk


def print_values(data):
    print("Printing values:")
    for entry in data:
        print(f"Text: {entry['text']}, Price: {entry['price']}")


def main():
    sg.theme("Default1")

    # Define layout
    layout = [
        [sg.Text(text="This is a very basic PySimpleGUI layout")],
        [sg.InputText(), sg.Button(button_text="Browse...")],
        [sg.Image()],
        [sg.Text(text="Item"), sg.InputText(), sg.Text(text="Price"), sg.InputText()],
        [
            sg.Button(button_text="Print", key="-ExampleKey-"),
            sg.Button(button_text="Exit"),
            sg.Button(button_text="Add item"),
        ],
    ]

    # Create window
    window = sg.Window("Image and Data Entry", layout, resizable=True, finalize=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        # Update image preview when a file is selected
        if event == "-FILE-":
            file_path = values["-FILE-"]
            try:
                image = Image.open(file_path)
                image.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(image)
                window["-IMAGE-"].update(data=photo)
            except Exception as e:
                print(f"Error loading image: {e}")

        # Add and remove additional sets
        if event == "Add item":
            layout_extension = [
                [
                    sg.Text("Text"),
                    sg.InputText(key="-TEXT2-", size=(20, 1)),
                    sg.Text("Price"),
                    sg.InputText(key="-PRICE2-", size=(10, 1)),
                ],
            ]
            window.extend_layout(window, layout_extension)

        # Print values
        if event == "Print":
            data = [
                {"text": values["-TEXT-"], "price": values["-PRICE-"]},
                {
                    "text": values.get("-TEXT2-", ""),
                    "price": values.get("-PRICE2-", ""),
                },
                {
                    "text": values.get("-TEXT3-", ""),
                    "price": values.get("-PRICE3-", ""),
                },
            ]
            print_values(data)

    window.close()


if __name__ == "__main__":
    main()


# p = Serial(
#     devfile="COM5",
#     baudrate=38400,
#     bytesize=8,
#     parity="N",
#     stopbits=1,
#     timeout=1.00,
#     dsrdtr=True,
# )

d = Dummy(profile="TM-H6000III")

d.set(align="center")
d.image("Artboard 7.png", center=True)
d.ln()
d.set(align="center", bold=True, double_height=True, double_width=True)
d.text("A QUEER.INK ZINE\n")

d.set(align="center", font="b")
d.set()
d.ln()

d.set(align="left")
d.textln("   TAGLIATELLE PASTA 500G          £2.25")
d.textln("   STONEBAKED PIZZA                £2.50")
d.textln("   BRIGHT LIGHTS                   £1.80")
d.textln("   LOTS OF SMELLS                  £3.50")
d.textln("   LOTS OF PEOPLE                 £25.00")
d.textln("   CHECKOUTS BEEPING               £6.00")
d.textln("   IN-STORE MUSIC PLAYING         £12.80")
d.textln("   PEOPLE LOOKING AT ME            £9.99")
d.textln("   ARE THEY GOING TO HARASS ME?   £39.99")
d.textln("   I WANT TO GO HOME               £2.10")
d.textln("   I WANT TO BE SICK               £5.50")

d.ln()

d.set(bold=True)
d.textln("   12 BALANCE DUE                £121.43")

d.set()
d.textln("       Visa Debit                £121.43")
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
d.textln("       Change                      £0.00")
d.ln()
d.set(font="b")
d.textln("********************************************************")
d.set(font="a", align="center")
d.text("HOW DID WE DO?\nLET US KNOW AT ")
d.set(bold=True, align="center")
d.text("HTTPS://QUEER.INK/\n")
d.set(bold=False, align="center")
d.textln("FOR A CHANCE TO WIN A PANIC ATTACK!")
d.set(font="b")
d.textln("********************************************************")

d.set(align="center")
d.textln("PLEASE KEEP FOR YOUR RECORDS\nPUBLISHED TERMS AND CONDITIONS APPLY")
d.ln()
d.barcode("{Bhttps://queer.ink/", "CODE128", width=2, pos="off", function_type="B")
d.ln()
d.textln("Thank you for reading.")

d.cut()

# p._raw(d.output)
