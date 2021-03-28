# -*- coding: utf-8  -*-
import family, config

# Linpedia.org, the GNU/Linux encyclopedia

class Family(family.Family):

    def __init__(self):
        family.Family.__init__(self)
	self.name = 'wikitech'
	
        self.langs = {
            'en':'wikitech.leuksman.com',
        }

# Namespaces
        
        self.namespaces[4] = {
	    '_default': u'Wikitech',
	    }
	self.namespaces[5] = {
	    '_default': u'Wikitech talk',
	    }
	
    def version(self, code):
        return "1.6alpha"

    def path(self, code):
        return '/index.php'