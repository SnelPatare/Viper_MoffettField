from flask import Flask, render_template, request, Response, send_file
import cv2, os, tempfile

app = Flask(__name__)
camera = cv2.VideoCapture(0)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        user_name = last_name + "_" + first_name
        contact_filename = user_name + '.txt'
        # Save the contact form data to a local file
        with open(contact_filename, 'a') as file:
            file.write(f"First Name: {first_name}\n")
            file.write(f"Last Name: {last_name}\n")
            file.write(f"Email: {email}\n")
            file.write(f"Phone Number: {phone_number}\n")
            file.write('\n')

        return 'Contact form submitted successfully!'

    return render_template('index.html')

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/take_picture')
def take_picture():
    success, frame = camera.read()
    if success:
        # Save the captured picture to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_image:
            cv2.imwrite(temp_image.name, frame)
            image_path = temp_image.name

        return render_template('picture.html', image_path=image_path)
    else:
        return 'Failed to capture picture.'

@app.route('/save_picture', methods=['POST'])
def save_picture():
    image_path = request.form['image_path']
    if image_path:
        # Move the picture to a desired location
        save_path = 'saved_pictures'
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        new_image_path = os.path.join(save_path, 'captured_picture.jpg')
        os.replace(image_path, new_image_path)

        return f'Picture saved successfully at: {new_image_path}'
    else:
        return 'No picture found to save.'


if __name__ == '__main__':
    app.run(debug=True)
