from PIL import Image
import argparse
import torchvision.transforms.functional as F
import torch

from networks import build_model

parser = argparse.ArgumentParser(description='PyTorch ImageNet Training')
parser.add_argument('-f','--filter_size', default=1, type=int,
                    help='anti-aliasing filter size')
parser.add_argument('-a', '--arch', metavar='ARCH', default='resnet18')
parser.add_argument('--pretrained', dest='pretrained', action='store_true',
                    help='use pre-trained model')
parser.add_argument('--weights', default=None, type=str, metavar='PATH',
                    help='path to pretrained model weights')
args = parser.parse_args()

img = Image.open("/home/xueyan/antialias-cnn/data/ILSVRC2012/val/n04228054/ILSVRC2012_val_00000568.JPEG")

mean=[0.485, 0.456, 0.406]
std=[0.229, 0.224, 0.225]

img = F.resize(img, (224, 224), interpolation=2)
img = F.to_tensor(img)
img = (F.normalize(img, mean=mean, std=std)[None,:]).cuda()

model = build_model(args.arch, args).cuda()

if args.weights is not None:
    print("=> using saved weights [%s]"%args.weights)
    weights = torch.load(args.weights)
    new_weights_sd = {}
    for key in weights['state_dict']:
        new_weights_sd[key[7:]] = weights['state_dict'][key]
    weights['state_dict'] = new_weights_sd
    model.load_state_dict(weights['state_dict'])

model.eval()
with torch.no_grad():
    output = model(img)