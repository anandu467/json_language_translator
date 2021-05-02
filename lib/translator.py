import json
from deep_translator import GoogleTranslator

translationCount=0

def translate(data,language):

    if not (data): return data
    dataType=type(data)
    translator=getTranslator(dataType)
    return translator(data,language)


def getTranslator(dataType):
    tranlatorMap={
        int:translateInt,
        float:translateInt,
        list:translateList,
        str:translateWord,
        dict:translateDict
    }
    return tranlatorMap[dataType]

def translateWord(word,language):
    if(not shouldTranslate(word)):
        return word
    try:
        logTranslation(word)
        word =GoogleTranslator(
                    source='en', target=language).translate(word)
        incrementTranslationCount()
    except:
        print("Error translating ",word)
        pass
    return word
def translateList(wordList,language):
    return [translate(x,language) for x in wordList]
def translateInt(word,language):
    return word
def translateDict(wordDict,language):
        for key in wordDict:
            value = wordDict[key]

            wordDict[key] = translate(value,language)
        return wordDict

def shouldTranslate(word):
    return type(word) == str and word.strip() !="" and not word.isdigit()
def validateJSON(inputJson):
    try:
        json.loads(inputJson)
        return "valid"
    except :
        return "invalid_json"
def logTranslation(word):
    print("-> ",word)    
def incrementTranslationCount():
    global translationCount;
    translationCount +=1
def start_translate(inputText,language,window):
            print("Translation started..")
            global translationCount;
            translationCount=0
            data = json.loads(inputText)
            data=translate(data,language)
            print(str(translationCount)+" records translated")
            window.write_event_value("-TRANSLATED-",json.dumps(data,indent=4, ensure_ascii=False))
