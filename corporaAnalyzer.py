## Python Code for comparing multiple feature sets
## Developed for use with text feature
## Useful for comparing any two (or more) corpora with identical feature Sets
## 
## For Use of Ease the SummaryToCSV method is included with an example of how to use it
## For questions feel free to contact me at e.omernick@gmail.com
##

## Eli Omernick
## June 2012


import itertools, random, codecs

from collections import defaultdict
from useful import *


################################################################################
################################ Analyzer Class ################################
################################################################################

class CorporaAnalyzer:

    def __init__(self, corporaDict, smooth = .5):
        '''Class to support the analysis and comparison of multiple corpora
            @param corporaDict a dict of the form: 
            {corpusName: {featureSetName: {feature: frequencyObserved}}}'''
        self.corporaDict = corporaDict
        self.features = defaultdict(set)
        self.featureTotals = defaultdict(lambda: defaultdict(int)) # Totals across all corpora
        self.featureTotalsPerCorpus = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self.featureSetTotals = defaultdict(int) # Size of each feature set
        self.featureSetTotalsPerCorpus = defaultdict(lambda: defaultdict(int)) 
        self.expectationDiff = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        # dict of Expected Frequency differences per pair of corpora (This is a bad name for it)
        self.EDTable = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        # StDev of above table to get the cute number
        self.EFDTable = defaultdict(lambda: defaultdict(float) )
        
        ## get totals of frequencies for expected value calculations
        for corpus, featureSets in self.corporaDict.items(): 
            for featureSet, features in featureSets.items():
                for feature, freq in features.items():
                    self.features[featureSet].add(feature)
                    self.featureSetTotals[featureSet] += freq
                    self.featureTotals[featureSet][feature] += freq
                    self.featureSetTotalsPerCorpus[featureSet][corpus] += freq
                    self.featureTotalsPerCorpus[featureSet][feature][corpus] += freq
        
        ## calculate (observed / expected) for each feature
        for featureSet, features in self.featureTotals.items():
            for feature in features:
                # average proportion
                eRatio = float(self.featureTotals[featureSet][feature]) / self.featureSetTotals[featureSet]
                for corpus in self.corporaDict:
                    # assume every feature occurs 
                    smooth = float(smooth) / self.featureSetTotalsPerCorpus[featureSet][corpus]
                    # expected number of occurences
                    eVal = (self.featureSetTotalsPerCorpus[featureSet][corpus] * eRatio) + smooth
                    oVal = self.featureTotalsPerCorpus[featureSet][feature][corpus] + smooth
                    self.expectationDiff[featureSet][feature][corpus] = oVal / eVal    

        ## Cross all corpora and populate self.EDTable
        ## We keep this around for the ability to decern salient features from it
        keys = self.corporaDict.keys()
        pairs = itertools.product(keys, keys)
        pairs = itertools.ifilter(lambda pair: pair[0] < pair[1], pairs)
        for pair in pairs:
            for featureSet, features in self.features.items():
                for feature in features:
                    v0 = self.expectationDiff[featureSet][feature][pair[0]]
                    v1 = self.expectationDiff[featureSet][feature][pair[1]]
                    self.EDTable[pair][featureSet][feature] = v0 - v1
        ## Get StDev from the Expected differences and compact it into The One Number'''
        for pair, featureSets in self.EDTable.items():
            for featureSet, features in featureSets.items():
                self.EFDTable[featureSet][pair] = stDev(self.EDTable[pair][featureSet].values())


