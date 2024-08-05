# -*- encoding: utf-8 -*-
"""

"""
import pandas as pd
from apps.home import blueprint
from flask import Flask,render_template, request,redirect, url_for, flash,current_app
from flask_login import login_required
from jinja2 import TemplateNotFound
import os
import openpyxl
from apps.home import kebutuhan_1
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
app.config["DEBUG"] = True

# Folder where uploaded files will be stored
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
# Ensure the upload folder exists


@blueprint.route('/index')
@login_required
def index():
    filepaths = {
        'kebutuhan_1': os.path.join(app.config['UPLOAD_FOLDER'], 'kebutuhan_1.xlsx'),
        'kebutuhan_2': os.path.join(app.config['UPLOAD_FOLDER'], 'kebutuhan_2.xlsx'),
        'kebutuhan_3': os.path.join(app.config['UPLOAD_FOLDER'], 'kebutuhan_3.xlsx'),
        'kebutuhan_4': os.path.join(app.config['UPLOAD_FOLDER'], 'kebutuhan_4.xlsx')
    }
    
    file_tables = {}
    
    for name, path in filepaths.items():
        if os.path.exists(path):
            df = pd.read_excel(path, engine='openpyxl')
            file_tables[name] = df.to_html()
    return render_template('home/index.html', segment='index',file_tables=file_tables)



@blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Read and convert file to HTML table
            try:
                df = pd.read_excel(filepath, engine='openpyxl')
                table_html = df.to_html(classes='table table-bordered table-striped', index=False)
            except Exception as e:
                flash(f"Error reading Excel file: {e}")
                return redirect(request.url)

            # Render specific templates based on filename
            if filename == 'kebutuhan_1.xlsx':
     
                return render_template('home/kebutuhan_1.html', table_html=table_html, name=filename)
            elif filename == 'kebutuhan_2.xlsx':
                return render_template('home/kebutuhan_2.html', table_html=table_html, name=filename)
            elif filename == 'kebutuhan_3.xlsx':
                return render_template('home/kebutuhan_3.html', table_html=table_html, name=filename)
            elif filename == 'kebutuhan_4.xlsx':
                return render_template('home/kebutuhan_4.html', table_html=table_html, name=filename)
            else:
                
                return redirect(request.url)

    return render_template('home/upload.html')


@blueprint.route('/kebutuhan_1')
@login_required
def kebutuhan_1():
    """Route to display the contents of 'kebutuhan_1.xlsx' in a table."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'kebutuhan_1.xlsx')

    if os.path.exists(filepath):
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
            table_html = df.to_html(classes='table table-bordered table-striped', index=False)
            return render_template('home/kebutuhan_1.html', table_html=table_html, name='kebutuhan_1.xlsx')
        except Exception as e:
            flash(f"Error reading Excel file: {e}")
            return redirect(url_for('home.index'))
    else:
        flash('The file kebutuhan_1.xlsx does not exist.')
        return redirect(url_for('home.index')) # Redirect to index or any other page

@blueprint.route('/kebutuhan_2')
@login_required
def kebutuhan_2():
    """Route to display the contents of 'kebutuhan_2.xlsx' in a table."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'kebutuhan_2.xlsx')

    if os.path.exists(filepath):
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
            table_html = df.to_html(classes='table table-bordered table-striped', index=False)
            return render_template('home/kebutuhan_2.html', table_html=table_html, name='kebutuhan_2.xlsx')
        except Exception as e:
            flash(f"Error reading Excel file: {e}")
            return redirect(url_for('home.index'))
    else:
        flash('The file kebutuhan_2.xlsx does not exist.')
        return redirect(url_for('home.index')) # Redirect to index or any other page

@blueprint.route('/kebutuhan_3')
@login_required
def kebutuhan_3():
    """Route to display the contents of 'kebutuhan_3.xlsx' in a table."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'kebutuhan_4.xlsx')

    if os.path.exists(filepath):
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
            table_html = df.to_html(classes='table table-bordered table-striped', index=False)
            return render_template('home/kebutuhan_3.html', table_html=table_html, name='kebutuhan_3.xlsx')
        except Exception as e:
            flash(f"Error reading Excel file: {e}")
            return redirect(url_for('home.index'))
    else:
        flash('The file kebutuhan_3xlsx does not exist.')
        return redirect(url_for('home.index')) # Redirect to index or any other pag
    

@blueprint.route('/kebutuhan_4')
@login_required
def kebutuhan_4():
    """Route to display the contents of 'kebutuhan_4.xlsx' in a table."""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'kebutuhan_4.xlsx')

    if os.path.exists(filepath):
        try:
            df = pd.read_excel(filepath, engine='openpyxl')
            table_html = df.to_html(classes='table table-bordered table-striped', index=False)
            return render_template('home/kebutuhan_4.html', table_html=table_html, name='kebutuhan_4.xlsx')
        except Exception as e:
            flash(f"Error reading Excel file: {e}")
            return redirect(url_for('home.index'))
    else:
        flash('The file kebutuhan_4.xlsx does not exist.')
        return redirect(url_for('home.index')) # Redirect to index or any other page
    
@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


    
if __name__ == '__main__':
    blueprint.run(debug=True)
# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None