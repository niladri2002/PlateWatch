from flask import Flask, request
import subprocess
import cv2
import os
import base64
from flask_cors import CORS
from flask import Flask, request, jsonify


app = Flask(__name__)
CORS(app)
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded_string

@app.route('/ocr', methods=['POST'])
def ocr_with_detection():
    # Save the uploaded image file
    image_file = request.files['image']
    image_file.save('input_image.jpg')
    filename = image_file.filename

# Save the uploaded image with the same filename as received
    image_path = os.path.join(os.getcwd(), filename)
    image_file.save(image_path)        
    
    # img = cv2.imread(image_path)

    # # Display the image
    # cv2.imshow('Original Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



    # Run the predictWithOCR.py file with the uploaded image
    command = "python predictWithOCR.py model='best.pt' source='input_image.jpg'"

    subprocess.run(command, shell=True)
    detect_dir = 'runs/detect'
    list_of_dirs = [os.path.join(detect_dir, d) for d in os.listdir(detect_dir) if os.path.isdir(os.path.join(detect_dir, d))]
    latest_dir = max(list_of_dirs, key=os.path.getctime)

    # Print the latest directory path
    print("hello =", latest_dir)
    image_files = [f for f in os.listdir(latest_dir) if os.path.isfile(os.path.join(latest_dir, f))]
    if image_files:
        latest_image_file = os.path.join(latest_dir, image_files[0])
        print("Latest image file:", latest_image_file)
        
        # Read and display the image using OpenCV
        uploaded_image = cv2.imread(latest_image_file)
        cv2.imshow('Latest Uploaded Image', uploaded_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("No image files found in the latest directory.")
    
    encoded_uploaded_image = encode_image('input_image.jpg')
    encoded_latest_image = encode_image(latest_image_file)

        # Return JSON response with both images
    response_data = {
            "uploaded_image": encoded_uploaded_image,
            "latest_image": encoded_latest_image
        }
    return jsonify(response_data)

    
    
    
if __name__ == '__main__':
    app.run(debug=True)



 #   !git clone https://github.com/Arijit1080/Licence-Plate-Detection-using-YOLO-V8.git
