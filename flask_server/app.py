import json
import os
from flask import Flask, flash,render_template, request, redirect, url_for, session,jsonify
from werkzeug.utils import secure_filename

#importation des modules définis

import importlib.util

loader_spec = importlib.util.spec_from_file_location("loader", "../loader.py")
loader_module = importlib.util.module_from_spec(loader_spec)
loader_spec.loader.exec_module(loader_module)

convert_spec = importlib.util.spec_from_file_location("convert", "../convert.py")
convert_module = importlib.util.module_from_spec(convert_spec)
convert_spec.loader.exec_module(convert_module)

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['xlsx', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.json_encoder = convert_module.my_encoder
in_memory_excel_file = None
file_structure_dictionary = None

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

            return redirect(url_for('rapport_fichier', filename=filename))

@app.route('/rapport_fichier')
def rapport_fichier():

    global in_memory_excel_file

    global file_structure_dictionary

    filename = request.args.get('filename')

    in_memory_excel_file = loader_module.load_excel_file("./uploads/"+filename)

    file_structure_dictionary = loader_module.get_excel_headers(in_memory_excel_file)

    return render_template("rapport.html", file=filename ,rapport=file_structure_dictionary )

@app.route('/parse_excel',methods = ['GET', 'POST'])
def parse_excel():

    global in_memory_excel_file

    global file_structure_dictionary

    if request.method == 'POST':

        filtre = {}
        types_dict = {}

        for sheet in file_structure_dictionary:
            filtre[sheet] = []
            types_dict[sheet] = {}
            for column in file_structure_dictionary[sheet]:

                if not sheet+column+"chosen" in request.form:
                    filtre[sheet].append(column)
                else:
                    #types_dict est du format sheet => list[  (column_name, convertion_parameters)  ]

                    column_type = request.form[sheet+column+"type"]
                    column_behaviour = request.form[sheet+column+"politique"]
                    column_default_value = request.form[sheet+column+"default-value"]
                    
                    if column_type == "int":
                        column_default = int(column_default)
                    elif column_type == "float":
                        column_default = float(column_default)

                    #convertion_element = convert_module.conversion_parameters(column_type, column_politique, column_default)
                    types_dict[sheet][column] = {
                        "type": column_type,
                        "behaviour": column_behaviour,
                        "default_value": column_default_value
                    }
        
        processedDF = loader_module.processFile("./uploads/"+request.form["file"], types_dict)
        tables=[]
        for df in processedDF:
            tables.append((df, processedDF[df].head().to_html()))
        #return jsonify({"filtre" : filtre , "types_dict" : processedDF})
        return render_template("process.html", dictDF=tables)

        # créer le types dict
    return None

if __name__ == "__main__":
    app.run(debug=True)