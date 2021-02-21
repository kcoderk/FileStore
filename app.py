from flask import Flask, jsonify, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__, static_folder='app')
base_path = os.path.dirname(__file__)  # 当前文件所在路径
file_path = os.path.join(base_path, "files/")


@app.route("/")
def index():
    return jsonify({"status": "file not found"})


@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        try:
            f = request.files['filename']
            if not os.path.exists(file_path):
                os.mkdir(file_path)
            upload_path = os.path.join(file_path, secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会报错
            if os.path.exists(file_path):
                return jsonify({"status": "filename already exists"})
            else:
                f.save(upload_path)
            return jsonify({"status": "success", 'filename': secure_filename(f.filename)})
        except Exception as e:
            print('error', e)
    if request.method == "GET":
        return render_template("index.html")
    return jsonify({"status": "failed"})


@app.route("/list", methods=['GET'])
def list_file():
    path_list = os.listdir(file_path)
    return jsonify({"filenames": path_list})

# @app.route('/', defaults={'path': ''})
@app.route('/<path:filename>')
def get_file(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join(file_path, filename)):
            return send_from_directory(file_path, filename, as_attachment=True)
    return jsonify({"status": "file not found"})


if __name__ == '__main__':
    app.run()
