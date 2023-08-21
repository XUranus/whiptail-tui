#!/usr/bin/env python3
#
#  whiptail_box.py

# stdlib
from __future__ import annotations
from typing import Optional, Sequence, Type, Callable, Any
import itertools
import re
import threading
import subprocess
# third part
from .whiptail_base import Response, WhiptailBase, POSITIVE_RETURN_CODE

DEFAULT_FORM_ITEM_PLACEHOLDER_LEN : int = 20

class WhiptailMessageBox(WhiptailBase):
    """
    Message box is used to display text message, it has only an ``ok`` button.

    :param message: the text message to display
    :param on_ok: event to trigger when ok button is pushed
    """
    def __init__(self,
        message : str,
        height : Optional[int],
        width : Optional[int],
        on_ok : Callable[[], Any] = lambda : None):
        super().__init__(box = 'msgbox', text = message, height = height, width = width)
        self.on_ok = on_ok
    
    def on_positive_event_triggered(self, value : str) -> None:
        """
        msgbox only has positive event, bind it to ``on_ok``
        """
        self.on_ok()
        pass
    

class WhiptailYesNo(WhiptailBase):
    """
    Display a yes/no dialog box.

    The string specified by ``message`` is displayed inside the dialog box.
    If this string is too long to be fit in one line, it will be automatically
    divided into multiple lines at appropriate places.
    The text string may also contain the newline character ``\n`` to control line breaking explicitly.

    This dialog box is useful for asking questions that require the user to answer either yes or no.
    The dialog box has a ``Yes`` button and a ``No`` button, in which the user can switch between
    by pressing the ``TAB`` key.

    :param message: The message to display in the dialog box
    """
    def __init__(self,
        message : str,
        height : Optional[int],
        width : Optional[int],
        on_yes : Callable[[], Any] = lambda : None,
        on_no : Callable[[], Any] = lambda : None):
        super().__init__(box = 'yesno', text = message, height = height, width = width)
        self.on_yes = on_yes
        self.on_no = on_no
    
    def on_positive_event_triggered(self, value : str) -> None:
        """
        triggered when ``'yes'`` selected, bind it to ``on_yes``
        """
        self.on_yes()
        pass

    def on_negative_event_triggered(self) -> None:
        """
        triggered when ``'no'`` selected, bind it to ``on_no``
        """
        self.on_no()
        pass


class WhiptailInfoBox(WhiptailBase):
    """
    Info is similar to the message box but the difference is unlike the message box
    info box will not wait for the user input.
    Use –-infobox flag and pass a string as an argument which will be displayed in the info box.

    In some shells, info box will run but will not display any result.
    You have to change the terminal emulation.

    :param message: The message to display in the dialog box
    """
    def __init__(self,
        message : str,
        height : Optional[int],
        width : Optional[int]):
        super().__init__(box = 'infobox', text = message, height = height, width = width)

    def on_positive_event_triggered(self, value : str) -> None:
        """
        info box will always return positive returncode, no event need to bind
        """
        pass


class WhiptailTextBox(WhiptailBase):
    """
    A text box lets you display the contents of a text file in a dialog box.
    It is like a simple text file viewer. The user can move through the file by using
    the ``UP``/``DOWN``, ``PGUP``/``PGDN`` and ``HOME``/``END`` keys available on most keyboards.
    If the lines are too long to be displayed in the box, the ``LEFT``/``RIGHT`` keys can be used
    to scroll the text region horizontally. For more convenience, forward and backward searching
    functions are also provided.

    :param textfile: path of the text file to display
    :param on_ok: event to trigger when ok button is pushed
    :param on_failed: event to trigger when file is failed to open
    """
    def __init__(self,
        textfile : str,
        height : Optional[int],
        width : Optional[int],
        on_ok : Callable[[], Any] = lambda : None,
        on_failed : Callable[[], Any] = lambda : None):
        super().__init__(box = 'textbox', text = textfile, height = height, width = width)
        self.on_ok = on_ok
        self.on_failed = on_failed
    
    def on_positive_event_triggered(self, value : str) -> None:
        """
        triggered when ``ok`` button pushed when file opened and displayed normally, bind it to ``on_ok``
        """
        self.on_ok()
        pass

    def on_esc_event_triggered(self) -> None:
        """
        triggered when file open failed, bind it to ``on_failed``
        """
        self.on_failed()
        pass


class WhiptailMenuItem:
    """
    Wrap the menu box item.

    WhiptailMenuItem one of the members in a WhiptailMenuBox, it can be displayed in the menu and selected.

    :param key: The text message to display. Key is also used to distinguish the item from other item, must be unique.
    :param description : The menu item description followed by the ``key``,
        only to be shown when WhiptailMenuBox enable description.
    :param data: The payload to be passed to ``on_selected`` callback function.
    :param on_selected: Event callback function to be triggered when the item is selected. 
    """
    def __init__(
        self,
        key : str,
        description : str = '',
        data : Any = None,
        on_selected : Callable[[Type[data]], Any] = lambda _ : None):
        self.key = key
        self.description = description
        self.data = data
        self.on_selected = on_selected


