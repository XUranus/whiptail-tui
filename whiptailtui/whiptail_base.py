#!/usr/bin/env python3
#
#  whiptail_base.py

from __future__ import annotations
from typing import Optional, Sequence, Type
from collections import namedtuple
import subprocess
import shutil

whiptail_box_name_list = [
    'msgbox',
    'yesno',
    'infobox',
    'inputbox',
    'passwordbox',
    'textbox',
    'menu',
    'checklist',
    'radiolist',
    'gauge'
]

POSITIVE_RETURN_CODE : int = 0
NEGATIVE_RETURN_CODE : int = 1
ESC_RETURN_CODE      : int = 255

class Response(namedtuple("__BaseResponse", "returncode value")):
    """
    Namedtuple to store the returncode and value returned by a whiptail dialog.

    :param returncode: The returncode.
    :param value: The value returned from the dialog.

	Return values are as follows:
        * ``0``: The ``Yes`` or ``OK`` button was pressed.
        * ``1``: The ``No`` or ``Cancel`` button was pressed.
        * ``255``: The user pressed the ``ESC`` key, or an error occurred.
    """
    returncode: int
    value: str

    __slots__ = ()

    def __new__(cls, returncode: int, value: AnyStr):
        """
        Create a new instance of :class:`~.Response`.

        :param returncode: The returncode.
        :param value: The value returned from the dialog.
        """
        if isinstance(value, bytes):
            val = value.decode("UTF-8")
        else:
            val = value
        return super().__new__(cls, returncode, val)



