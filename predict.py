from Final_Model_Google_Colab.pytorch_YOLOv4 import models
import os
test_images = [f for f in os.listdir('Final_Model_Google_Colab/test') if f.endswith('.jpg')]
import random
img_path = "Final_Model_Google_Colab/test/" + random.choice(test_images)


weight = 'Final_Model_Google_Colab/Final_Model.pth'
num_classes = 2
names_classes = 'Final_Model_Google_Colab/test/_classes.txt'
models.predict(num_classes,weight,img_path,names_classes)