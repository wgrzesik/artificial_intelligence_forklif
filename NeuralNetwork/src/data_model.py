import torch.nn as nn 
import torch


class DataModel(nn.Module):
    def __init__(self, num_objects):
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
        self.fc = nn.Linear(in_features=48*112*112, out_features=num_objects)

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