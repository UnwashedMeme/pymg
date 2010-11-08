import csv, re, logging, os.path,itertools,os

def empty(s) : return s == None or len(s) == 0

class Play (object) :
    dispatch_patterns = [('Soundtracks/(?P<album>[^/])+/(.*)\.(?P<ext>.{3,4})','pSoundtrack')]

    #filename_patterns = [('(?P<artist>[^\-]+) - (?P<album>[^\-]+) - (?P<track>[0-9]{1,2}) - (?P<title>[^\-]+)\.(?P<ext>.{3,4})')]

    ext = None
    year = None

    def __init__(self,line) :
        self.__dict__.update(line)
        if self.artist == "" or self.title == "" :
            self.parsePath()

        try :
            if isinstance(self.year,str) and len(self.year) > 0 : self.year = int(self.year)
        except :
            pass

        try :
            if isinstance(self.track,str) and len(self.track) > 0 : self.track = int(self.track)
        except :
            pass
        
        logging.info("Finished parsing %s", self)

    def parsePath(self) :
        logging.debug("Parsing %r", self.path)
        path = re.sub('^(Jazz|Folksy|Country)/', '', self.path)
        for (p,fn) in self.dispatch_patterns :
            m = re.match(p,path)
            if m : 
                getattr(self,fn)(m)
                return
        self.parseFilename()

    def parseFilename(self) :
        m = re.match('(?P<artist>[^\-]+) - (?P<album>[^\-]+) - (?P<track>[0-9]{1,2}) - (?P<title>[^\-]+)\.(?P<ext>.{3,4})',
                     os.path.basename(self.path))
        if m : self.__dict__.update(m.groupdict())
                     

    def pSoundtrack(self,m) :
        logging.debug("soundtrack: %r",m)
        if empty(self.album) : self.album = m.group('album')

    def __str__(self):
        return "%s - %r - %r - %r - %r (%s)" % (self.date,self.artist,self.album, self.track, self.title, self.ext)




            
plays= csv.DictReader(open("logs/mpd_plays.log",'r'), fieldnames=['date','path','artist','album','title','track'])

def makeReader(f) :
    return csv.DictReader(open(f,'r'), fieldnames=['date','path','artist','album','title','track'])

def artfn(p) : return p.artist

if __name__ == '__main__' :
    logging.basicConfig(level=logging.DEBUG)

    allplays = [os.path.join("logs/", n) for n in os.listdir("logs")]
    allplays= [Play(line) for line in itertools.chain(*[makeReader(p) for p in allplays])]
    allplays = sorted(allplays, artfn)



#itertools.groupby(allplays,artfn)
#[(a,len(list(i))) for (a,i) in itertools.groupby(plays,artfn)]

# allplays= [pymg.Play(line) for line in itertools.chain(*[makeReader(p) for p in allplays])]
# allplays = sorted(allplays, key=artfn)
# [(a,len(list(i))) for (a,i) in itertools.groupby(allplays,artfn)]

# second = lambda(l) :l[1]

# acp.sort(key=second)
