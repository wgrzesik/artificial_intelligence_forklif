import glob
import pathlib
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import ConcatDataset

# images have to be the same size for the algorithm to work
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize images to (224, 224)
    transforms.ToTensor(),  # Convert images to tensors, 0-255 to 0-1
    # transforms.RandomHorizontalFlip(),  # 0.5 chance to flip the image
    transforms.Normalize([0.5,0.5,0.5], [0.5,0.5,0.5]) 
])

letters_path = 'C:/Users/wojmed/Documents/VS repositories/Inteligentny_Wozek/NeuralNetwork/src/train_images/letters'
package_path = 'C:/Users/wojmed/Documents/VS repositories/Inteligentny_Wozek/NeuralNetwork/src/train_images/package'
images_path = 'C:/Users/wojmed/Documents/VS repositories/Inteligentny_Wozek/NeuralNetwork/src/train_images'

# # Load images from folders
# letter_folder = ImageFolder(letters_path, transform=transform)
# package_folder = ImageFolder(package_path, transform=transform)

# Combine the both datasets into a single dataset
#combined_dataset = ConcatDataset([letter_folder, package_folder])
combined_dataset = ImageFolder(images_path, transform=transform)

#image classes
path=pathlib.Path(images_path)
classes = sorted([i.name.split("/")[-1] for i in path.iterdir()])

# print(classes)