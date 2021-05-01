import PySimpleGUI as sg
from lib.translator import start_translate,validateJSON
import threading
from pathlib import Path
from lang import lang_choices
from lib.fileutils import readText,writeText
import pyperclip
languages={x[1]:x[0] for x in lang_choices}
translateButtonDisabled = False

fileBrowseAction ="OPEN"



sg.theme('DarkBlue')  # please make your windows colorful

a=sg.Titlebar(title="sss")
# sg.SystemTray(

#     filename = "icon.ico"
#   )

saveIcon=b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAByElEQVQ4jdXSz0/acBjH8f4netSQgIT667JdTZaZHXbQ0+LfMWMksuhEN4UpZZrMgy3REKNRYoiyDrpFajd0BEX6LfUHKCIS6V/w8aShtohczPYk79uTV57DQ1H/1dA+pY/2ya6X3ri4IGQuV4SktiIktWAsqc0Jaq66Fx5xp8uXbn4cYwhohuCVV0CKZBHiowjxUWzyMVxXNF09HgG0P3NSE21nlJFqMHGYxgzLYYbl4OMCRnBaAM0Q0P7Mif2L2mS80C+7aIbAwcjo/hiBfJYHt7GBxbV1rH/ndVihfIOO0QjuDnAw8mBNkGYILC4eAwsiAvEslnZVXdxOFu++xWH58ONx0D6dYu8XZo9gm5Rgm6jRpATHbPoetHsP5g1g21Ti591Co9k+JbafH+xlVbwNHJvWy6qNgcv7RcObPGzxT/FpYIefoFTRkLu8QipDTMsXiyiUK08DO78quK5ouCiVoZzmTSuUyri60RoD1dw5fu0mTDvOX+hA6+e/WwbQ6v4dqgbrpbvQLQUNoGVos986IcLh2cOapNRtVSJom9qDzS2ixRl5bQApiqJah8NvLK7w4Hgwul2vseXYVqsz/L7FGTbH/tm5Bdrf2B6CbEEjAAAAAElFTkSuQmCC'
browseIcon=b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAABjElEQVQ4jaXTT0vCcBzH8S907di9TrI/P2V/DDr0BII61jPoeXyrkQuj0qbzEgndhnQL+5U2cClUFBbNlj6KoGt+u6RUbpRz8Lr82N784MMAAAAcZyqBXBCRs98S6M7AWI/jTInIWyJyivAmbJyv/7v3dbOo2JCA1bqI3AgjIUcROQMAABE5WyvUKVtp0O5pPNlKg1at2ruM7jQs5u+clfILLR0HE1kuv9DC4d0JzNtBP13q0W9aoUOa5f+gFzqkl7oj7w7M20EfomLSVp2SZnOIZTySNmvEthuUtl8jol0KD1o+Jc1m6Jmy/0ByZDRGMF3qkbL/QMy8niyoFwOSN2skGy7JhksSXsQIFoORYTTLJ91+Jdlwxw8qufaPYQY06zleUM0/USp7O0Kz/NCgbv8R1AodUg/aI/RiEC+o7N0PR/hOzT+NH2QZL3SQAXnr6v/BtN2l5E4rdJCBVPYm5LsegZp7DP2X41AO2h8g4eURy3jEzOvJZDwS8cIGAAABq3MJ5MIkRONsFgDgEyX9px77ofENAAAAAElFTkSuQmCC'

