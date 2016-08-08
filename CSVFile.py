import csv
from csvvalidator import *
import pandas as pd
import os
import md5
import hashlib
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import File, Spreadsheet, Base

engine = create_engine('mysql+pymysql://root:root@localhost:3306/mydb', echo=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


ALLOWED_EXTENSIONS = set(['csv'])


class CSVFile:
    'Common base for csv management'

    __field_names = ('date', 'category', 'employee name', 'employee address', 'expense description', 'pre-tax amount', 'tax name', 'tax amount' )
    __df = None
    __filename = None
    __hashval = None
    __maxfilesize = 16 * 1024 * 1024 #16 megabytes 
    __errorlist = []
    __error = \
    {
        "OVERSIZE_FILE": "The file is beyond I gigabytes.",
        "DUPLICATE_FILE": "The file already exist ",
        "NOT_CSV": "The file is not in csv format."
    }

    def __init__(self, filename ):
        '''
            Constructor
        '''
        self.__df = pd.read_csv(filename)
        self.__filename = filename
        self.__hashval = self.md5sum()
   
    def isValid(self):
        '''
            validate the CSV file
        '''

        if self.__isDuplicate () or self.__isTooBig( ) or not self.__allowed_file( ):
            return False


        subset = self.__df[list(self.__field_names)]
        tuples = [tuple(x) for x in subset.values]
        tuples = [self.__field_names] + tuples 
        #print tuple (self.__df.values.tolist())
        data = tuple (tuples )

        validator = CSVValidator(self.__field_names)

        validator.add_value_check('date', datetime_string('%m/%d/%Y'))

        validator.add_value_check('pre-tax amount', float)
        validator.add_value_check('tax amount', float)

        categories = ('Travel', 'Meals and Entertainment', 'Computer - Hardware', 'Computer - Software', 'Office Supplies')
        validator.add_value_check('category', enumeration(categories))


        problems = validator.validate(data)
        return len(problems) == 2


    def __allowed_file(self):
        '''
            allowed file type
        '''
        return '.' in self.__filename and \
               self.__filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


    def md5sum(self):
        '''
            hash the file to a unique string
        '''
        md5 = hashlib.md5()
        with open(self.__filename, 'rb') as f:
            for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
                md5.update(chunk)
        return md5.hexdigest()


    def dataInJson(self):
        '''
            data in json format
        '''
        return self.__df.to_json()


    def __saveRowToFileTable(self):
        '''
            save data to file table
        '''
        file_record = File(name=self.__filename, hash=self.__hashval)
        session.add(file_record)
        session.commit()

    def __saveRowToSpreadSheetTable(self, date, category, employee_name, employee_address, expense_description, pre_tax_amount, tax_name, tax_amount):
        '''
            save a row to spreadsheet table
        '''
        spread_record = Spreadsheet(date = date,
            category = category,
            employee_name = employee_name,
            employee_address = employee_address,
            expense_description = expense_description,
            pre_tax_amount = pre_tax_amount,
            tax_name = tax_name,
            tax_amount = tax_amount,
            name = self.__filename
        )
        session.add(spread_record)
        session.commit()


    def __formatDate(self, vdate):
        '''
            format date
        '''
        return datetime.strptime(vdate, '%m/%d/%Y')


    def __formatCurrency(self, value):
        '''
            format currency
        '''
        cval = str (value).replace(',','')
        cval = float( cval.replace('.',''))
        return cval


    def __saveToSpreadSheet(self):
        '''
            save all rows to spreadsheet table
        '''
        for i,r in self.__df.iterrows():
            vdate = self.__formatDate(r['date'])
            pretax = self.__formatCurrency(r['pre-tax amount'])

            curtax = self.__formatCurrency(r['tax amount'])

            self.__saveRowToSpreadSheetTable (vdate,r['category'],r['employee name'],r['employee address'],r['expense description'], pretax ,r['tax name'], curtax )


    def save(self):
        '''
            Save to database
        '''
        if self.isValid( ):
            #save file to database
            self.__saveRowToFileTable()

            #save spreadsheet to database
            self.__saveToSpreadSheet()


    def __isDuplicate (self):
        '''
            identify duplicates
        '''
        numhashrecord = session.query(File).filter_by(hash=self.__hashval).count()
        numnamerecord = session.query(File).filter_by( name=self.__filename).count()
        return numhashrecord > 1 or numnamerecord > 1


    def getDataFrame (self):
        '''
            get dataframe
        '''
        return self.__df


    def getDataFrameByMonth (self):
        '''
            get dataframe by month
        '''
        col = list(self.__field_names)

        dateCol = col[0]
        preTaxCol = col[5]
        taxCol = col[-1]

        columnList = []

        columnList.extend([dateCol, taxCol])
        curFrame = self.__df[columnList]

        curFrame[dateCol] = pd.to_datetime(self.__df[dateCol])

        per = curFrame.date.dt.to_period("M")
        g = curFrame.groupby(per)
        return g.sum()
        



    def __isTooBig (self):
        '''
            get dataframe
        '''
        return os.path.getsize( self.__filename ) > self.__maxfilesize

    def errors (self):
        '''
            get all error messages
        '''

        if not self.__allowed_file( ) :
            mflag = "NOT_CSV"
            message = self.__error[mflag]
            self.__errorlist.append (message)

        if self.__isTooBig( ):
            mflag = "OVERSIZE_FILE"
            message = self.__error[mflag]
            self.__errorlist.append (message)

        if self.__isDuplicate ():
            dupObject = session.query(File).filter_by(hash=self.__hashval).first() 
            mflag = "DUPLICATE_FILE"

            spMsg = "with name: " + dupObject.name
            message = self.__error[mflag] + spMsg
            self.__errorlist.append (message)

        return " <br/> ".join (self.__errorlist)


