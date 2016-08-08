from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class File(Base):
    '''
        model class for the files
    '''
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column( String(255) )
    hash = Column( String(255) )

    def __repr__(self):
        return "<File(id='%s', name='%s', hash='%s')>" % (
                             self.id, self.name, self.hash)


class Spreadsheet(Base):
    '''
        model class for saving and populating the spreadsheet
    '''
    __tablename__ = 'spreadsheets'

    id = Column(Integer, primary_key=True)
    #date = Column(Date) 
    date = Column(DateTime)
    category = Column(String(255))
    employee_name = Column(String(255))
    employee_address = Column(String(500))
    expense_description = Column(String(500))
    pre_tax_amount = Column(Float) 
    tax_name = Column(String(255))
    tax_amount = Column(Float) 
    name = Column(String(255)) #name of file

    def __repr__(self):
        return "<Spreadsheet(id='%s', date='%s', category='%s' employee_name='%s', employee_address='%s', expense_description='%s', pre-tax_amount='%.2f', tax_name='%s', tax_amount='%.2f')>" % (self.id, self.date, self.category, self.employee_name, self.employee_address, self.expense_description, self.pre_tax_amount, self.tax_name , self.tax_amount)


