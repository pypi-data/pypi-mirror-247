import re

class fuss():

    '''FUSS (Fast Uniform Style String) is a crossable and readable style string format.
Use <style>text</style> to declear style.
Use <item> to declear instanse.

You can parse it to any type, like:

(Minecraft) <blue><bold>A Minecraft Server</all>
(IM) <italic>hello</italic><emoji.happy>
(Terminal) <backspace><mark>foo-bar</mark><CRLF>

To escape, please use backslash(\\).
e.g. Shell Prompt\\>
\\<escape>; \\\\backslash'''

    def __init__(self, src: str) -> None:
        
        self.__src = str()
        self.__style: dict[int, list[str]] = dict()

        escape_lock = False
        style_lock = False

        style = str()
        for i in range(len(src)):

            c = src[i]

            if style_lock == False and escape_lock == True:
                
                if c in ('<', '>', '\\'):
                    self.__src += c
                    escape_lock = False

                else:
                    raise Exception(f'Invalid escape \\{c}') #! errs
                
            elif style_lock == False and escape_lock == False:

                if c == '\\':
                    escape_lock == True
                elif c == '<':
                    style_lock = True
                elif c == '>':
                    raise Exception('please use \\> instead')
                else:
                    self.__src += c

            elif style_lock == True and escape_lock == False:

                if c == '>':

                    idx = len(self.__src)

                    if idx not in self.__style:
                        self.__style[idx] = list()

                    self.__style[idx].append(style)
                    style = ''
                    style_lock = False
                
                elif c not in 'abcdefghijklmnopqrstuvwxyz0123456789_./':
                    raise Exception('unsupport non-idn char currently')

                else:
                    style += c
            
            elif style_lock == True and escape_lock == True:
                pass

        if escape_lock == True:
            raise Exception('uncomplete escape')
        if style_lock == True:
            raise Exception('unclosed <>')

    def __str__(self) -> str:
        return self.__src
    
    def __repr__(self) -> str:
        
        result = str()
        imax = len(self.__src)
        for i in range(imax):

            if i in self.__style:
                for style in self.__style[i]:
                    result += f'<{style}>'

            if self.__src[i] in ('<', '>', '\\'):
                result += '\\'

            result += self.__src[i]

        if imax in self.__style:
            for style in self.__style[imax]:
                result += f'<{style}>'

        return result