class WhiptailMenuBox(WhiptailBase):
    """
    Wrap the menu box base of whiptail menu

    Menu box is a dialog box used to present a list of choice in the form of a menu for user to choose.

    Each menu entry consists of a tag string and an item string.
		The tag gives the entry a name to distinguish it from the other entries in the menu.
		The item is a short description of the option that the entry represents.
		The user can move between the menu entries by pressing the ``UP``/``DOWN`` keys,
		the first letter of the tag as a hot-key. There are menu-height entries displayed
		in the menu at one time, but the menu will be scrolled if there are more entries than that.

    :param message: The message to display in the dialog box.
    :param items: A sequence of items to display in the menu.
    :param prefix: The prefix string to be show in front of menu item text.
    :param description: If to show description in WhiptailMenuItem.
    :param items: A sequence of WhiptailMenuItem, you can config the text and event in this struct.
    :param on_cancel: The event callback to be trigger when menu canceled with nothing selected.
    """
    def __init__(
        self,
        message : str,
        height : Optional[int],
        width : Optional[int],
        prefix : str = '-',
        description : str = False,
        items : Sequence[WhiptailMenuItem] = (),
        on_cancel : Callable[[], Any] = lambda : None):
        super().__init__(box = 'menu', text = message, height = height, width = width)
        self.prefix = prefix
        self.description = description
        self.items = items
        self.on_cancel = on_cancel
        # validate items have unique key
        if len(set([item.key for item in self.items])) != len(self.items):
            raise Exception("menu items must have unique key!")
        # build box extra args
        menu_item_args = [(item.key, '{} {}'.format(self.prefix, item.description) \
            if self.description else '') for item in self.items]
        menu_item_args = list(itertools.chain.from_iterable(menu_item_args)) # flatten the list
        self.box_extra_args = [str(self.get_default_list_height())] + menu_item_args

    def on_positive_event_triggered(self, value : str) -> None:
        """
        triggered when item selected, bind it to ``on_selected`` of corresponding WhiptailMenuItem
        """
        for item in self.items:
            if item.key == value:
                item.on_selected(item.data)
                return
        raise Exception(f"no items found! key = {value}")

    def on_negative_event_triggered(self) -> None:
        """
        triggered when ``'cancel'`` button pushed, bind it to ``on_cancel``
        """
        self.on_cancel()
        pass


class WhiptailInputBox(WhiptailBase):
    """
    An input box is useful when you want to ask questions that require the user to input a string as the answer.
    If ``placeholder`` is supplied it is used to initialize the input string.
    When inputting the string, the ``BACKSPACE`` key can be used to correct typing errors. If the input string
    is longer than the width of the dialog box, the input field will be scrolled.

    If ``password`` is :py:obj:`True`, the text the user enters is not displayed.
    This is useful when prompting for passwords or other sensitive information.
    Be aware that if anything is passed in "init", it will be visible in the system's
    process table to casual snoopers. Also, it is very confusing to the user to provide
    them with a default password they cannot see. For these reasons, using "init" is highly discouraged.

    :param message: The message to display in the dialog box
    :param placeholder: A default value for the text
    :param password: Whether the text being entered is a password, and should be replaced by ``*``. Default :py:obj:`False`
    :param validator: Check if the input is valid, if it's invalid, input box will forbid to submit
    :param error_message: Message to display if input is not invalid. 
    """
    def __init__(
        self,
        message : str,
        height : Optional[int],
        width : Optional[int],
        placeholder : str = '',
        password : bool = False,
        validator : Callable[[str], bool] = lambda _ : True,
        error_message : str = 'invalid input!',
        on_submit : Callable[[str], Any] = lambda _ : None,
        on_cancel : Callable[[], Any] = lambda : None):
        super().__init__(box = 'passwordbox' if password else 'inputbox' , \
            text = message, height = height, width = width)
        self.placeholder    : str                      = placeholder
        self.password       : bool                     = password
        self.validator      : Callable[[str], bool]    = validator
        self.error_message  : str                      = error_message
        self.on_submit      : Callable[[str], Any]     = on_submit
        self.on_cancel      : Callable[[], Any]        = on_cancel
        # build box extra args
        self.box_extra_args = [self.placeholder]

    def refresh(self):
        self.show()

    def on_positive_event_triggered(self, value : str) -> None:
        """
        triggered when input box ``ok`` button pushed, bind it to ``on_submit``
        """
        if not self.validator(value):
            # pop a message box to display error message
            WhiptailMessageBox(
                message = self.error_message,
                height = self.height,
                width = self.width).show()
            # re-render
            self.refresh()
        self.on_submit(value)
        pass

    def on_negative_event_triggered(self) -> None:
        """
        triggered when input box ``cancel`` button pushed, bind it to ``on_cancel``
        """
        self.on_cancel()


