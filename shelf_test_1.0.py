import shelve

## http://docs.python.org/2/library/shelve.html

filename = 'test_shelf.db'
key = 'key1'

d = shelve.open(filename)

class pet:
    number_of_legs = 0

    def sleep(self):
        print "zzz"

    def count_legs(self):
        print "I have %s legs" % self.number_of_legs

doug = pet()
doug.number_of_legs = 4

d[key] = 'string1'
d['key2'] = [1, 2, 3, 4]
d['key3'] = doug 

d.close()
