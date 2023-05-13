# Imports Libray
import os
import pathlib
import pandas as pd 
from flask import Flask, render_template, request, redirect, send_from_directory, url_for,make_response
import tkinter
from tkinter import messagebox
root = tkinter.Tk()
root.withdraw()

app = Flask(__name__)

UPLOAD_FOLDER = 'data'
if not os.path.exists(UPLOAD_FOLDER):
     os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER


path = "data/"


lis=os.listdir(path)
def check_file_indir(filename):
    if filename not in lis:
        return False
    else:
        return True
        


allowed_extensions = ['.csv','.xlsx']
def check_file_extension(filename):
    file_extension = pathlib.Path(filename).suffix
    if file_extension in allowed_extensions:
        return True
    else:
        return False
    


@app.route('/')
def home():
    return render_template('upload.html')



@app.route("/", methods=['POST'])
def uploadFiles():
    uploaded_file = request.files['file']
    if check_file_extension(uploaded_file.filename) == False:
        return make_response({"message":"File is not in proper format"},201)
    elif check_file_indir(uploaded_file.filename) ==False:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        print(make_response({"message":"File Uploaded Sucessfully"},201))
        return redirect(url_for('home'))
    else:
        return(make_response({"message":"File already Exits"},201))
    


@app.route('/login') 
def run(): 
 	return render_template('index.html')

 
@app.route("/view",methods=["POST","GET"])
def view_files():
    list1=[]
    for filename in os.listdir(path):
        paths=os.path.join(path,filename)
        if os.path.isfile(paths):
            list1.append(filename)
    return render_template("list.html", result=list1)
    

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename,as_attachment=True)
 
 
@app.route("/delete/<filename>")
def delete_files(filename):
    os.remove(path +"/" + filename)
    return redirect(url_for("view_files"))

@app.route("/views/<filename>")
def csvtohtml(filename):
    file_extension = pathlib.Path(filename).suffix
    print(file_extension)
    if file_extension == '.csv':
        print(path + filename)
        df = pd.read_csv(path + filename)
        return render_template('table.html', tables=[df.to_html()], titles=[''])
    else:
        print(path+ filename)
        df = pd.read_excel(path + filename)
        return render_template('table.html', tables=[df.to_html()], titles=[''])


if (__name__ == "__main__"):
    app.debug = True
    app.run()