red_x_base64=b'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAACXBIWXMAAAsTAAALEwEAmpwYAAACV0lEQVQ4ja2UX0hTYRjGf2droxZtUDOVRNofQfxDhBeT4UQIBHFsplKXLrrroqtOF+1SN5JBRAhBhNObrEDmEaPwrgjJiwilVeS2nN0Eq6CbsC1ZF+dbHs88NaLn5vB97/s+33ne7/leif1hBYaAfuCALvYTWAYWgKJB/R6MAClgFLDtE7eJWErkGkIC4oAMmGo42CRy46K2CnEgXAORHkNArLIwi+8IcAiYFmsH0Ad8A77rCJxAACgAP4B3QBfQALwF9QJS7Mp01Lm922Oz95+e9PmzgE9D5nN1+zfHkveeHXO5i+JgRG0KsJjF360DaRHsO3fzdsuJzlOBzmD48Jf8Zk8hs/ESaGofCCZHb0w12xsa3Y2tbStrynwOyAJlYAdok4C7wGWNNKfHH3h1fupOPWABikr0SgYkKRxLeISi4tyli58+vFjpAj6LOhtwSwJmgIiuT76OwdBMaHzSUyEV+1b1ADmbfrx0AVjV1SWN7LH6+tFiRInKGUFmrYEMQPqj3yTJVMbAY0YwIvR1DIanQxOTLexKLgLWcCzhaR8IJtl7+xWUTahvU/vEnN6e3rnQ+PUKWUm5JueUqJzVkrq6/Q9RPVmBDdgxAwcBL/BGBALhicTpI8frXUBpMXo1l36yFClk3itft/K9rWf6HYD1aFPz+poyv4FqG1BfWQ7UZi9o5Nvr3N7tyOyD5x5/4CPVxs5rjG3XtC4lFAGquWVNoQN1dGkl/W6JiNk1ezIwrE/8L8NBi38dXzH+Yq1hah+wVTKNmC3AWdRemTV5lSGwLAhL+sJf07WqI9Q0faYAAAAASUVORK5CYII='
layout = [[sg.Text('Translate your JSON files flawlessely in any language.'), sg.Text(size=(12,2))],[sg.Text('Source'),sg.Text(' '*54),

sg.Button('', image_data=browseIcon,
          button_color=(sg.theme_background_color(),sg.theme_background_color()),
          border_width=0, key='pickFile',tooltip=" Open ")
,sg.Button('', image_data=red_x_base64,
          button_color=(sg.theme_background_color(),sg.theme_background_color()),
          border_width=0, key='-CLEAR-A-',tooltip=" Clear "),sg.Text("   Output"),
          sg.Text(' '*52),
          
          
sg.Button('', image_data=saveIcon,
          button_color=(sg.theme_background_color(),sg.theme_background_color()),
          border_width=0, key='saveFile',tooltip=" Save as "),
          
          
          sg.Button('', image_data=red_x_base64,

          button_color=(sg.theme_background_color(),sg.theme_background_color()),
          border_width=0, key='-CLEAR-B-',tooltip=" Clear ")
],[sg.FileBrowse("SaveAs",file_types=(("JSON Files", "*.json"),),enable_events=True),
sg.SaveAs("Open",file_types=(("JSON Files", "*.json"),),enable_events=True)],
          [sg.Multiline(	border_width=1,default_text='Paste your JSON here', size=(45,20),text_color="white",key='-IN-'),
          sg.Multiline('', size=(45,20),text_color="white",key='-OUTPUT-',right_click_menu=(0,["Clear","Copy to Clipboard"]))]
  ,[sg.Text('Status')],

          [sg.Multiline('',key="status",pad=(0,10),size=(95,5),autoscroll=True,     auto_refresh = True,  reroute_stdout = True,text_color="#00FF00",background_color="black")],
                    [sg.Text("Language :"),sg.Combo(list(languages.keys()),key='dropdown',size=(18,6),tooltip="Select Language",default_value="French"), sg.Text(' '*60),sg.Button('Translate',disabled=translateButtonDisabled,border_width=2,button_color=('black', "#7ACED7"),),sg.Button('  About  ',key="About",border_width=2,button_color=('black', "#7ACED7"),),sg.Button('  Exit  ',border_width=2,button_color=('black', "#7ACED7"),key="Exit")],
                   [],
          
          ]

icon =b'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'
window = sg.Window(' JSON Translator', layout,icon=icon,finalize=True)
window.FindElement('Open').hide_row()
window.FindElement('SaveAs').hide_row()


while True:  # Event Loop
    event, values = window.read()


    # print(event, values)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event=="About":
        sg.popup(' 👨‍💻 anand467\n\n https://github.com/anandu467')
    if event == 'Translate':
        window["status"].update("")
        window.FindElement('Translate').Update(disabled=True)
        translateButtonDisabled=True
        if(not validateJSON(values['-IN-'])=="valid"):
            sg.popup_error("Invalid JSON")
            window.FindElement('Translate').Update(disabled=False)
        else:
        # print(languages.get(values['dropdown']))
        # change the "output" element to be the value of "input" element
            threading.Thread(target=start_translate,args=(values['-IN-'],languages.get(values['dropdown']),window),daemon=True).start()
        
    if event=="-TRANSLATED-":
        window['-OUTPUT-'].update(values[event])
        window.FindElement('Translate').Update(disabled=False)
    if event=="Copy to Clipboard":
        pyperclip.copy(values["-OUTPUT-"])
    if event in ["Clear","-CLEAR-B-"]:
        window["-OUTPUT-"].update("")
    if event in ["-CLEAR-A-"]:
        window["-IN-"].update("")
    if event =="pickFile":
        fileBrowseAction="OPEN"
        window.FindElement('SaveAs').click()

            
    if event=="SaveAs":
        filePath = Path(values[event])
        status=writeText(filePath,values["-OUTPUT-"])
        if (status):
            sg.popup_ok("Saved")
    if event=="Open":
        filePath = Path(values[event])
        window["-IN-"].update(readText(filePath))

                
    if event=="saveFile":

        window.FindElement('Open').click()


       


        



window.close()



