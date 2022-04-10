# Comparing Feather Again GZIP Compress CSV files reading/writing

After comparing .feather files against .csv.gz, I have found that feather files are significantly faster at reading and writing than gzip compressed .csv files.

Here are some results after comparing them.

For feather files, reading and writing a dataframe of single column random numbers:
####
<img src='assets/feather.png'>


####

For gzip csv files, reading and writing the same inputs:
####
<img src='assets/csvgz.png'>

####

Comparison on a log plot (base 2):
####
<img src='assets/comparison.png'>

