#!/usr/bin/env python3
# Note, this code should work in both python 2 and 3.

def htmlReplaceReserved(code):
    '''
    Replace reserved HTML characters (&<>") with appropriate entity (&amp;&lt;&gt;&quot;).
    
    code: str
        text that may contain reserved characters.

    returns text with reserved charaters replaced with entities.
    '''
    return code.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def pullWhitespace(code, sPos):
    '''
    Pulls out whitespace from a starting postion and get new position.
    
    code: str
        all code.
    sPos: int
        starting postion.

    returns: whitespace (str), new starting position
    '''
    ePos = sPos
    while(ePos < len(code) and code[ePos].isspace()):
        ePos += 1
    return code[sPos:ePos], ePos

def pullDocstring(code, sPos):
    '''
    Pulls out docstring from a starting postion and get new position.
    
    code: str
        all code.
    sPos: int
        starting postion.

    returns: docstring (str), new starting position, error occured (bool)
    '''

    ePos = sPos+3
    if(ePos > len(code)):
        raise ValueError("Remaining string too short for docstring: %s" % (code[sPos:]))
    quoteStr = code[ePos-3: ePos]
    ePos+=1
    if(not quoteStr in ["'''",'"""']):
        raise ValueError("A docstring must start with (''') or (\"\"\"), not (%s)." % quoteStr)
    strEnded = False
    while(not strEnded and ePos < len(code)):
        if(code[ePos-3:ePos] == quoteStr):
            strEnded = True
        ePos+=1
    return code[sPos:ePos], ePos, strEnded

def pullString(code, sPos):
    '''
    Pulls out string from a starting postion and get new position.
    
    code: str
        all code.
    sPos: int
        starting postion.
    
    returns: string (str), new starting position, error occured (bool)
    '''
    quoteStr = code[sPos]
    if(not quoteStr in ["'",'"']):
        raise ValueError("A string must start with (') or (\"), not (%s)." % quoteStr)
    strEnded = False # the string has ended (error check)
    ePos = sPos+1
    while(not strEnded and ePos < len(code) and not code[ePos] == '\n'):
        # note, newlines in str not after "\" will cause an error in python
        if(code[ePos] == quoteStr):
            strEnded = True
        elif(code[ePos]=='\\' and ePos+1<len(code)):
            # breaking character, skip next
            ePos+=1
        ePos+=1
    return code[sPos:ePos], ePos, strEnded

def pullNumber(code,sPos):
    '''
    Pulls out number from a starting postion and get new position.
    
    code: str
        all code.
    sPos: int
        starting postion.

    returns: number (str), new starting position
    '''
    ePos = sPos
    while(ePos < len(code) and (code[ePos].isdigit()) or code[ePos] in ['.','e','E']):
        ePos+=1
    return code[sPos:ePos], ePos

def pullIdentifier(code, sPos):
    '''
    Pulls out identifier from a starting postion and get new position.
    
    code: str
        all code.
    sPos: int
        starting postion.

    returns: identifier (str), new starting position
    '''
    if(not (sPos < len(code) and (code[sPos].isalpha() or code[sPos] == '_'))):
        # null return
        return '', sPos
    ePos = sPos+1
    while(ePos < len(code) and (code[ePos].isalnum() or code[ePos] == '_')):
        ePos += 1
    return code[sPos:ePos], ePos

