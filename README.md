# whiptail-tui
more powerful whiptail python wrapper

## Example
```py

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
```
see `demo.py` for more

## Document
build document using
```bash
cd docs && make html
```