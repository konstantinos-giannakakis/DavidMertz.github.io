
__version__ = '$Id: wxpython_interface.py,v 1.4 2006/01/09 16:45:35 yurochek Exp $'

import sys; sys.path.append('..')

import config, re, sys
from wxPython.wx import *

        

class UI:
    def __init__(self):
        pass

    def output(self, text, newline = True):
        """
        If a character can't be displayed, it will be replaced with a
        question mark.
        """
        if newline:
            print text.encode(config.console_encoding, 'replace')
        else:
            # comma at the end means "don't print newline"
            print text.encode(config.console_encoding, 'replace'),

    def input(self, question):
        """
        Works like raw_input(), but returns a unicode string instead of ASCII.

        Unlike raw_input, this function automatically adds a space after the
        question.
        """

        # sound the terminal bell to notify the user
        #sys.stdout.write('\07')
        answer = dialog = wxTextEntryDialog ( None, 'question', 'Title Here', '' )

#tkSimpleDialog.askstring('title', question)
        return answer or ''

    def inputChoice(self, question, options, hotkeys):
        goodAnswer = False
        while not goodAnswer:
            for i in range(len(options)):
                option = options[i]
                hotkey = hotkeys[i]
                m = re.search('[%s%s]' % (hotkey.lower(), hotkey.upper()), option)
                if m:
                    pos = m.start()
                    options[i] = '%s[%s]%s' % (option[:pos], option[pos], option[pos+1:])
                else:
                    options[i] = '%s [%s]' % (option, hotkey)

            prompt = '%s (%s)' % (question, ', '.join(options))
            answer = self.input(prompt)
            if answer.lower() in hotkeys or answer.upper() in hotkeys:
                return answer.lower()
ui = UI()
print ui.input('Test?')