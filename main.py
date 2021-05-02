import PySimpleGUI as sg
import threading
from pathlib import Path
from lib.lang import languages
from lib.fileutils import readText, writeText
from lib.icons import saveIcon, browseIcon, red_x_base64, icon
from lib.translator import start_translate, validateJSON
import pyperclip


sg.theme('DarkBlue')

a = sg.Titlebar(title="sss")


layout = [[sg.Text('Translate your JSON files flawlessely in any language.'), sg.Text(size=(12, 2))], [sg.Text('Source'), sg.Text(' '*54),

                                                                                                       sg.Button('', image_data=browseIcon,
          button_color=(sg.theme_background_color(),
                        sg.theme_background_color()),
          border_width=0, key='pickFile', tooltip=" Open "), sg.Button('', image_data=red_x_base64,
                                                                       button_color=(
                                                                           sg.theme_background_color(), sg.theme_background_color()),
                                                                       border_width=0, key='-CLEAR-A-', tooltip=" Clear "), sg.Text("   Output"),
    sg.Text(' '*52),


    sg.Button('', image_data=saveIcon,
              button_color=(sg.theme_background_color(),
                            sg.theme_background_color()),
              border_width=0, key='saveFile', tooltip=" Save as "),


    sg.Button('', image_data=red_x_base64,

              button_color=(sg.theme_background_color(),
                            sg.theme_background_color()),
              border_width=0, key='-CLEAR-B-', tooltip=" Clear ")
], [sg.FileBrowse("SaveAs", file_types=(("JSON Files", "*.json"),), enable_events=True),
    sg.SaveAs("Open", file_types=(("JSON Files", "*.json"),), enable_events=True)],
    [sg.Multiline(	border_width=1, default_text='Paste your JSON here', size=(45, 20), text_color="white", key='-IN-'),
     sg.Multiline('', size=(45, 20), text_color="white", key='-OUTPUT-', right_click_menu=(0, ["Clear", "Copy to Clipboard"]))], [sg.Text('Status')],

    [sg.Multiline('', key="status", pad=(0, 10), size=(95, 5), autoscroll=True,
                  auto_refresh=True,  reroute_stdout=True, text_color="#00FF00", background_color="black")],
    [sg.Text("Language :"), sg.Combo(list(languages.keys()), key='dropdown', readonly=True, size=(18, 6), tooltip="Select Language", default_value="French"), sg.Text(' '*58), sg.Button('Translate', border_width=2,
                                                                                                                                                                                         button_color=('black', "#51c4d3"),), sg.Button('  About  ', key="About", border_width=2, button_color=('black', "#51c4d3"),), sg.Button('  Exit  ', border_width=2, button_color=('black', "#51c4d3"), key="Exit")],
    [],

]


window = sg.Window(' JSON Translator', layout, icon=icon, finalize=True)
window.FindElement('Open').hide_row()
window.FindElement('SaveAs').hide_row()


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "About":
        sg.popup(' 👨‍💻 anandu467\n\n https://github.com/anandu467',icon=icon)
    if event == 'Translate':
        window["status"].update("")
        window.FindElement('Translate').Update(disabled=True)
        translateButtonDisabled = True
        if(not validateJSON(values['-IN-']) == "valid"):
            sg.popup_error("\nInvalid JSON\n",no_titlebar=True,auto_close=True,auto_close_duration=3,icon=icon)
            window.FindElement('Translate').Update(disabled=False)
        else:
            # print(languages.get(values['dropdown']))
            # change the "output" element to be the value of "input" element
            threading.Thread(target=start_translate, args=(
                values['-IN-'], languages.get(values['dropdown']), window), daemon=True).start()

    if event == "-TRANSLATED-":
        window['-OUTPUT-'].update(values[event])
        window.FindElement('Translate').Update(disabled=False)
    if event == "Copy to Clipboard":
        pyperclip.copy(values["-OUTPUT-"])
    if event in ["Clear", "-CLEAR-B-"]:
        window["-OUTPUT-"].update("")
    if event in ["-CLEAR-A-"]:
        window["-IN-"].update("")
    if event == "pickFile":
        fileBrowseAction = "OPEN"
        window.FindElement('SaveAs').click()

    if event == "SaveAs" and values[event] != "":
        filePath = Path(values[event])
        status = writeText(filePath, values["-OUTPUT-"])
        if (status):
            sg.popup_ok("Saved")
    if event == "Open" and values[event] != "":
        filePath = Path(values[event])
        window["-IN-"].update(readText(filePath))

    if event == "saveFile":

        window.FindElement('Open').click()


window.close()
