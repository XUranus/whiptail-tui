#!/usr/bin/env python3
#
#  whiptail_box.py

# stdlib
from __future__ import annotations
from typing import Optional, Sequence, Type, Callable, Any

# third part
from .whiptail_base import WhiptailBase

class WhiptailMessageBox(WhiptailBase):
    """
    Wrap the message box base of whiptail msgbox

    Message box is used to display text message, it has only an ``ok`` button.

    :param message: the text message to display
    :param on_ok: event to trigger when ok button is pushed
    """
    def __init__(self, message : str, height : Optional[int], width : Optional[int], on_ok : Callable[[], Any]):
        super().__init__(box = 'msgbox', text = message, height = height, width = width)
        self.on_ok = on_ok

    
    



class WhiptailYesNo(WhiptailBase):
    """
    wrap the yesno box base of whiptail yesno
    """



class WhiptailInfoBox(WhiptailBase):
    """
    wrap the info box base of whiptail infobox
    """



class WhiptailInputBox(WhiptailBase):
    """
    wrap the password input box base of whiptail inputbox and passwordbox
    """



class WhiptailTextBox(WhiptailBase):
    """
    wrap the text box base of whiptail textbox
    """


class WhiptailMenuBox(WhiptailBase):
    """
    wrap the menu box base of whiptail menu
    """



class WhiptailCheckListBox(WhiptailBase):
    """
    wrap the check list box base of whiptail listbox
    """



class WhiptailRadioListBox(WhiptailBase):
    """
    wrap the radio list box base of whiptail radiolist
    """



class WhiptailGaugeBox(WhiptailBase):
    """
    wrap the progress bar box base of whiptail gauge
    """