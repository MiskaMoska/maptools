import torchvision.transforms as transforms
from torchvision.io import image
import torchvision as tv

trans = transforms.Compose([
    transforms.Resize([10, 10]),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))
])

testset = tv.datasets.ImageFolder(root=r'C:\Users\wx98\Downloads\val', transform=trans)


# img = image.read_image('work/test1.png').float()
# img = trans(img)


