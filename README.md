## AI BASED OPTHALMIC DISEASE DIAGNOSIS TOOL
AI-Based Ophthalmic Diagnosis System is a deep learning-powered application that analyzes retinal images to detect and classify eye diseases such as Diabetic Retinopathy, Glaucoma, and Macular Degeneration. The system provides accurate, real-time predictions to assist ophthalmologists in clinical decision-making.

This project integrates computer vision, AI, and web technologies to create a doctor-friendly interface for retinal image analysis.
## Features
Upload retinal images for analysis

Detect multiple ophthalmic conditions using a trained CNN model

Display prediction probabilities and disease severity

Voice-assisted diagnosis for accessibility

Generate alerts and recommendations for further medical consultation

Dashboard to manage patient history and predictions
## Data Collection

Collect retinal/fundus images from public datasets like EyePACS, Messidor, or MetaDataset.

Images include labeled categories such as Normal, Glaucoma, Diabetic Retinopathy.
Organize images into folders per class for supervised learning.
Resize all images to a uniform dimension (e.g., 224x224)

## DATA PREPROCESSING 
Normalize pixel values (0–1 scaling)

Apply augmentation (rotation, flipping, brightness adjustment) to increase dataset variety
## MODEL TRAINING 
Use a CNN architecture 
Compile with appropriate loss function (categorical_crossentropy) and optimizer (Adam)

Train the model using training dataset and validate on validation set

Evaluate metrics: accuracy, precision, recall, F1-score
<img width="1753" height="520" alt="Screenshot 2025-10-06 213608" src="https://github.com/user-attachments/assets/9186a1d8-8e86-4454-bb92-9869b7ce3788" />



Split dataset into training, validation, and test sets (e.g., 70/15/15)

