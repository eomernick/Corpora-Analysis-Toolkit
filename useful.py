## Generic Python Code for wide ranges of Applications
## 
## Eli Omernick
## Summer 2012
import math, os, re, pickle 
from collections import defaultdict

################################################################################
############################# String Manipulations #############################
################################################################################

def tokenize(sText, pairing = False):
    '''Given a string of text sText, returns a list of the individual stemmed tokens that 
        occur in that string (in order). This is my quick and dirty Tokenizer. 
        Satisfaction Not Guarenteed'''
    import string
    from stemmer import PorterStemmer
    sText = sText.lower()
    sText = re.sub("&#8217;", "'", sText)
    sText = re.sub("&.{0,6};", " ", sText)
    sText = re.sub("[\x80-\xff]", "", sText)
    sText = sText.split(None)
    for p in string.punctuation.replace("'", ""):
        try:
            sText = mapAndFold(lambda x: x.split(p), sText)
        except TypeError: # empty string
            return []
    sText = mapAndFold(lambda x: x.split(), sText)
    sText = map(lambda x: x.strip("\'"), sText)
    sText = map(lambda x: x.strip("\""), sText)
    sText = map(lambda x: x.strip("_"), sText)
    sText = filter(lambda x: not re.match("\d+", x), sText)
    sText = filter(lambda x: not x == "", sText)
    sText = filter(lambda x: not x[0] == "@", sText)
    stemmer = PorterStemmer()
    if pairing:
        #return original with token val in tuple
        return [(w,stemmer.stem(w, 0, len(w)-1)) for w in sText]
    return [stemmer.stem(w, 0, len(w)-1) for w in sText]

def unescape(text):
    '''Escapes Unicode encodings in Ascii and returns the unicode string
        Based on a method by Juan Manuel Caicedo Carvajal available here:
        https://bitbucket.org/cavorite/webscraping/src/39d8485f827b/common.py'''
    from urllib2 import unquote
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#" or text[:2] == "\\u":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    r = re.sub("&#?\w+;", fixup, text)
    r = re.sub("%([\da-fA-F]{2})%([\da-fA-F]{2})%([\da-fA-F]{2})",lambda x: unicode(unquote(x.group(0)), 'utf-8'), r)
    r = re.sub("\\u(\d+ )", lambda x: unichr(int(x.group(1))), r)
    return r

def mapAndFold(fun, lst):
    '''maps fun onto a list then merges resulting list into one useful for several iterations of mapping functions which return lists, which would otherwise return lists of lists'''
    return reduce((lambda x, y: x+y),map(fun, lst))

def formatFloat(f, places = 2):
    '''concats float f to places places after the decimal.'''
    f = str(f)
    sides = f.split(".")
    right = sides[1][:min(places, len(sides[1]))]
    return float(sides[0]+"."+right)

def formatTuple(t):
    '''strips punctuation from tuple string'''
    if type(t) == tuple:
        return " ".join(t)
    return t

################################################################################
################################## Statistics ##################################
################################################################################

def average(x):
    assert len(x) > 0
    return float(sum(x)) / len(x)

def median(x):
    x.sort()
    return x[len(x)/2]

def mode(x):
    tallies = defaultdict(int)
    for i in x:
        tallies[i] += 1
    return sorted(tallies.items(), key=lambda x: x[1], reverse = True)[0][0]

def pearsons(x, y):
    assert len(x) == len(y)
    n = len(x)
    assert n > 0
    avg_x = average(x)
    avg_y = average(y)
    diffprod = 0
    xdiff2 = 0
    ydiff2 = 0
    for idx in range(n):
        xdiff = x[idx] - avg_x
        ydiff = y[idx] - avg_y
        diffprod += xdiff * ydiff
        xdiff2 += xdiff * xdiff
        ydiff2 += ydiff * ydiff

    if xdiff2 * ydiff2 == 0: # Boundary case
        if diffprod == 0: # No change
            return 0.0
        return diffprod / abs(diffprod) # perfect coorelation 
    return diffprod / math.sqrt(xdiff2 * ydiff2)

def stDev(values):
    size = len(values)
    s = sum(values)
    ave = average(values)
    sumDiff2 = 0.0
    for n in values:
        sumDiff2 += (n - ave)**2
    return math.sqrt(sumDiff2 / size)

def studentsTTest((m1,s1,n1),(m2,s2,n2)):
    '''returns t-val for the 2 distributions described
        @param m=mean, s=stDev, n=number of vals in distribution
        For use with small datasets'''
    sPool = (s1**2)*(n1-1)+(s2**2)*(n2-1)
    sPool = math.sqrt(sPool/(n1+n2-2))
    return ((m1-m2)/sPool)*(n1*n2/(n1+n2))

def tTest((m1,s1,n1),(m2,s2,n2)):
    '''returns t-val for the 2 distributions described
        @param m=mean, s=stDev, n=number of vals in distribution
        For use with large datasets'''
    return (m1-m2)/math.sqrt((s1**2/n1)+(s2**2/n2))

################################################################################
################################### File IO ####################################
################################################################################
    
def save(dObj, sFilename):
    '''Given an object and a file name, write the object to the file using pickle.'''
    
    f = open(sFilename, "w")
    p = pickle.Pickler(f)
    p.dump(dObj)
    f.close()

def load(sFilename):
    '''Given a file name, load and return the object stored in the file.'''
    
    f = open(sFilename, "r")
    u = pickle.Unpickler(f)
    dObj = u.load()
    f.close()
    return dObj

