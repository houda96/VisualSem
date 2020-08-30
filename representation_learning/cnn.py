import torch
import torch.nn as nn
from torchvision.models import resnet152

class CNN(nn.Module):
    def __init__(self, dim):
        super().__init__()
        resnet = resnet152(pretrained = True)

        for parameter in resnet.parameters():
            parameter.requires_grad = False

        if dim == 2048:
            self.resnet = nn.Sequential(*list(resnet.children())[:-1])
        else:
            self.resnet = resnet

    def forward(self, batch):
        encoded = self.resnet(batch)
        return encoded.reshape(encoded.shape[:2])
