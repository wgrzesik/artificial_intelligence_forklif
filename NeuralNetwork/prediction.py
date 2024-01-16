import torch
import torch.nn as nn
from torchvision.transforms import transforms
import numpy as np
from torch.autograd import Variable
from torchvision.models import squeezenet1_1
import torch.functional as F
from io import open
import os
from PIL import Image
import pathlib
import glob
from tkinter import Tk, Label
from PIL import Image, ImageTk

absolute_path = os.path.abspath('NeuralNetwork/src/train_images')
train_path = absolute_path
absolute_path = os.path.abspath('Images/Items_test')
pred_path = absolute_path

root=pathlib.Path(train_path)
classes=sorted([j.name.split('/')[-1] for j in root.iterdir()])


class DataModel(nn.Module):
    def __init__(self, num_classes):
        super(DataModel, self).__init__()
        #input (batch=256, nr of channels rgb=3 , size=244x244)

        # convolution
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=3, stride=1, padding=1)
        #shape (256, 12, 224x224)

        # batch normalization
        self.bn1 = nn.BatchNorm2d(num_features=12)
        #shape (256, 12, 224x224)
        self.reul1 = nn.ReLU()

        self.pool=nn.MaxPool2d(kernel_size=2, stride=2)
        # reduce image size by factor 2
        # pooling window moves by 2 pixels at a time instead of 1
        # shape (256, 12, 112x112)



        self.conv2 = nn.Conv2d(in_channels=12, out_channels=24, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(num_features=24)
        self.reul2 = nn.ReLU()
        # shape (256, 24, 112x112)

        self.conv3 = nn.Conv2d(in_channels=24, out_channels=48, kernel_size=3, stride=1, padding=1)
        #shape (256, 48, 112x112)
        self.bn3 = nn.BatchNorm2d(num_features=48)
        #shape (256, 48, 112x112)
        self.reul3 = nn.ReLU()

        # connected layer
        self.fc = nn.Linear(in_features=48*112*112, out_features=num_classes)

    def forward(self, input):
            output = self.conv1(input)
            output = self.bn1(output)
            output = self.reul1(output)

            output = self.pool(output)
            output = self.conv2(output)
            output  = self.bn2(output)
            output = self.reul2(output)
            
            output = self.conv3(output)
            output = self.bn3(output)
            output = self.reul3(output)

            # output shape matrix (256, 48, 112x112)
            #print(output.shape)
            #print(self.fc.weight.shape)

            output = output.view(-1, 48*112*112)
            output = self.fc(output)
            
            return output

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'best_model.pth')
checkpoint=torch.load(file_path)
model = DataModel(num_classes=2)
model.load_state_dict(checkpoint)
model.eval()

transformer = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize images to (224, 224)
    transforms.ToTensor(),  # Convert images to tensors, 0-255 to 0-1
    # transforms.RandomHorizontalFlip(),  # 0.5 chance to flip the image
    transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5]) 
])

def prediction(img_path,transformer):
    
    image=Image.open(img_path)
    
    image_tensor=transformer(image).float()
    
    image_tensor=image_tensor.unsqueeze_(0)
    
    if torch.cuda.is_available():
        image_tensor.cuda()
        
    input=Variable(image_tensor)
    
    output=model(input)
    
    index=output.data.numpy().argmax()
    
    pred=classes[index]
    
    return pred

def prediction_keys():

    #funkcja zwracajaca sciezki do kazdego pliku w folderze w postaci listy

    images_path=glob.glob(pred_path+'/*.jpg')

    pred_list=[]

    for i in images_path:
        pred_list.append(i)

    return pred_list

def predict_one(path):

    #wyswietlanie obrazka po kazdym podniesieniu itemu
    root = Tk()
    root.title("Okno z obrazkiem")

    image = Image.open(path)
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)
    label.pack()

    root.mainloop()

    #uruchamia sie funkcja spr czy obrazek to paczka czy list
    pred_print = prediction(path,transformer)
    print('Zdjecie jest: '+pred_print)
    return pred_print