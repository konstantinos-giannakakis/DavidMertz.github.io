"demonstrate that initargs work --fpm"

import pickle, sys, string
import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setParanoia
from UserList import UserList
import funcs

funcs.set_parser()

class foo:
    def __init__(self,a,b,c,fname):

        # test 1 -- unpickler should NOT restore any
        # attributes before __init__ is called
        if len(self.__dict__.keys()) != 0:
            raise "ERROR -- attrs shouldn't exists before __init__"

        self.a = a
        self.b = b
        self.c = c
        self.fh = open(fname,'r')

        print "INITTED OK (%d,%d,%d)"%(a,b,c)
        print self.__dict__.keys()

    # this is also a good test that getstate and getinitargs
    # play nicely with each other

    def __getinitargs__(self):
        # hardcode one arg so we can be sure it's passed
        # and not just the __dict__ value restored
        # (ie after init, c==100, but after __dict__ set,
        # it's correct)
        return (self.a,self.b,100,self.fh.name)

    def __getstate__(self):
        # don't pickle filehandle - restore from initargs filename
        print "**GETSTATE**"
        d = {}
        d.update(self.__dict__)
        del d['fh']
        return d

fh = open('aaa','w')
fh.write('OK')
fh.close()

# use objects with and w/out initargs
# exercise all three cases (toplevel,attr,item)

f = foo(1,2,3,'aaa')
f.g = foo(4,5,6,'aaa')
f.h = UserList(['x','y','z'])
f.l = [foo(7,8,9,'aaa'),UserList(['a','b','c'])]
f.z = [UserList([foo(10,11,12,'aaa')])]

setParanoia(0)

s = pickle.dumps(f)
x = xml_pickle.dumps(f)
print x

print "-----"

print "** expect 100's as last item in sequences"

# uncomment one of the next lines to test xml_pickle/pickle

m = xml_pickle.loads(x)
#m = pickle.loads(s)

# test 2 -- make sure other attrs were restored
if len(m.__dict__.keys()) != 8:
    raise "FAILED TO RESTORE attrs", m.__dict__.keys()

# test 3 -- make sure attrs overwrote anything set in __init__
#           (one could argue it either way, but that's the
#            standard pickle behavior)

print m.a,m.b,m.c
if m.c != 3:
    raise "attributes didn't override initargs!"

try:
    print "Expect: OK y c 11"
    # make sure filehandle was correctly opened from
    # filename passed via initargs
    print m.fh.readline()
    # make sure non-initargs objects are all alive
    print m.h[1]
    print m.l[1][2]
    print m.z[0][0].b
except:
    print "FAILED"

# rigorous testcases from dqm to ensure __init__ isn't
# called when it shouldn't be
from gnosis.util.introspect import instance_noinit

class Old_noinit: pass

class Old_init:
    def __init__(self): print "Init in Old"

if funcs.pyver() >= "2.2":
    class New_slots_and_init(int):
        __slots__ = ('this','that')
        def __init__(self): print "Init in New w/ slots"

    class New_init_no_slots(int):
        def __init__(self): print "Init in New w/o slots"

    class New_slots_no_init(int):
        __slots__ = ('this','that')

    class New_no_slots_no_init(int):
        pass

print "There should be NO text between the following lines:"
print "----------------------------------------------------"
instance_noinit(Old_noinit)
instance_noinit(Old_init)
if funcs.pyver() >= "2.2":
    instance_noinit(New_slots_and_init)
    instance_noinit(New_slots_no_init)
    instance_noinit(New_init_no_slots)
    instance_noinit(New_no_slots_no_init)
print "----------------------------------------------------"

funcs.unlink('aaa')