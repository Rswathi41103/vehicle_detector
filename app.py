from flask import Flask, render_template, request, redirect, url_for
from vehicle_identifier import VehicleIdentifier
import os
import cv2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def detect_and_count_vehicles(image_path):
    vd = VehicleIdentifier()
    img = cv2.imread(image_path)
    vehicle_boxes = vd.detect_vehicles(img)
    vehicle_count = len(vehicle_boxes)
    marked_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'detected_image.jpg')
    for box in vehicle_boxes:
        x, y, w, h = box
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imwrite(marked_image_path, img)
    return marked_image_path, vehicle_count

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            # Save the uploaded file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            # Detect and count vehicles
            detected_image_path, vehicle_count = detect_and_count_vehicles(file_path)
            return render_template("index.html", detected_image=detected_image_path, vehicle_count=vehicle_count)
    return render_template("index.html")

@app.route("/uploaded")
def uploaded():
    uploaded_images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("uploaded.html", uploaded_images=uploaded_images)

if __name__ == "__main__":
    app.run(debug=True)
