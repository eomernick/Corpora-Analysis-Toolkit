## Interface to the functionality of everything
## Eli Omernick
## 5-31-2012

from corporaAnalyzer import *
from readabilitytests import ReadabilityTool

if __name__ == '__main__':
    
    ## T.S. Elliot - The Naming of Cats
    t0 = "The Naming of Cats is a difficult matter, It isn't just one of your holiday games; You may think at first I'm as mad as a hatter When I tell you, a cat must have THREE DIFFERENT NAMES. First of all, there's the name that the family use daily, Such as Peter, Augustus, Alonzo or James, Such as Victor or Jonathan, or George or Bill Bailey - All of them sensible everyday names. There are fancier names if you think they sound sweeter, Some for the gentlemen, some for the dames: Such as Plato, Admetus, Electra, Demeter - But all of them sensible everyday names. But I tell you, a cat needs a name that's particular, A name that's peculiar, and more dignified, Else how can he keep up his tail perpendicular, Or spread out his whiskers, or cherish his pride? Of names of this kind, I can give you a quorum, Such as Munkustrap, Quaxo, or Coricopat, Such as Bombalurina, or else Jellylorum - Names that never belong to more than one cat. But above and beyond there's still one name left over, And that is the name that you never will guess; The name that no human research can discover - But THE CAT HIMSELF KNOWS, and will never confess. When you notice a cat in profound meditation, The reason, I tell you, is always the same: His mind is engaged in a rapt contemplation Of the thought, of the thought, of the thought of his name: His ineffable effable Effanineffable Deep and inscrutable singular Name."
    
    ## Eli Omernick - A Breif Reflection (With Cats)
    t1 = "I am not a cat. Were I a cat then I suspect I would not have typed out these words. These words are far too ordinary for a cat to bother with. I am currently in the company of three cats, and none of them seem the least bit interested in what I'm doing; I cite this as evidence. They seem quite content to lounge about and accept their occasional tributes of food water and attention without dirtying themselves with the sort of mundane task of typing example prose for a dull old computer program: perhaps if it were a more profound matter, such as dangling string or moving red dots. I may not be as dignified, but whose name fosters results on Google?"
    
    ## William Shakespeare - Sonnet 18
    t2 = "Shall I compare thee to a summer's day? Thou art more lovely and more temperate: Rough winds do shake the darling buds of May, And summer's lease hath all too short a date: Sometime too hot the eye of heaven shines, And often is his gold complexion dimm'd; very fair from fair sometime declines, By chance or nature's changing course untrimm'd; But thy eternal summer shall not fade Nor lose possession of that fair thou owest; Nor shall Death brag thou wander'st in his shade, When in eternal lines to time thou growest: So long as men can breathe or eyes can see, So long lives this and this gives life to thee. "
    
    corpora = {"T.S.Elliot": t0, "CatMan": t1, "Shakespeare": t2}
    ## Readability tests:
    print "*"*80
    print "Readability Tests"
    print "*"*80
    for c, text in corpora.items():
        rt = ReadabilityTool(text)
        results = rt.getReportAll()
        print c
        for test, val in results.items():
            print "\t{0}: {1}".format(test, val)
            
    ## Comparison Metrics
    corpora = parsePlainText(corpora)
    
    ## Demonstration of Actual interface with CorporaAnalyzer
    
    ca = CorporaAnalyzer(corpora)
    
    ivdVals = ca.IVD()
    print "*"*80
    print "Inverse Vocab Density"
    print "*"*80
    for corpus, featureSets in ivdVals.items():
        print corpus
        for featureSet,  score in featureSets.items():
            print "\t{0}\n\t\t{1}".format(featureSet, score)
    
    voVals = ca.VOSummary()
    pairs = voVals.keys()
    print "*"*80
    print "Vocab Overlaps"
    print "*"*80
    for (f,s), featureSets in voVals.items():
        print "{0} vs. {1}:".format(f,s)
        for featureSet, score in featureSets.items():
            print "\t{0}\n\t\t{1}".format(featureSet, score)
    ## Individual VO scores can be retrieved using the VO method, similar 
    ## to the EFD method used below 
            
    print "*"*80
    print "Expected Frequency Discrepancy"
    print "*"*80
    for (f,s) in pairs:
        print "{0} vs. {1}:".format(f,s)
        for fSet, score in ca.EFD(f,s).items():
            print "\t{0}\n\t\t{1}".format(fSet, score)
    ## The EFDSummary method can be used to return a dictionary of all results, similar to the VOSummary method above

    print "*"*80
    print "Salient Features"
    print "*"*80
    sf = ca.salientFeatures(numFeatures=5)
    print "="*50
    print "All Corpora:"
    print "="*50
    for corpus, featureSets in sf.items():
        print corpus
        for featureSet, words in featureSets.items():
            words = map(lambda (x,y): "{0}: {1}".format(formatTuple(x),formatFloat(y)), words)
            print "\t{0}\n\t\t{1}".format(featureSet, list(words))
    print "="*50    
    print "Pairwise"
    print "="*50
    for pair in pairs:
        sf = ca.salientFeatures(numFeatures=5, corpora=pair)
        print "{0} vs. {1}:".format(pair[0],pair[1])
        featureSets = sf[sf.keys()[0]]# They'll be the same
        for featureSet, words in featureSets.items():
            words = map(lambda (x,y): "{0}: {1}".format(formatTuple(x),formatFloat(y)), words)
            print "\t{0}\n\t\t{1}".format(featureSet, list(words))

    ## Salient Features won't be interesting because the corpora being compared are so small and have small vocab overlaps. The highest rated features will all be words which appear in one group but not the others


    ## This summaryToCSV method saves all of the above displayed info into easily readable/parsable CSV files
    summaryToCSV(corpora, "./demoResults/")
        