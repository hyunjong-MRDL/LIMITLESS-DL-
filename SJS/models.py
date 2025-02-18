import torch.nn as nn
import timm

class ResNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = timm.create_model("resnet50", pretrained=True)
        self.model.fc = nn.Linear(in_features=2048, out_features=2, bias=True)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.model(x)
        x = self.softmax(x)
        
        return x

class VGG16(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = timm.create_model("vgg16_bn", pretrained=True)
        self.model.head.fc = nn.Linear(in_features=4096, out_features=2, bias=True)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.model(x)
        x = self.softmax(x)
        
        return x

class Inception(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = timm.create_model("inception_v3", pretrained=True)
        self.model.fc = nn.Linear(in_features=2048, out_features=2, bias=True)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.model(x)
        x = self.softmax(x)
        
        return x

class GlandNet(nn.Module):
    def __init__(self):
        super(GlandNet, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 3, 1, 1),  # input shape: (batch, 3, 256, 256)
            nn.ReLU(),
            nn.MaxPool2d(2),            # output shape: (batch, 32, 128, 128)
            nn.Conv2d(32, 64, 3, 1, 1),
            nn.ReLU(),
            nn.MaxPool2d(2),            # output shape: (batch, 64, 64, 64)
            nn.Conv2d(64, 128, 3, 1, 1),
            nn.ReLU(),
            nn.MaxPool2d(2),            # output shape: (batch, 128, 32, 32)
            nn.Conv2d(128, 256, 3, 1, 1),
            nn.ReLU(),
            nn.MaxPool2d(2)             # output shape: (batch, 256, 16, 16)
        )
        self.fc = nn.Linear(256 * 16 * 16, 1024)  # output shape: (batch, 1024)

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        
        return x
    
class VectorSumModel(nn.Module):
    def __init__(self):
        super(VectorSumModel, self).__init__()
        self.PG_model = GlandNet()
        self.SG_model = GlandNet()
        self.fc_fusion = nn.Sequential(
            nn.Linear(1024, 256),  # vector sum does NOT change the channel size
            nn.ReLU(),
            nn.Linear(256, 1),     # output shape: (batch, 1)
            nn.Sigmoid()
        )
    
    def forward(self, PG_img, SG_img):
        f1 = self.PG_model(PG_img)
        f2 = self.SG_model(SG_img)
        fused_feat = f1 + f2
        output = self.fc_fusion(fused_feat)

        return output
    
class AttnModel(nn.Module):
    def __init__(self):
        super(AttnModel, self).__init__()
        self.PG_model = GlandNet()
        self.SG_model = GlandNet()
        self.fc_fusion = nn.Sequential(
            nn.Linear(1024, 256),  # vector sum does NOT change the channel size
            nn.ReLU(),
            nn.Linear(256, 1),     # output shape: (batch, 1)
            nn.Sigmoid()
        )
    
    def forward(self, PG_img, SG_img):
        f1 = self.PG_model(PG_img)
        f2 = self.SG_model(SG_img)
        fused_feat = f1 + f2
        output = self.fc_fusion(fused_feat)

        return output