# TorchStuff

Calculate the Polygon area and length (perimeter).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Installation

```bash
pip3 install torchstuff
```
## Usage

```python
import torch

# Example vertices
vertices = torch.tensor([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])

# Create Polygon object
polygon = Polygon(vertices)

# Access properties
area = polygon.area
length = polygon.length

print(f"Area: {area}, Length: {length}")

```
## Contributing

Just me for now
