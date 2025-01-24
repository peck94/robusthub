In image classification, the objective is to train a machine learning model to categorize input images into one of several possible classes. Examples include classifying tissue samples as healthy or diseased, or classifying images according to the most salient object present in them (e.g., cats and dogs). The most common image classification data sets used for benchmarking purposes, are the MNIST, Fashion-MNIST, CIFAR-10, CIFAR-100 and ImageNet data sets. Popular deep neural network architectures for these tasks include convolutional neural networks such as ResNet, WideResNet and VGG as well as vision transformers.

### Metrics

* **Accuracy.** For robust image classification, the accuracy of the algorithm in standard and adversarial settings is the most important metric.

### Threat models

* **$L_p$-bounded perturbations.** In the $L_p$ threat model, the distance between two images (under $L_p$ norm) must not exceed some given $\varepsilon$. This budget depends on the application.
* **Patch attacks.** In a patch attack, the attacker is allowed to arbitrarily modify small (typically rectangular) patches within the original image without constraint. The budget is given by the maximum area of the patch.

### References

* [An introduction to adversarially robust deep learning](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10313059)
* [Denoised Smoothing: A Provable Defense for Pretrained Classifiers](https://proceedings.neurips.cc/paper_files/paper/2020/file/f9fd2624beefbc7808e4e405d73f57ab-Paper.pdf)
* [Obfuscated Gradients Give a False Sense of Security: Circumventing Defenses to Adversarial Examples](https://arxiv.org/abs/1802.00420)
* [Towards Deep Learning Models Resistant to Adversarial Attacks](https://arxiv.org/abs/1706.06083)
* [Towards Evaluating the Robustness of Neural Networks](https://arxiv.org/abs/1608.04644)
