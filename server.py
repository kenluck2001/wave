from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug import secure_filename
import os
import datetime
import collections
from CSVFile import CSVFile

app = Flask(__name__)
app.secret_key = '%/8erjghdsdsggdfk546dfg!!|ghfgjut'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

UPLOAD_FOLDER = os.getcwd() + '/upload/'

ALLOWED_EXTENSIONS = set(['csv'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

	
@app.route('/index')
def show_every_tables():
    total = []
    listOfData = []

    listOfFiles = [ os.path.join(app.config['UPLOAD_FOLDER'], x) for x in os.listdir(UPLOAD_FOLDER) if x and x[0]!="." and x[-1]!="~"] 

    listOfFilesWithDateDict =  { os.path.getmtime(filename): filename for filename in listOfFiles }

    orderedlistOfFilesWithDateDict = collections.OrderedDict(sorted(listOfFilesWithDateDict.items()))

    orderedlistOfFiles = orderedlistOfFilesWithDateDict.values() #get only the filenames in the right order

    
    for fullpath in orderedlistOfFiles[::-1]:
        csvObj = CSVFile(fullpath)
        #split fullname to normal file name
        currentFileArr = fullpath.split ("/")
        currentFile = currentFileArr[-1]
        currentRow = currentFile, csvObj.getDataFrame(), csvObj.getDataFrameByMonth ()
        total.append (currentRow )

    emsg = "Files are successfully fetched"
    etype = "success"

    flash(emsg, etype)

    return render_template("index.html", total = total, isfull = len(orderedlistOfFiles) > 0 )



@app.route('/show/<filename>')
def show_csv(filename):
    fileWithPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    csvObj = CSVFile(fileWithPath)
    return render_template("showtable.html" )



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():

    def __allowed_file(filename):
        '''
            allowed file type
        '''
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    emsg = None
    if request.method == 'POST':
        fileObj = request.files['file']

        if fileObj and __allowed_file(fileObj.filename):
            filename = secure_filename(fileObj.filename)
            fileWithPath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            fileObj.save(fileWithPath)

            csvObj = CSVFile(fileWithPath) 
            csvObj.save() #save to database

            if not csvObj.isValid(): 
                emsg = "The current file uploaded failed. "  + csvObj.errors ()

            return redirect(url_for('show_every_tables'))

        etype = "error"
        emsg = "File is not compatible. Check file type and size"
        flash(emsg, etype)
        return redirect(url_for('show_every_tables'))

    
    etype = "error"
    flash(emsg, etype)
    return redirect(url_for('show_every_tables'))
	

if __name__ == '__main__':
   app.run(debug = True)
