import json
import os
from flask import Flask, flash,render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename


#importation des modules définis


import importlib.util



loader_spec = importlib.util.spec_from_file_location("loader", "../loader.py")
loader_module = importlib.util.module_from_spec(loader_spec)
loader_spec.loader.exec_module(loader_module)


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['xlsx', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "toto"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/")
def main():
    return render_template('index.html')




@app.route('/excel_upload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(url_for('rapport_fichier',
                                    filename=filename))


@app.route('/rapport_fichier')
def rapport_fichier():

    filename = request.args.get('filename')

    in_memory_file = loader_module.load_excel_file("./uploads/"+filename)

    rapport = loader_module.get_excel_headers(in_memory_file)

    return render_template("rapport.html", rapport =  rapport )

if __name__ == "__main__":
    app.run(debug=True)




