import csv
from csvvalidator import *
import pandas as pd
import numpy as np
from CSVFile import CSVFile


ab = CSVFile ("data_example.csv")
print "Data is valid\n"
print ab.isValid()

print "Data is hashed\n"
print ab.md5sum()

print "Data in json\n"
print ab.dataInJson()

print "Data is saved\n"
print ab.save()

print "Dataframe is here\n"
print ab.getDataFrame ()

print "Data error\n"
print ab.errors ()

print "Second test \n\n\n"
ab = CSVFile ("globals.js")
print "Data is valid\n"
print ab.isValid()

print "Data is hashed\n"
print ab.md5sum()

print "Data in json\n"
print ab.dataInJson()

print "Data is saved\n"
print ab.save()

print "Dataframe is here\n"
print ab.getDataFrame ()

print "Data error\n"
print ab.errors ()

print "=======================================\n"

ab = CSVFile ("data_example.csv")
print "Data is valid\n"
print ab.getDataFrameByMonth()

