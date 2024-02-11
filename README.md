# Overview
## Violence Detection System 
The aim is to develop an intelligent Violence Detection System (VDS) that uses advanced technologies, including computer vision and deep learning, to automatically detect violent actions in real-time. Where the system is designed to take frames from surveillance cameras to display it for the user to monitor and to detect whether there is violent action or not. When violent action detected the system generated alert to notify authorities.

## Project idea 
The idea of the system is to read a series of frames to detect violent action. First, read the skeleton key points of people and then send the frame to calculate the specific distance between two persons if they are close to each other, then take their skeleton key points for 64 frames to predict the actionsthen send the frame to calculate the specific distance between two persons if they are close to each other, then take their skeleton key points for 64 frames to predict the actions if there is violence or not. if there is violence or not.

## Dataset
This project is planned to be used first on public buses. I thought about the simple actions of passengers in four classes, such as standing and holding for non-violent actions while punching with one-hand and punching with two-hands for violent actions. As planned, 64 frames (about 2 seconds) are needed to predict the action. I used the macro in my phone camera to start recording 2-second videos.
### Data Processing
After finishing recording videos, I needed to apply YOLOv8 pose estimation to detect and extract the keypoints of the person as demonstrated in **Figure**.

![image](https://github.com/Abdallah-Elghandour/Violence-Detection-System/assets/132736956/9e6b6c00-4f1e-4eb4-8d4d-2dfcd8068e0a)

YOLOv8 pose finds 34 values of (x, y) of 17 keypoints as joints of a person as demonstrated in **Figure**. So, we need to transform videos into a 3-dimensional array (1, 64, 34), as 1 video is a sequence of 64 frames, and in each frame, 34 values of keypoints of the person. As a result, the model will understand the pattern of the sequence of the keypoints movements.

![image](https://github.com/Abdallah-Elghandour/Violence-Detection-System/assets/132736956/e28abef0-2abd-46ae-9581-8e2d717b250a)

### Data Analysis
As a result, 2501 videos have been recorded, divided into 400 standing, 799 holding, 804 1-hand punching, and 498 2-hands punching. After cleaning the data, it consisted of 393 standing, 742 holding, 737 1-hand punching, and 437 2-hands punching. Calculating the amount of data, columns number is 34, to calculate number of class’s rows = class’s videos * 64 frames. Standing class consists of 393 * 64 = 25152 rows, Holding class 742 * 64 = 47488 rows, 1-hand punching class 737 * 64 = 47168 rows, 2-hands punching class 437 * 64 = 27968 rows. Total rows = 147776.


## Architecture

![image](https://github.com/Abdallah-Elghandour/Violence-Detection-System/assets/132736956/c4238960-a61a-4fd9-98ca-5836694841c5)

## Implementation
In this section, I am going to describe my implementation processes which includes transforming the dataset, building the model, and building the application.
### Data Transformation
As I mentioned before, I need to extract the keypoints of the person from the videos dataset to train our model. By using OpenCv library that allows reading frames of video, after that sending the frame for yolov8 pose prediction to get the keypoints, lastly appends the keypoints in array to continue until it reaches 64 frames as a one action to appends them in the class dataset file and append class label in class label file as demonstrated in **Figure**. It will do this step for each class. After that append all classes dataset in one file to prepare it for training. 

![image](https://github.com/Abdallah-Elghandour/Violence-Detection-System/assets/132736956/21746e59-f48c-48ba-b38f-ba9b11373cdd)

### Building the Model
#### Load and Split Data
As all data is in a single file, I had to split it into train, test, valid data. Which train data is 8o%, test data is 10%, and valid data is 10%.
#### Model Architecture
I
 build my model with deep network that consisted of 7 layers with combination of
Long Short-Term Memory (LSTM) layers and fully connected (Dense) layers will be
described in the following and demonstrated in **Figure**, first layer is
the Dense input layer which it takes 34 units of batch input shape (100, 64,
34) with ReLU activation function, then 4 LSTM layers which they take 128, 64,
34, 34 units respectively and they return sequence of outputs except last
layer, then Dense layer of 64 units with ReLU activation function, last layer is
Dense layer with 4 units with softmax activation function and regularization
terms to prevent overfitting. The model is compiled with categorical
crossentropy as the loss function which is commonly used for multi-class
classification problems. Adam optimizer is used with a specified learning rate.

![image](https://github.com/Abdallah-Elghandour/Violence-Detection-System/assets/132736956/2d012f4f-05c3-43b5-99a8-e353a56fadec)

#### Training
 I specified learning rate with 1e^-4, epochs 300, and batch size 100. 	The last result of epoch iteration was 104 where Early Stopping stopped the training process.
#### Accuracy & Loss
![image](https://github.com/Abdallah-Elghandour/Violence-Detection-System/assets/132736956/ebab07f2-ad68-4fa7-9322-d1dac8b3266f)

#### Evaluation
![image](https://github.com/Abdallah-Elghandour/Violence-Detection-System/assets/132736956/d67dd89b-5158-4a16-be9b-f1aeef80f936)

### Building the Application
The application is designed to enable users to initiate streaming by selecting the start button. During streaming, the camera sends frames to the system, utilizing YOLOv8 for person detection. The system calculates the centroid point for each detected person, which is crucial for subsequent operations. Following person detection, the system identifies the two closest individuals by calculating the distance between their centroid points. Every 64 frames, keypoints of the two individuals are sent for action prediction. For enhanced accuracy, three consecutive sets of 64 frames are considered. If four or more predictions indicate violent actions, the system triggers violence detection. Upon detecting violence, the system initiates an email notification to the authorized person and logs the violence detection event information such as cameraID, time stamp, and location in the database.
To implement the application, Flask, a Python backend framework, was chosen. Three APIs were created: the first for the main website, the second for user inputs (such as start or stop requests), and the third for displaying the video feed. Additionally, Resend API is used for email notifications, and the MongoDB API to insert logs to the database.
The application’s user interface is composed of a bar that has the application logo, container that has video feed border, and a changeable button between Start\Stop as demonstrated in **Figure**.
![image](https://github.com/Abdallah-Elghandour/Violence-Detection-System/assets/132736956/931a3c27-0783-488f-8109-195e174f56a6)
