import re
import time
import threading

from whiptailtui import WhiptailMessageBox, WhiptailMenuBox, \
WhiptailMenuItem, WhiptailYesNo, WhiptailRadioListBox, WhiptailInfoBox, \
WhiptailTextBox, WhiptailInputBox, WhiptailCheckListBox, WhiptailSelectItem, \
WhiptailFormItem, WhiptailFormBox, WhiptailGaugeBox

def validate_ip(ip : str):
    # Define a regular expression pattern for IP address validation
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'

    # Use the re.match() function to check if the input matches the pattern
    if re.match(pattern, ip):
        # Split the IP address into its components
        octets = ip.split('.')
        # Check if each octet is a valid number (0-255)
        if all(0 <= int(octet) <= 255 for octet in octets):
            return True
    return False

WhiptailMessageBox(
    message = "message box content",
    height = 10,
    width = 40,
    on_ok = lambda : print('ok pushed')) \
    .show()

WhiptailYesNo(
    message = "choose yes or no",
    height = 10,
    width = 40,
    on_yes = lambda : print('you choosed yes'),
    on_no = lambda : print('you choosed no')) \
    .set_yes_button("是") \
    .set_no_button("否") \
    .set_default_no() \
    .show()

WhiptailInfoBox(
    message = "info box content",
    height = 10,
    width = 40) \
    .show()

WhiptailTextBox(
    textfile = __file__,
    height = 10,
    width = 40,
    on_ok = lambda : print('ok pushed'),
    on_failed = lambda : print('open file failed')) \
    .show()

WhiptailMenuBox(
    message = "menu box message",
    height = 20,
    width = 40,
    prefix = '-',
    description = True,
    items = (
        WhiptailMenuItem(
            key = "item1",
            description = "description1",
            data = {"text" : "hello world"},
            on_selected = lambda v : print(f'select {v}')
        ),
        WhiptailMenuItem(
            key = "item2",
            description = "description2",
            data = {"text" : "hello world"},
            on_selected = lambda v : print(f'select {v}')
        ),
        WhiptailMenuItem(
            key = "item3",
            description = "description3",
            data = {"text" : "hello world"},
            on_selected = lambda v : print(f'select {v}')
        )
    ),
    on_cancel = lambda : print('Whiptail menu box canceled')
).show()

WhiptailCheckListBox(
    message = "list box",
    height = 20,
    width = 40,
    prefix = '-',
    description = True,
    items = (
        WhiptailSelectItem(
            key = "item1",
            description = "description1"
        ),
        WhiptailSelectItem(
            key = "item2",
            description = "description2"
        ),
        WhiptailSelectItem(
            key = "item3",
            description = "description3"
        )
    ),
    on_cancel = lambda : print('Whiptail checklist box canceled'),
    on_submit = lambda v : print(f'checklist selected: {v}')
).show()


WhiptailRadioListBox(
    message = "radio box",
    height = 20,
    width = 40,
    prefix = '-',
    description = True,
    items = (
        WhiptailSelectItem(
            key = "item1",
            description = "description1"
        ),
        WhiptailSelectItem(
            key = "item2",
            description = "description2"
        ),
        WhiptailSelectItem(
            key = "item3",
            description = "description3"
        )
    ),
    on_cancel = lambda : print('Whiptail radiolist box canceled'),
    on_submit = lambda v : print(f'radiolist selected: {v}')
).show()


WhiptailInputBox(
    message = "input an ip address",
    height = 10,
    width = 40,
    placeholder = '192.168',
    validator = validate_ip,
    error_message = "invalid ip address!",
    on_submit = lambda text : print(f'input: {text}'),
    on_cancel = lambda : print('input canceled')) \
    .show()


WhiptailFormBox(
    message = "input your login info",
    height = 20,
    width = 40,
    submit_button = ' LOGIN ',
    on_submit = lambda form_data : print(f'form data: {form_data}'),
    on_cancel = lambda : print('form canceled'),
    items = (
        WhiptailFormItem(
            key = "username",
            name = "user",
            value = "XUranus",
            validator = lambda text : len(text) < 10,
            error_message = "username too long"
        ),
        WhiptailFormItem(
            key = "password",
            name = "passwd",
            password = True
        )
    )
).show()

progress_bar = WhiptailGaugeBox(
    message = "progress bar",
    height = 10,
    width = 40).listen()

print(progress_bar)

for percent in range(1, 101):
    progress_bar.update_percent(percent)
    time.sleep(1)
progress_bar.terminate()