class WhiptailSelectItem:
    """
    Wrap the checklist/radio box item.

    WhiptailSelectItem one of the members in a WhiptailCheckListBox or WhiptailRadioListBox, it can be displayed in the list and selected.

    :param key: The text message to display. Key is also used to distinguish the item from other item, must be unique.
    :param description : The menu item description followed by the ``key``,
        only to be shown when WhiptailCheckListBox/WhiptailRadioListBox enable description.
    """
    def __init__(
        self,
        key : str,
        description : str = ''):
        self.key         : str = key
        self.description : str = description
        self.selected    : bool = False


class WhiptailCheckListBox(WhiptailBase):
    """
    A checklist box is similar to a menu box in that there are multiple entries presented in the form of a menu.

    You can select and deselect items using the SPACE key.
    The initial on/off state of each entry is specified by status.

    :param message: The message to display in the dialog box
    :param items: A sequence of items to display in the checklist
    :param prefix:
    """
    def __init__(
        self,
        message : str,
        height : Optional[int],
        width : Optional[int],
        prefix : str = '-',
        description : str = False,
        items : Sequence[WhiptailSelectItem] = (),
        on_cancel : Callable[[], Any] = lambda : None,
        on_submit : Callable[[Sequence[str]], Any] = lambda _ : None):
        super().__init__(box = 'checklist', text = message, height = height, width = width)
        self.prefix = prefix
        self.description = description
        self.items = items
        self.on_cancel = on_cancel
        self.on_submit = on_submit
        # validate items have unique key
        if len(set([item.key for item in self.items])) != len(self.items):
            raise Exception("checkbox list items must have unique key!")
        # build box extra args
        menu_item_args = [(item.key, '{} {}'.format(self.prefix, item.description) \
            if self.description else '', "ON" if item.selected else "OFF") \
            for item in self.items]
        menu_item_args = list(itertools.chain.from_iterable(menu_item_args)) # flatten the list
        self.box_extra_args = [str(self.get_default_list_height())] + menu_item_args

    def on_positive_event_triggered(self, value : str) -> None:
        """
        triggered when input box ``ok`` button pushed, bind it to ``on_submit``
        """
        keys = re.findall(r'"([^"]*)"', value)
        self.on_submit(keys)
        pass

    def on_negative_event_triggered(self) -> None:
        """
        triggered when input box ``cancel`` button pushed, bind it to ``on_cancel``
        """
        self.on_cancel()


class WhiptailRadioListBox(WhiptailBase):
    """
    A radiolist box is similar to a menu box.

    The only difference is that you can indicate which entry is currently selected,
    by setting its status to on.

    :param message: The message to display in the dialog box.
    :param items: A sequence of items to display in the radiolist.
    :param prefix: The prefix string to be show in front of item text.
    """
    def __init__(
        self,
        message : str,
        height : Optional[int],
        width : Optional[int],
        prefix : str = '-',
        description : str = False,
        items : Sequence[WhiptailSelectItem] = (),
        on_cancel : Callable[[], Any] = lambda : None,
        on_submit : Callable[[str], Any] = lambda _ : None):
        super().__init__(box = 'radiolist', text = message, height = height, width = width)
        self.prefix = prefix
        self.description = description
        self.items = items
        self.on_cancel = on_cancel
        self.on_submit = on_submit
        # validate items have unique key
        if len(set([item.key for item in self.items])) != len(self.items):
            raise Exception("radiolist list items must have unique key!")
        # build box extra args
        menu_item_args = [(item.key, '{} {}'.format(self.prefix, item.description) \
            if self.description else '', "ON" if item.selected else "OFF") \
            for item in self.items]
        menu_item_args = list(itertools.chain.from_iterable(menu_item_args)) # flatten the list
        self.box_extra_args = [str(self.get_default_list_height())] + menu_item_args

    def on_positive_event_triggered(self, value : str) -> None:
        """
        triggered when input box ``ok`` button pushed, bind it to ``on_submit``
        """
        self.on_submit(value)
        pass

    def on_negative_event_triggered(self) -> None:
        """
        triggered when input box ``cancel`` button pushed, bind it to ``on_cancel``
        """
        self.on_cancel()


