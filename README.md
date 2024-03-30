Facial Biometric Using Python
This project is a Python-based application that utilizes face recognition technology to automate student attendance tracking. The program leverages computer vision techniques and machine learning algorithms to capture student images, recognize their faces, and record their attendance in a convenient and efficient manner.

Features
Captures student images using a webcam
Associates each student's face image with their name and matriculation number
Trains a face recognition model using the LBPH algorithm
Performs real-time face recognition on the captured video stream
Matches detected faces with registered student images
Records student attendance in a CSV file with timestamp
Prerequisites
Python 3.x
OpenCV
NumPy
Pillow (Python Imaging Library)
pandas
tkinter (for GUI)
Installation


Clone the repository:


Install the required Python packages:

Copy code
pip install opencv-python numpy pillow pandas
Usage
Run the main script:

Copy code
python main.py
The GUI window will appear.
Enter the student's name and matriculation number in the respective fields.
Click the "Take Image" button to capture the student's face image using the webcam.
Repeat steps 3 and 4 for all students.
Once all student images are captured, click the "Track Image" button to start the face recognition process.
The program will display the recognized student names and mark their attendance in the CSV file.
Project Structure

License
This project is licensed under the MIT License.

Acknowledgements
The project utilizes the OpenCV library for computer vision tasks.
The face recognition algorithm is based on the LBPH method.


References
PyImageSearch: Raspberry Pi Face Recognition
Medium: Build a Face Recognition-based Attendance System in Python
