import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    image_folder = os.path.join(app.static_folder, 'images')
    image_files = get_recent_images(image_folder, 3)
    return render_template('index.html', image_files=image_files)

@app.route('/images/<path:filename>')
def serve_image(filename):
    image_folder = os.path.join(app.static_folder, 'images')
    return send_from_directory(image_folder, filename)

def get_recent_images(folder, num_images):
    files = os.listdir(folder)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
    print(files[:num_images])
    return [f"images/{x}" for x in files[:num_images]]

if __name__ == '__main__':
    app.run()

