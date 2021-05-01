import json
from deep_translator import GoogleTranslator

report = "\n\nTranslation Report \n --------------------"
translationCount=0


def translate(data,language):
    global report
    global translationCount
    if(type(data) in  [int,float]):
        return data
    if type(data) ==list:
        return [translate(x,language) for x in data ]
    for x in data:
        if(type(data[x]) == str):
            print("-> "+data[x])
            try:
                data[x] = GoogleTranslator(
                    source='en', target=language).translate(data[x])
                translationCount+=1
            except:
                report += data[x]+" : not translated \n"
        else:
            data[x] = translate(data[x],language)
    return data


# with open(fileName) as inputFile:
#     with open(fileName.split(".")[0]+"_translated.json", "w", encoding="utf-8") as outputFile:
#         data = json.load(inputFile)
#         json.dump(translate(data), outputFile, indent=4, ensure_ascii=False)
#         report+="\n"+str(translationCount)+" records translated"
#         print(report)


def validateJSON(inputJson):
    try:
        json.loads(inputJson)
        return "valid"
    except :
        return "invalid_json"
    

def start_translate(inputText,language,window):
            print("Translation started..")
            global translationCount;
            translationCount=0




            
            data = json.loads(inputText)

            data=translate(data,language)
            print(str(translationCount)+" records translated")
            window.write_event_value("-TRANSLATED-",json.dumps(data,indent=4, ensure_ascii=False))
