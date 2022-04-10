# Comparing Feather Against GZIP Compressed CSV files reading/writing

This is a very simple display on some results of the read/write times of feather and gzip compressed files for different file sizes. It is a "knock out some results in an hour" kind of report, rather than actually comparing the pros and cons of the two file types for different purposes, or under various conditions.

After comparing .feather files against .csv.gz, I have found that feather files are significantly faster at reading (by a factory about 10) and writing (by a factor of about 100) than gzip compressed .csv files for the test case.

Here are some results after comparing them.

For feather files, reading and writing a dataframe of single column random numbers:
####
<img src='assets/feather.png'>


####

For gzip csv files, reading and writing the same inputs:
####
<img src='assets/csvgz.png'>

####

Comparison on a log plot (base 10):
####
<img src='assets/comparison.png'>

####

As you can see, feather files read by approximately a factor of 10 better than the compressed csv files across the entire range of file sizes, and are about 100 times as fast in the writing case.