################################################################################
############################## Retrieval Methods ###############################
################################################################################

                    
    def EFDSummary(self, corpora = None, featureSets = None):
        '''Returns the average and standard deviation across all pairs of corpora
        corpora and featureSets are optional parameters. If supplied then they will 
        be interpreted as lists of keys which the analysis will be limited to.
        returns a dict from corpus to featureset to the average and stdev of the EFD 
        vals generated comparing that corpus against the others.'''
        if not corpora:
            corpora = self.corporaDict.keys()
        if not featureSets: 
            featureSets = self.features.keys()
        pairs = itertools.product(corpora, corpora)
        pairs = itertools.ifilter(lambda pair: pair[0] < pair[1], pairs)
        EFDList = defaultdict(lambda:defaultdict(list))
        for pair in pairs:
            for featureSet in featureSets:
                EFDList[pair[0]][featureSet].append(self.EFDTable[featureSet][pair])
                EFDList[pair[1]][featureSet].append(self.EFDTable[featureSet][pair])
        ret = defaultdict(dict)
        for cat, featureSets in EFDList.items():
            for featureSet, lst in featureSets.items():
                ave = average(lst)
                stdev = stDev(lst)
                ret[cat][featureSet] = (ave, stdev)
        return ret
        
    def EFD(self, corpus0, corpus1):
        '''Returns the Expected Frequency Discrepency between the two given corpora
            @param the two copus keys to be compared
            @return a dict from featureset to the StDev of the EFD Distribution'''
        ret = {}
        pair = (corpus1, corpus0)
        if corpus0 < corpus1:
            pair = (corpus0, corpus1)
        for featureSet, pairs in self.EFDTable. items():
            ret[featureSet] = self.EFDTable[featureSet][pair]
        return ret            

    def salientFeatures(self, numFeatures = 20, corpora = None, featureSets = None):
        '''Returns a dict from Corpus to featureSet to salient fetures'''
        if not corpora:
            corpora = self.corporaDict.keys()
        if not featureSets: 
            featureSets = self.features.keys()
        featureSalience = defaultdict(lambda:defaultdict(lambda:defaultdict(list)))
        pairs = itertools.product(corpora, corpora)
        pairs = itertools.ifilter(lambda pair: pair[0] < pair[1], pairs)
        for pair in pairs:
            featureSets = self.EDTable[pair]
            for featureSet, features in featureSets.items():
                for feature, efd in features.items():
                    featureSalience[pair[0]][featureSet][feature].append(-efd)
                    featureSalience[pair[1]][featureSet][feature].append(efd)
        
        topFeatures = defaultdict(lambda:defaultdict(set))
        def addFeatureAve(s, (word, val)):
            s.add((word, val))
            if len(s) > numFeatures:
                s.remove(min(s, key = lambda x: abs(x[1])))
        ## Find the most consistantly volitile feature
        for corpus, featureSets in featureSalience.items():
            for featureSet, features in featureSets.items():
                for feature, salienceList in features.items():
                    addFeatureAve(topFeatures[corpus][featureSet], (feature,  average(salienceList))) 
        return topFeatures
    
    def IVD(self, corpora=None, featureSets = None):
        '''Returns the density of the of the feature distribution per featureSet'''
        densities = defaultdict(dict)
        if not corpora:
            corpora = self.corporaDict.keys()
        if not featureSets: 
            featureSets = self.features.keys()
        for corpus in corpora:
            for featureSet in featureSets:
                total = self.featureSetTotalsPerCorpus[featureSet][corpus]
                uniqueFeatures = len(self.corporaDict[corpus][featureSet].keys())
                densities[corpus][featureSet] = float(uniqueFeatures) / total
        return densities

    def VOSummary(self, corpora = None, featureSets = None):
        '''Returns the % of the vocabulary which occurs in both corpora'''
        if not corpora:
            corpora = self.corporaDict.keys()
        if not featureSets: 
            featureSets = self.features.keys()
        overlaps = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        for corpus in corpora:
            for featureSet in featureSets: 
                baseFeatures = set(self.corporaDict[corpus][featureSet].keys())
                for corpus2 in corpora:
                    if corpus < corpus2:
                        subFeatures = set(self.corporaDict[corpus2][featureSet].keys())
                        commonFeatures = subFeatures & baseFeatures
                        allFeatures = subFeatures | baseFeatures
                        olap = float(len(commonFeatures)) / len(allFeatures)
                        overlaps[(corpus,corpus2)][featureSet] = olap
        return overlaps
		
    def VO(self, pair, featureSets = None):
        '''returns the Vocab overlap of the pair of corpora in the given featuresets 
            (default all featuereSets)'''
        if not featureSets: 
            featureSets = self.features.keys()
        pair = sorted(pair)
        features0 = set(self.corporaDict[pair[0]][featureSet].keys())
        features1 = set(self.corporaDict[pair[1]][featureSet].keys())
        commonFeatures = features0 & features1
        allFeatures = features0 | features1
        olap = float(len(commonFeatures)) / len(allFeatures)
		

################################################################################
#################################### Misc. #####################################
################################################################################

