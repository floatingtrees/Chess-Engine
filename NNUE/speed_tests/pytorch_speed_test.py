import torch
from torch import nn
import timeit

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(1024, 1024),
            nn.ReLU(),
            nn.Linear(1024, 1),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork()
x = torch.rand((1, 1024))

start = timeit.default_timer()
print("starting")

for i in range(50000):
    model.forward(x)


print(timeit.default_timer() - start)