class WhiptailFormItem:
    """
    WhiptailFormItem one of the members in a WhiptailFormBox, it's used to represent an form item.

    :param key: The text message to display. Key is also used to distinguish the item from other item, must be unique.
    :param name: The form item name.
    :param password: If is password input
    :param value : The form item value.
    """
    def __init__(
        self,
        key : str,
        name : str,
        password : bool = False,
        value : str = DEFAULT_FORM_ITEM_PLACEHOLDER_LEN * ' ',
        validator : Callable[[str], bool] = lambda _ : True,
        error_message : str = 'invalid input!'):
        self.key        : str   = key
        self.name       : str   = name
        self.password   : bool  = password
        self.value      : str   = value
        self.validator : Callable[[str], bool] = validator
        self.error_message : str = error_message 


class WhiptailFormBox(WhiptailBase):
    """
    A form box is not a native box from whiptail, it's created using menu box and input box.

    :param message: The message to display in the dialog box.
    :param items: A sequence of items to display in the radiolist.
    """
    def __init__(
        self,
        message : str,
        height : Optional[int],
        width : Optional[int],
        items : Sequence[WhiptailFormItem] = (),
        submit_button : str = 'submit',
        on_cancel : Callable[[], Any] = lambda : None,
        on_submit : Callable[[list], Any] = lambda _ : None):
        super().__init__(box = 'menu', text = message, height = height, width = width)
        self.prefix = '-'
        self.items = items
        self.on_cancel = on_cancel
        self.on_submit = on_submit

        self.submit_button = submit_button
        # validate items have unique key
        if len(set([item.key for item in self.items])) != len(self.items):
            raise Exception("radiolist list items must have unique key!")
        # build box extra args
        menu_item_args = [(item.key, len(item.value) * '*' if item.password else item.value) \
            for item in self.items]
        menu_item_args = [(item[0], '{} {}'.format(self.prefix, item[1])) for item in menu_item_args]
        menu_item_args.append(('', '[{}]'.format(self.submit_button)))
        menu_item_args = list(itertools.chain.from_iterable(menu_item_args)) # flatten the list
        self.box_extra_args = [str(self.get_default_list_height())] + menu_item_args

    def refresh(self) -> None:
        # refresh box extra args
        menu_item_args = [(item.key, len(item.value) * '*' if item.password else item.value) \
            for item in self.items]
        menu_item_args = [(item[0], '{} {}'.format(self.prefix, item[1])) for item in menu_item_args]
        menu_item_args.append(('', '[{}]'.format(self.submit_button)))
        menu_item_args = list(itertools.chain.from_iterable(menu_item_args)) # flatten the list
        self.box_extra_args = [str(self.get_default_list_height())] + menu_item_args
        self.show()
        pass

    def on_positive_event_triggered(self, value : str) -> None:
        """
        triggered when input box ``ok`` button pushed, bind it to ``on_submit``
        """
        menu_key = value
        if menu_key == '':
            form_data = [{'name' : item.name, 'value' : item.value.strip()} for item in self.items]
            self.on_submit(form_data)
            return
        for item in self.items:
            if item.key == menu_key:
                # create a inputbox to edit value for menu_key
                response = WhiptailInputBox(
                    message = item.key,
                    height = self.height,
                    width = self.width,
                    placeholder = item.value.strip(),
                    password = item.password,
                    validator = item.validator,
                    error_message = item.error_message).show()
                if response.returncode == POSITIVE_RETURN_CODE:
                    item.value = response.value
                self.refresh()
                return
        raise Exception(f"unknown form key: {value}")

    def on_negative_event_triggered(self) -> None:
        """
        triggered when input box ``cancel`` button pushed, bind it to ``on_cancel``
        """
        self.on_cancel()


class WhiptailGaugeBox(WhiptailBase):
    """
    wrap the progress bar box base of whiptail gauge
    """
    def __init__(self,
        message : str,
        height : Optional[int],
        width : Optional[int],
        percent : int = 0):
        super().__init__(box = 'gauge', text = message, height = height, width = width)
        self.percent : int = percent
        # validate items have unique key
        if percent > 100:
            raise Exception(f"gauge percent greater than 100! ({percent})")
        self.box_extra_args = [str(percent)]
        self.thread = None
    
    def listen(self) -> Type[self]:
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
        self.process = subprocess.Popen(cmd, stdin = subprocess.PIPE, stderr=subprocess.PIPE, text = True)
        self.thread = threading.Thread(target = self.start)
        return self

    def start(self) -> Response:
        _, err = self.process.communicate()
        # err is the selected key str
        return Response(self.process.returncode, err)

    def update_percent(self, percent : int) -> None:
        if percent > 100 or percent < 0:
            raise Exception("percent must in 1..100!")
        self.percent = percent
        self.process.stdin.write(f"{percent}\n")
        self.process.stdin.flush()

    def terminate(self) -> None:
        self.process.stdin.close()