def parsePlainText(groups):
    '''groups is a dict from corpus:list of files, file, or plain text returns the feature dict of unigrams and bigrams for all groups'''
    freqs = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for g, files in groups.items():
        if type(files) == list:
            for file in files:
                try:
                    sText = loadFile(file)
                except IOError:
                    sText = file
                unigrams = tokenize(sText)
                bigrams = bigramifyList(unigrams)
                for u in unigrams:
                    freqs[g]['unigrams'][u] += 1
                for b in bigrams:
                    freqs[g]['bigrams'][b] += 1
        else:
            sText = files
            try: 
                sText = loadFile(files)
            except IOError:
                pass
            unigrams = tokenize(sText)
            bigrams = bigramifyList(unigrams)
            for u in unigrams:
                freqs[g]['unigrams'][u] += 1
            for b in bigrams:
                freqs[g]['bigrams'][b] += 1
    return freqs

def summaryToCSV(corpora, output, smooth = .5, numFeatures = 20):
    '''Summarizes multiple corpora into the given output file
        @param corpora is of the form: {corpusName: {featureSetName: {feature: frequencyObserved}}}
        @param output should be the base file name for all outputs (no file extension)
        There is an example of a call below
        Outputs a summary file as well as pairwise comparisons for the applicable summerized values'''
    
    things = ["IVD ({0})","VO ({0})","EFD Average({0}), EFD StDev ({0})","Top Features ({0}){1}"]
    ## Things are all per feature set
    topLine = ["Corpus"]
    featureSets = set() # set of all the feature sets
    for corpus, fSets in corpora.items():
        newFsets = set(fSets.keys())
        featureSets |= newFsets
    featureSets = list(featureSets) ## maintain order
    for thing in things:
        for featureSet in featureSets:
            topLine.append(thing.format(featureSet, ","*(numFeatures-1)))
    analyzer = CorporaAnalyzer(corpora, smooth = smooth)
    outLines = [",".join(topLine)]
    efds = analyzer.EFDSummary()
    overlaps = analyzer.VOSummary()
    overlapsAveLists = defaultdict(lambda: defaultdict(list))
    overlapsAve = defaultdict(lambda: defaultdict(int))
    for (corpus1, corpus2), fSets in overlaps.items():
        for featureSet, olap in fSets.items():
            overlapsAveLists[corpus1][featureSet].append(olap)
            overlapsAveLists[corpus2][featureSet].append(olap)
    for corpus, fSets in overlapsAveLists.items():
        for featureSet, lst in fSets.items():
            overlapsAve[corpus][featureSet] = average(lst)
    salientFeatures = analyzer.salientFeatures(numFeatures = numFeatures)
    densities = analyzer.IVD()
    for corpus in corpora.keys():
        outBits = [corpus]
        for f in featureSets:
            outBits.append(densities[corpus][f])
        for f in featureSets:
            outBits.append(overlapsAve[corpus][f])
        for f in featureSets:
            outBits.append(efds[corpus][f][0])
            outBits.append(efds[corpus][f][1])
        for f in featureSets:
            for (s, u) in salientFeatures[corpus][f]:
                outBits.append(str(u).replace(",", " "))
        outLines.append(",".join(map(unicode, outBits)))
    outFile = codecs.open(output+"Summary.csv", encoding='utf-8', mode='w')
    outFile.write(u"\n".join(outLines))
    outFile.close()
    ## do pairwise grids
    grids = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    keys = corpora.keys()
    pairs = itertools.product(keys, keys)
    pairs = itertools.ifilter(lambda pair: pair[0] < pair[1], pairs)
    for pair in pairs:
        for featureSet, olap in overlaps[pair[0]][pair[1]].items():
            grids[featureSet+"Overlap"][pair[0]][pair[1]] = overlaps[pair[0]][pair[1]][featureSet]
            grids[featureSet+"EFD"][pair[0]][pair[1]] = analyzer.EFDTable[featureSet][pair]
    for grid, corpora in grids.items():
        sortedCorpora = sorted(corpora.keys(), key=lambda x: len(corpora[x].keys()), reverse = True)
        last = corpora[sortedCorpora[-1]].keys()
        sortedCorpora += last
        revSorted = [x for x in sortedCorpora]
        revSorted.reverse()
        topLine = [""] + revSorted[:-1]
        outLines = [",".join(topLine)]
        for corpus0 in sortedCorpora[:-1]:
            nextLine = [corpus0]
            for corpus1 in revSorted[:revSorted.index(corpus0)]:
                nextLine.append(corpora[corpus0][corpus1])
            outLines.append(",".join(map(str, nextLine)))
        outFile = codecs.open(output+grid+".csv", encoding='utf-8', mode="w")
        outFile.write("\n".join(outLines))
        outFile.close()


