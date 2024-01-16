import glob
from src.torchvision_resize_dataset import combined_dataset, images_path, classes
import src.data_model
from torch.optim import Adam
import torch 
import torch.nn as nn 
from torch.utils.data import DataLoader 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_loader = DataLoader(
    combined_dataset,   #dataset of images
    batch_size=256,     # accuracy
    shuffle=True    # rand order
)

model = src.data_model.DataModel(num_objects=2).to(device)

#optimizer 
optimizer = Adam(model.parameters(), lr=0.001, weight_decay=0.0001)
#loss function
criterion = nn.CrossEntropyLoss()

num_epochs = 20
# train_size = len(glob.glob(images_path+'*.jpg'))
train_size = 2002

go_to_accuracy = 0.0
for epoch in range(num_epochs):
    #training on dataset
    model.train()
    train_accuracy = 0.0
    train_loss = 0.0
    for i, (images, labels) in enumerate(train_loader):
        if torch.cuda.is_available():
            images = torch.Variable(images.cuda())
            labels = torch.Variable(labels.cuda())
        # clearing the optimizer gradients
        optimizer.zero_grad()

        outputs = model(images) # predoction
        loss = criterion(outputs, labels)   #loss calculation
        loss.backward()
        optimizer.step()

        train_loss += loss.cpu().data*images.size(0)
        _, prediction = torch.max(outputs.data, 1)

        train_accuracy += int(torch.sum(prediction == labels.data))

    train_accuracy = train_accuracy/train_size
    train_loss = train_loss/train_size

    model.eval()

    print('Epoch:  '+ str(epoch+1) +' Train Loss: '+ str(int(train_loss)) +' Train Accuracy: '+ str(train_accuracy))

    if train_accuracy > go_to_accuracy:
        go_to_accuracy= train_accuracy
        torch.save(model.state_dict(), "best_model.pth") 