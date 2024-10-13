import os
from flask import Flask, request, jsonify

class ImageGallery:
    def __init__(self, directory='images'):
        self.directory = directory
        if not os.path.exists(directory):
            os.makedirs(directory)

    def upload_image(self, image_path):
        if os.path.exists(image_path):
            image_name = os.path.basename(image_path)
            destination = os.path.join(self.directory, image_name)
            with open(image_path, 'rb') as src, open(destination, 'wb') as dst:
                dst.write(src.read())
            return f"Image '{image_name}' uploaded successfully."
        else:
            return f"Image '{image_path}' does not exist."

    def show_all_images(self):
        images = os.listdir(self.directory)
        if images:
            return images
        else:
            return "No images in gallery."

    def delete_image(self, image_name):
        image_path = os.path.join(self.directory, image_name)
        if os.path.exists(image_path):
            os.remove(image_path)
            return f"Image '{image_name}' deleted successfully."
        else:
            return f"Image '{image_name}' does not exist."

app = Flask(__name__)
gallery = ImageGallery()
@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            image_path = os.path.join(gallery.directory, image.filename)
            image.save(image_path)
            result = gallery.upload_image(image_path)
            return f'''
            <!doctype html>
            <html lang="en">
              <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
                <title>Upload Image</title>
                <meta http-equiv="refresh" content="2; url=/" />
                <style>
                    body {{
                        background-color: purple;
                        color: white;
                        text-align: center;
                        font-family: Arial, sans-serif;
                    }}
                    .dancing-character {{
                        font-size: 50px;
                        animation: dance 1s infinite;
                    }}
                    @keyframes dance {{
                        0% {{ transform: translateY(0); }}
                        50% {{ transform: translateY(-20px); }}
                        100% {{ transform: translateY(0); }}
                    }}
                    .container {{
                        margin-top: 50px;
                    }}
                    .message {{
                        font-size: 24px;
                        margin-bottom: 20px;
                    }}
                </style>
              </head>
              <body>
                <div class="container">
                    <h1 class="message">{result}</h1>
                    <p class="dancing-character">💃</p>
                    <p>Redirecting to the gallery...</p>
                </div>
              </body>
            </html>
            '''
    return '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Upload Image</title>
        <style>
            body {{
                background-color: purple;
                color: white;
                text-align: center;
                font-family: Arial, sans-serif;
            }}
            .dancing-character {{
                font-size: 50px;
                animation: dance 1s infinite;
            }}
            @keyframes dance {{
                0% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-20px); }}
                100% {{ transform: translateY(0); }}
            }}
            .container {{
                margin-top: 50px;
            }}
            form {{
                display: inline-block;
                margin-top: 20px;
            }}
            input[type="file"] {{
                margin-bottom: 10px;
            }}
        </style>
      </head>
      <body>
        <div class="container">
            <h1>Upload Image</h1>
            <p class="dancing-character">💃</p>
            <form method="post" enctype="multipart/form-data">
              <input type="file" name="image"><br>
              <input type="submit" value="Upload">
            </form>
        </div>
      </body>
    </html>
    '''

@app.route('/')
def index():
    images = gallery.show_all_images()
    if isinstance(images, list):
        image_tags = ''.join([f'''
        <div style="display:inline-block; margin:10px;">
            <img src="/{gallery.directory}/{image}" alt="{image}" style="width:100px;height:100px;">
            <form method="post" action="/delete" style="display:inline;">
                <input type="hidden" name="image_name" value="{image}">
                <input type="submit" value="Delete">
            </form>
        </div>
        ''' for image in images])
        return f'''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Image Gallery</title>
            <style>
                body {{
                    background-color: purple;
                    color: white;
                    text-align: center;
                    font-family: Arial, sans-serif;
                }}
                .dancing-character {{
                    font-size: 50px;
                    animation: dance 1s infinite;
                }}
                @keyframes dance {{
                    0% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-20px); }}
                    100% {{ transform: translateY(0); }}
                }}
            </style>
          </head>
          <body>
            <h1>Image Gallery</h1>
            <p class="dancing-character">💃</p>
            <a href="/upload">Upload New Image</a>
            {image_tags}
          </body>
        </html>
        '''
    else:
        return '''
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Image Gallery</title>
            <style>
                body {{
                    background-color: purple;
                    color: white;
                    text-align: center;
                    font-family: Arial, sans-serif;
                }}
                .dancing-character {{
                    font-size: 50px;
                    animation: dance 1s infinite;
                }}
                @keyframes dance {{
                    0% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-20px); }}
                    100% {{ transform: translateY(0); }}
                }}
            </style>
          </head>
          <body>
            <h1>Image Gallery</h1>
            <p class="dancing-character">💃</p>
            <a href="/upload">Upload New Image</a>
            <p>No images in gallery.</p>
          </body>
        </html>
        '''

@app.route('/delete', methods=['POST'])
def delete_image():
    image_name = request.form['image_name']
    result = gallery.delete_image(image_name)
    return f'''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Delete Image</title>
        <meta http-equiv="refresh" content="2; url=/" />
        <style>
            body {{
                background-color: purple;
                color: white;
                text-align: center;
                font-family: Arial, sans-serif;
            }}
            .dancing-character {{
                font-size: 50px;
                animation: dance 1s infinite;
            }}
            @keyframes dance {{
                0% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-20px); }}
                100% {{ transform: translateY(0); }}
            }}
        </style>
      </head>
      <body>
        <h1>{result}</h1>
        <p class="dancing-character">💃</p>
        <p>Redirecting to the gallery...</p>
      </body>
    </html>
    '''

if __name__ == "__main__":
    app.run()