def loadFile(sFilename):
    '''Given a file name, return the contents of the file as a string.'''
    f = open(sFilename, "r")
    sTxt = f.read()
    f.close()
    return sTxt
    
def ddictToDict(ddict):
    '''recursively converts defaultdicts into normal dicts. 
    Useful for pickling defaultdicts which have lambdas'''
    if not type(ddict) == defaultdict:
        return ddict
    ret = {}
    for k, v in ddict.items():
        ret[k] = ddictToDict(v)
    return ret

def dictToCSV(d, out):
    '''takes dict d, with the form {a:{b:c}} (where b is consistant across all a's)
    and writes it to a csv formatted file with path out'''
    topLine = ['']
    topLine += d[d.keys()[0]].keys() # The 'features' measured
    outLines = [",".join(map(str,topLine))]
    for group, ents in d.items():
        nextLine = [group]
        for k in topLine[1:]: # all 'featureSets'
            nextLine.append(ents[k])
        outLines.append(",".join(map(str,nextLine)))
    f = open(out, 'w')
    f.write("\n".join(outLines))
    f.close()
    
def csvToDict(source):
    '''The reverse process as dictToCSV above
        orientation is taken that top level keys are on the left column'''
    s = loadFile(source)
    lines = s.split("\r")
    lines = mapAndFold(lambda x: x.split("\n"), lines) # inconsistant files!
    lines = map(lambda x: x.split(","), lines) # seperate into entries
    keys = lines[0][1:]
    ret = {}
    for line in lines[1:]:
        pairs = zip(keys, line[1:])
        ret[line[0]]=dict(pairs)
    return ret
    
################################################################################
################################# Time Keeping #################################
################################################################################

def nextDate((year, month, day)):
    import calendar
    cal = calendar.Calendar()
    print (year, month, day)
    if day < max(cal.itermonthdays(year, month)):
        return (year, month, day+1)
    if month < 12:
        return (year, month+1, 1)
    return (year+1, 1, 1)

class dateRange:
    def __init__(self):
        self.start = (999999,1,1) #This Year probably doesn't matter
        self.end = (-999999,1,1) #You probably don't care about stuff before then

    def update(self, date):
        self.start = min(self.start, date)
        self.end = max(self.end, date)

    def getRange(self):
        '''returns the integer number of days between the two dates'''
        factors = (365,30.4375,1)
        diffs = [factors[i]*(self.end[i]-self.start[i]) for i in range(3)]
        return int(sum(diffs))

    def __str__(self):
        return str((self.start, self.end))    
    
################################################################################
################################ Miscellaneous #################################
################################################################################    
    
def  bigramifyList(tokens):
    '''pairs successive elements of a list into tuples
    originally used for making bigrams out of unigrams'''
    bigrams = []
    for i in range(len(tokens) - 1):
        bigrams.append((tokens[i], tokens[i+1]))
    return bigrams

def stopList():
    '''return a list of common english words. It's a list I found somewhere plus a few additions of my own.'''
    return ['a', "a's", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually', 'after', 'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apart', 'appear', 'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask', 'asking', 'associated', 'at', 'available', 'away', 'awfully', 'b', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', 'c', "c'mon", "c's", 'came', 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', 'co', 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing', 'contains', 'corresponding', 'could', "couldn't", 'course', 'currently', 'd', 'definitely', 'described', 'despite', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', "don't", 'done', 'down', 'downwards', 'during', 'e', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially', 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly', 'example', 'except', 'f', 'far', 'few', 'fifth', 'first', 'five', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'h', 'had', "hadn't", 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', "he's", 'hello', 'help', 'hence', 'her', 'here', "here's", 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'hi', 'him', 'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', 'http', 'i', "i'd", "i'll", "i'm", "i've", 'ie', 'if', 'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate', 'indicated', 'indicates', 'inner', 'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it', "it'd", "it'll", "it's", 'its', 'itself', 'j', 'just', 'k', 'keep', 'keeps', 'kept', 'know', 'knows', 'known', 'l', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like', 'liked', 'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'm', 'mainly', 'many', 'may', 'maybe', 'me', 'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must', 'my', 'myself', 'n', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor', 'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'o', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own', 'p', 'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably', 'probably', 'provides', 'q', 'que', 'quite', 'qv', 'r', 'rather', 'rd', 're', 'really', 'reasonably', 'regarding', 'regardless', 'regards', 'relatively', 'respectively', 'right', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'serious', 'seriously', 'seven', 'several', 'shall', 'she', 'should', "shouldn't", 'since', 'six', 'so', 'some', 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying', 'still', 'sub', 'such', 'sup', 'sure', 't', "t's", 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that's", 'thats', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', "there's", 'thereafter', 'thereby', 'therefore', 'therein', 'theres', 'thereupon', 'these', 'they', "they'd", "they'll", "they're", "they've", 'think', 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used', 'useful', 'uses', 'using', 'usually', 'uucp', 'v', 'value', 'various', 'very', 'via', 'viz', 'vs', 'w', 'want', 'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll", "we're", "we've", 'welcome', 'well', 'went', 'were', "weren't", 'what', "what's", 'whatever', 'when', 'whence', 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', "who's", 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with', 'within', 'without', "won't", 'wonder', 'would', 'would', "wouldn't", 'x', 'y', 'yes', 'yet', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'z', 'zero']