def pyToHTML(code, lineNums=False):
    '''
    Converts raw Python code into HTML that can be formatted (with the aid of CSS). 
    
    code: str
        Python code.
    lineNums: (default: False)
    
    returns HTML code string.
    
    HTML classes named:
        python: whole object
        codeLN: line numbers region
        codeText: Python code
        codeDocstr: docstring (includes quotes)
        codeStr: string (includes quotes)
        codeNum: number
        codeWord: identifier (e.g., variable name, function name)
        codeDefCnst: built-in constant (e.g., True, None)
        codeBuiltIn: built-in object (e.g., len, str, help)
        codeKey: keyword (e.g., if, raise, and)
        codeComm: comment
        codeErr: error (e.g., unclosed string)
        
    Note that "print" is treated as a built-in function not a keyword (Python 3-style).
    '''
    kwCnst = ['False', 'None', 'True']
    kwList = ['and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 
              'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global',
              'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise',
              'return', 'try', 'while', 'with', 'yield']
    baseFuncts = ['abs', 'delattr', 'hash', 'memoryview', 'set', 'all', 'dict', 'help', 'min', 
                  'setattr', 'any', 'dir', 'hex', 'next', 'slice', 'ascii', 'divmod', 'id', 
                  'object', 'sorted', 'bin', 'enumerate', 'input', 'oct', 'staticmethod', 'bool', 
                  'eval', 'int', 'open', 'str', 'breakpoint', 'exec', 'isinstance', 'ord', 'sum', 
                  'bytearray', 'filter', 'issubclass', 'pow', 'super', 'bytes', 'float', 'iter', 
                  'print', 'tuple', 'callable', 'format', 'len', 'property', 'type', 'chr', 
                  'frozenset', 'list', 'range', 'vars', 'classmethod', 'getattr', 'locals', 
                  'repr', 'zip', 'compile', 'globals', 'map', 'reversed', '__import__', 'complex', 
                  'hasattr', 'max', 'round']
    
    outHTML = ""
    strI = 0
    while(strI < len(code)):
        preI = strI
        if(code[strI].isspace()):
            # whitespace
            temp, strI = pullWhitespace(code, strI)
            outHTML += htmlReplaceReserved(temp)
        elif(strI+3 <= len(code) and code[strI:strI+3] in ["'''",'"""']):
            # docstring
            temp, strI, goodStr = pullDocstring(code, strI)
            outHTML += "<span class='codeDocstr%s'>%s</span>" % \
                ((' codeErr','')[goodStr], htmlReplaceReserved(temp))
        elif(code[strI] in ["'",'"']):
            # string
            temp, strI, goodStr = pullString(code, strI)
            outHTML += "<span class='codeStr%s'>%s</span>" % \
                ((' codeErr','')[goodStr], htmlReplaceReserved(temp))
        elif(code[strI].isdigit()):
            # number
            temp, strI = pullNumber(code, strI)
            outHTML += "<span class='codeNum'>%s</span>" % (htmlReplaceReserved(temp))
        elif(code[strI].isalnum() or code[strI] == '_'):
            # identifier (function, variable, keyword, etc.)
            temp, strI = pullIdentifier(code, strI)
            if(temp in kwCnst): # defined constant
                htmlClass = 'codeDefCnst'
            elif(temp in kwList): # keyword
                htmlClass = 'codeKey'
            elif(temp in baseFuncts): # built-in function
                htmlClass = 'codeBuiltIn'
            else: # generic identifier
                htmlClass = 'codeWord'
            outHTML += "<span class='%s'>%s</span>" % (htmlClass, htmlReplaceReserved(temp))
        elif(code[strI] == '.'):
            # period then numbr or member of something
            strI+=1
            if(strI < len(code) and code[strI].isdigit()):
                # number
                temp, strI = pullNumber(code, strI)
                outHTML += "<span class='codeNum'>.%s</span>" % (htmlReplaceReserved(temp))
            else:
                # member of something
                temp, strI = pullIdentifier(code, strI)
                outHTML += ".<span class='codeWord'>%s</span>" % (htmlReplaceReserved(temp))
        elif(code[strI] == '#'):
            # comment
            ePos = code.find('\n',strI)
            if(ePos<0):
                ePos = len(code)
            outHTML += "<span class='codeComm'>%s</span>" % (htmlReplaceReserved(code[strI:ePos]))
            strI = ePos
        else:
            # Punctuation/operations/other
            outHTML += htmlReplaceReserved(code[strI])
            strI+=1
        if(preI >= strI): # didn't move forward (prevent infinite loop)
            outHTML += "<span class='codeErr'>%s</span>" % (htmlReplaceReserved(code[preI]))
            strI = preI+1
    if(lineNums):
        lineN = code.count('\n')+1
        lnText = ''.join(['<div>%d</div>'%i for i in range(1,lineN+1)])
        return "<pre class='python'><table><tbody style='vertical-align:top;'><tr><td><div class='codeLN'>%s</div></td>" \
            "<td><div class='codeText'>%s</div></td></tr></tbody></table></pre>" % (lnText, outHTML)
    else:
        return "<pre class='python'><div class='codeText'>%s</div></pre>" % (outHTML)
    
