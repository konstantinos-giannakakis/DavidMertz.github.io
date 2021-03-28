# -*- coding: utf-8  -*-

__version__ = '$Id: commons_family.py,v 1.7 2005/10/13 21:00:59 leogregianin Exp $'

import family

# The Wikimedia Commons family

class Family(family.Family):
    
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'commons'
        self.langs = {
            'commons': 'commons.wikimedia.org',
        }
        
        self.namespaces[4] = {
            '_default': 'Commons',
        }
        self.namespaces[5] = {
            '_default': 'Commons talk',
        }

    def version(self, code):
        return "1.5"
