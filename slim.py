import paddle
from paddle.vision.models import mobilenet_v1
paddle.disable_static()
net = mobilenet_v1(pretrained=False)
paddle.summary(net, (1, 3, 32, 32))

import paddle.vision.transforms as T
transform = T.Compose([
                    T.Transpose(),
                    T.Normalize([127.5], [127.5])
                ])
train_dataset = paddle.vision.datasets.Cifar10(mode="train", backend="cv2",transform=transform)
val_dataset = paddle.vision.datasets.Cifar10(mode="test", backend="cv2",transform=transform)

from __future__ import print_function
print(f'train samples count: {len(train_dataset)}')
print(f'val samples count: {len(val_dataset)}')
for data in train_dataset:
    print(f'image shape: {data[0].shape}; label: {data[1]}')
    break

from paddle.static import InputSpec as Input
optimizer = paddle.optimizer.Momentum(
        learning_rate=0.1,
        parameters=net.parameters())

inputs = [Input([None, 3, 32, 32], 'float32', name='image')]
labels = [Input([None], 'int64', name='label')]

model = paddle.Model(net, inputs, labels)

model.prepare(
        optimizer,
        paddle.nn.CrossEntropyLoss(),
        paddle.metric.Accuracy(topk=(1, 5)))

model.fit(train_dataset, epochs=2, batch_size=128, verbose=1)
result = model.evaluate(val_dataset,batch_size=128, log_freq=10)
print(result)

from paddleslim.dygraph import L1NormFilterPruner
pruner = L1NormFilterPruner(net, [1, 3, 224, 224])