class WhiptailBase:
    """
    Manage common attribute of whiptail all type of whiptail box box.

    The attributes is corresponded to command options:
        clear_on_exit    <bool>              --clear                     clear screen on exit
        default_no       <bool>              --defaultno                 default no button
        default_item     <Optional[str]>     --default-item <text>       set default string
        full_buttons     <bool               --fullbuttons               use full buttons
        no_cancel        <bool>              --nocancel                  no cancel button
        yes_button       <Optional[str]>     --yes-button <text>         set text of yes button
        no_button        <Optional[str]>     --no-button <text>          set text of no button
        ok_button        <Optional[str]>     --ok-button <text>          set text of ok button
        cancel_button    <Optional[str]>     --cancel-button <text>      set text of cancel button
        no_item          <bool>              --noitem                    don't display items
        no_tags          <bool>              --notags                     don't display tags
        separate_output  <bool>              --separate-output           output one line at a time
        title            <Optional[str]>     --title <text>              display title
        backtitle        <Optional[str]>     --backtitle <text>          display backtitle
        scrolltext       <bool>              --scrolltext                force vertical scrollbars
        topleft          <bool>              --topleft                   put window in top-left corner

    Box command options:
        --msgbox <text> <height> <width>
        --yesno  <text> <height> <width>
        --infobox <text> <height> <width>
        --inputbox <text> <height> <width> [init] 
        --passwordbox <text> <height> <width> [init] 
        --textbox <file> <height> <width>
        --menu <text> <height> <width> <listheight> [tag item] ...
        --checklist <text> <height> <width> <listheight> [tag item status]...
        --radiolist <text> <height> <width> <listheight> [tag item status]...
        --gauge <text> <height> <width> <percent>   
    """
    def __init__(self, box : str, text : str, height : Optional[int], width : Optional[int]):
        # init all whiptail attributes to False or None
        self.clear_on_exit  : bool          = False
        self.default_no     : bool          = False
        self.default_item   : Optional[str] = None
        self.full_buttons   : bool          = False
        self.no_cancel      : bool          = False
        self.yes_button     : Optional[str] = None
        self.no_button      : Optional[str] = None
        self.ok_button      : Optional[str] = None
        self.cancel_button  : Optional[str] = None
        self.no_item        : bool          = False
        self.no_tags        : bool          = False
        self.separate_output: bool          = False
        self.title          : Optional[str] = None
        self.backtitle      : Optional[str] = None
        self.scrolltext     : bool          = False
        self.topleft        : bool          = False
        # some terminal need to configure TERM enviroment variable
        self.term_env       : Optional[str] = None
        # whiptail box attributes
        self.box         : str           = box
        self.text        : str           = text
        self.height      : int           = height
        self.width       : int           = width
        self.box_extra_args : Sequence[str] = ()
        self.process = None
        if box not in whiptail_box_name_list:
            raise Exception("invalid whiptail box name: {}".format(box))
        if self.height is None:
            self.height = self.get_default_height()
        if self.width is None:
            self.width = self.get_default_width()

    def get_default_height(self) -> int:
        """
        calculate default height of dialog box using terminal size if height is not specified
        """
        _, height = shutil.get_terminal_size()
        height -= 2
        height -= (height % 5)
        return height

    def get_default_width(self) -> int:
        """
        calculate default width of dialog box using terminal size if width is not specified
        """
        width, _ = shutil.get_terminal_size()
        width -= 2
        hewidthight -= (width % 5)
        return width

    def get_default_list_height(self) -> int:
        """
        Calculate default list height of dialog box.
        Must be used after box height is initialized.
        """
        return self.height - 10

    def build_whiptail_args(self) -> list[str]:
        """
        Build whiptail command args from whiptail attriutes.
        Any attribute of type Optional[str] and is not None and
        Any attribute of type bool if True should be put in list
        """
        whiptail_args = []
        if self.clear_on_exit:
            whiptail_args.append("--clear")
        if self.default_no:
            whiptail_args.append("--defaultno")
        if self.full_buttons:
            whiptail_args.append("--fullbuttons")
        if self.no_cancel:
            whiptail_args.append("--nocancel")
        if self.no_item:
            whiptail_args.append("--noitem")
        if self.no_tags:
            whiptail_args.append("--notags")
        if self.separate_output:
            whiptail_args.append("--separate-output")
        if self.scrolltext:
            whiptail_args.append("--scrolltext")
        if self.topleft:
            whiptail_args.append("--topleft")
        if self.default_item is not None:
            whiptail_args += ["--default-item", self.default_item]
        if self.yes_button is not None:
            whiptail_args += ["--yes-button", self.yes_button]
        if self.no_button is not None:
            whiptail_args += ["--no-button", self.no_button]
        if self.ok_button is not None:
            whiptail_args += ["--ok-button", self.ok_button]
        if self.cancel_button is not None:
            whiptail_args += ["--cancel-button", self.cancel_button]
        if self.title is not None:
            whiptail_args += ["--title", self.title]
        if self.backtitle is not None:
            whiptail_args += ["--backtitle", self.backtitle]
        return whiptail_args
    
    def run(self) -> Response:
        """
        box command all need text, height and width
        whiptail command can be split as: [TERM=ansi] whiptail [whiptail args...] --<box> <text> <height> <width> [box extra args...]
        whiptail args should be extract from whiptail attributes while box extra args should be extrat from box attributes
        """
        whiptail_args = self.build_whiptail_args()
        cmd = []
        if (self.term_env is not None):
            cmd = ["TERM={}".format(self.term_env)]
        cmd += ["whiptail"]
        cmd += [*list(whiptail_args)]
        cmd += [
            "--{}".format(self.box),
            "--",
            str(self.text),
            str(self.height),
            str(self.width),
            *list(self.box_extra_args)
        ]
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        _, err = process.communicate()
        # err is the selected key str
        return Response(process.returncode, err)

    def show(self) -> Response:
        """
        run the command and trigger the corresponding event according to the response return code
        """
        response = self.run()
        if response.returncode == POSITIVE_RETURN_CODE:
            self.on_positive_event_triggered(response.value)
        elif response.returncode == NEGATIVE_RETURN_CODE:
            self.on_negative_event_triggered()
        elif response.returncode == ESC_RETURN_CODE:
            self.on_esc_event_triggered()
        else:
            raise Exception(f"unexpected Response return code {response.returncode}")
        return response

    def on_positive_event_triggered(self, value : str) -> None:
        """
        subclass need to override this method if needed
        """
        raise Exception("on_positive_event_triggered not implemented!")
        pass

    def on_negative_event_triggered(self, value : str) -> None:
        """
        subclass need to override this method if needed
        """
        raise Exception("on_negative_event_triggered not implemented!")
        pass

    def on_esc_event_triggered(self, value : str) -> None:
        """
        subclass need to override this method if needed
        """
        raise Exception("on_esc_event_triggered not implemented!")
        pass
    
    def set_clear_on_exit(self) -> Type[self]:
        self.clear_on_exit = True
        return self

    def set_default_no(self) -> Type[self]:
        self.default_no = True
        return self

    def set_default_item(self, default_item : str) -> Type[self]:
        self.default_item = default_item
        return self

    def set_full_buttons(self) -> Type[self]:
        self.full_buttons = True
        return self

    def set_no_cancel(self) -> Type[self]:
        self.no_cancel = True
        return self
        
    def set_yes_button(self, yes_button : str) -> Type[self]:
        self.yes_button = yes_button
        return self

    def set_no_button(self, no_button : str) -> Type[self]:
        self.no_button = no_button
        return self

    def set_ok_button(self, ok_button : str) -> Type[self]:
        self.ok_button = ok_button
        return self

    def set_cancel_button(self, cancel_button : str) -> Type[self]:
        self.cancel_button = cancel_button
        return self

    def set_no_item(self) -> Type[self]:
        self.no_item = True
        return self

    def set_no_tags(self) -> Type[self]:
        self.no_tags = True
        return self

    def set_separate_output(self) -> Type[self]:
        self.separate_output = True
        return self

    def set_title(self, title : str) -> Type[self]:
        self.title = title
        return self

    def set_backtitle(self, backtitle : str) -> Type[self]:
        self.backtitle = backtitle
        return self

    def set_scrolltext(self) -> Type[self]:
        self.scrolltext = True
        return self
    
    def set_topleft(self) -> Type[self]:
        self.topleft = True
        return self


