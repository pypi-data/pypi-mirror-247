'''
@author: M. Bernt
'''

from sys import stdout


def gffwriter(featurelist, acc, size, outfile=None, mode="w"):
    """
    write the gff string for each feature
    @param[in] featurelist a list of features to be written
    @param[in] acc string to be prepended to each line (e.g. accession)
    @param[in] outfile file to write into, if None: write to stdout
    @param[in] mode file write mode, e.g. a, w, ...
    """

    featurelist.sort(key=lambda x: x.start)

    if isinstance(outfile, str):
        file = open(outfile, mode)
        for feat in featurelist:
            file.write("%s\n" % feat.gffstr(acc, size))
        file.close()
    elif outfile is None:
        for feat in featurelist:
            stdout.write("%s\n" % feat.gffstr(acc, size))
    else:
        for feat in featurelist:
            outfile.write("%s\n" % feat.gffstr(acc, size))
