def separatecontentPhameasy(saltsynonyms):
    remove = False
    temp = ""
    for char in saltsynonyms :
        if char == '(' :
            remove = True
        if not remove :
            temp += char
        if char == ')' :
            remove = False
    saltsynonyms = temp
    saltsynonyms_temp = saltsynonyms.split('+')
    saltsynonyms = []
    for component in saltsynonyms_temp :
        if component.find('/') != -1 :
            saltsynonyms.append(component.split('/')[0])
            saltsynonyms.append(component.split('/')[1])    
        else :
            saltsynonyms.append(component)
    return saltsynonyms

def separatecontent1mg(saltsynonyms):
    saltsynonyms_temp = saltsynonyms.split('+')
    saltsynonyms = []
    for component in saltsynonyms_temp :
        if component.find('(') != -1 :
            saltsynonyms.append(component.split('(')[0])    
        else :
            saltsynonyms.append(component)
    return saltsynonyms
            