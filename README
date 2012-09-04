Corpora Analysis Toolkit (CAT) 

Readme. Do it.

These are the key scripts to do language modle analysis and corpora comparison as done by me (Eli Omernick) in the summer of 2012 at Pomona College. If you have any comments, questions, critisism, praise, or abuse feel free to contact me at e.omernick@gmail.com. 

I did not write all of this code. I wrote about half of it. The rest I gathered from around the web, and I think I've creditted everyone who is responsible for writting it. 

This was developed in Python 2.7. I do not know why it would not work in other versions of Python. I've run it on Python 2.5. No gaurentees are made on other versions. 

Also, I like CamelCase. I realize that this is not considered proper Python "Style." It is, however, my style.

***************************************************************************
***************************************************************************

Contents:

1. Required Modules
2. Features and how to use them
	a. Readability 
	b. Inverse Vocabulary Density (IVD)
	c. Vocabulary Overlap (VO)
	d. Expected Frequency Discrepency (EFD)
	e. Salient Features
    f. A Few Additional Notes
3. A Note on LIWC
4. Aknowledgements


***************************************************************************
***************************************************************************

1. Required Modules

These functions rely on a number of python packages which are not standard with installations of Python 2.x. They include:

nltk (for readability tests) (Special Sylables files included)
	You also need the punkt tokenizer modules, which you can get by navigating the GUI spawned by nltk.download()

The included textanalyzer and readability tests have been hard coded for english by a minor modification on my part which allowed me to exclude other files. The interfacing remains the same, so if one desired they could get the original files from here:

http://code.google.com/p/nltk/source/browse/trunk#trunk%2Fnltk_contrib%2Fnltk_contrib%2Freadability

And use the tool with other languages. 

***************************************************************************
***************************************************************************

2. Features 

============================================================
	a. Readability 
============================================================

There are eight different scores for readability/reading ease included in the readability tests file. They are all based on simple algebraic formulae involving some combination of words/sentance, characters/word, sylables/word, and complex words (words with more than 2 syllables)/sentance. You can read about them on wikipedia: http://en.wikipedia.org/wiki/Readability_test. 

To get results include readabilitytests.py and make the following method calls:

rt = ReadabilityTool(text)

results = rt.getReportAll()

results will be a dictionary from the test name to the result score. Just iterate through and print it out. An example is in demo.py. Individual tests can also be run. Consult source code for their method names (you could probably guess them).

============================================================
	b. Inverse Vocabulary Density (IVD)
============================================================

IVD is the proportion of the total features which are unique (e.g. Number of different words used in a text / total words). It is specific to a particular corpora. 

To get this value first make a CorporaAnalyser (passing it the parsed dict of {corpus: {featureSet: {feature: frequency}}}. Then call IVD() to get a dict of {corpus: IVD}. For example see demo.py:

============================================================
	c. Vocabulary Overlap (VO)
============================================================

Vocab Overlap is a pair-wise comparison. It returns the proportion of the shared featurespace which is present in both corpora being compared (e.g. The number of different words which appear in both corpora divided by the number of different words which appear in either corpus). 

It is supported by the VO and VOSummary methods in CorporaAnalyzer. demo.py contains an example. 

============================================================
	d. Expected Frequency Discrepancy (EFD)
============================================================

EFD is also a pairwise metric. The fundamental idea behind EFD is to check the observed/expected ratios for each feature in each corpus, then to take the differences in those features to create a distribution of the discrepancies between the two corpora. The standard deviation of this distribution give a good sense for the dominance of salient features. 

To test for Statistical significance one can do a Chi-squared test with the resulting distribution with the null modle as either an EFD distribution of randomly split values across the corpora being compared (randomly assign them to groups instead of by whatever they're classified as). An alternative null modle can be generated by doing self similarity EFD (split each category into two and do the analysis on those groups). This process has not been totally refined, and will be adressed in later revisions.

This function can be evoked in a manner similar to VO, ehere the EFDSummary method returns a dictionary of pairs of values to the StDev and Mean of the resulting distribution and the EFD method returns the result between two parameter pairs.

There is no way at this time to retrieve the actual distribution, save by hacking through the salient features function described below. This won't take much effort to change however, so I'll hopefully get that done as soon as I figure out a reasonable way to interface it.

============================================================
	e. Salient Features
============================================================

Salient features are those which have the largest individual EFD values. For multiple corpora calls to this function it returns the features with the highest average salience. 

Returned words are words which differentiate the corpora in question. Negative values indicate that presence is negatively correlated with the group. For pairwise comparisons the first item in the pair (the one alphabetically first) is the key for this distinction. 

A method call to salient features looks like:

salientFeatures(self, numFeatures = 20, corpora = None, featureSets = None):

all parameters are optional, corpora and featureSets indicate the subsets of their respective groups to be included in the analysis (default all). numFeatures is the number of features to return (default 20).

The return type is a dict of the form: {corpus: {featureSet: set([(feature, efdAverage)])}}

============================================================
    f. Additional Notes 
============================================================

The SummarryToCSV method writes all of these analysis out to csv files in the provided path. It's the fastest way to apply a complete analysis to the data if you're willing to just sift through the results later.

The smooth parameter when creating the CorporaAnalyser is for calculating the observed/expected value. It is added to both of those quantities. A goof threashold for determining actually salient features is then (1+smooth)/smooth which will be the approximate result if a feature appears once in a corpus and no where else in the data. 


***************************************************************************
***************************************************************************

3. LIWC

If you're doing corpora comparisons for whatever reason you may want to consider LIWC. LIWC is a standalone program. It is a dictionary of words divided into "Psychologically significant" categories which gives breakdowns for the proportions of words in a text sample which are in each of those categories. 

It is installed on the CS Lab machine 227-12 at Pomona College as of August 2012, if you happen to be there.

It can also be aquired here:

http://www.liwc.net/


***************************************************************************
***************************************************************************

4. Aknowledgments

Stemmer.py was written by Vivake Gupta. The included version was last modified in 2008.

readabilitytest.py (along with textanalyzer.py) is an extension of NLTK, originally developed by Thomas Jakobsen and Thomas Skardal from University of Agder. It was added to NLTK Dec. 2007.

I made extremely minor modifications to these files to facilitate more general functionality. I've noted my changes in the included files. 

