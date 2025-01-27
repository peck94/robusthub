Medical images are typically acquired through a very noisy measuring process, such as MR or CT scans. The output of most medical scanners is not directly usable for diagnostic purposes due to this noise, and images therefore need to be denoised or *reconstructed* before medical personnel can make sense of them. Many classical algorithms exist that are currently in widespread use in commercial scanners, such as total variation and wavelet denoising. These algorithms are often specializations of proximal operators and hence enjoy certain mathematical guarantees on their fidelity.

With the rise of deep learning in computer vision, researchers have naturally attempted to improve classical denoising algorithms using neural networks. This has led to quite a few studies claiming state-of-the-art performance in medical image reconstruction. However, with the vulnerability of deep neural networks to adversarial perturbations, the reliability of these methods is not clear, and mathematical guarantees are often absent. It has been shown that neural networks trained to reconstruct medical images (or, more generally, solve linear inverse problems) are *unstable*: they can easily hallucinate non-existent features or leave out diagnostically relevant features from the reconstructions entirely.

### Metrics

* **SSIM.** The [Structural Similarity Index Measure](https://en.wikipedia.org/wiki/Structural_similarity_index_measure) (SSIM) is often used to train and evaluate generative models for image restoration.
* **MSE.** The Mean Squared Error (MSE) is simply the squared $L_2$ distance between the reference image and the reconstruction.
* **PSNR.** [Peak Signal-to-Noise Ratio](https://en.wikipedia.org/wiki/Peak_signal-to-noise_ratio) (PSNR) is also a common metric to assess the fidelity of image reconstructions.

### Threat models

* **$L_p$-bounded perturbations.** In the $L_p$ threat model, the distance between two images (under $L_p$ norm) must not exceed some given $\varepsilon$. This budget depends on the application.
* **Patch attacks.** In a patch attack, the attacker is allowed to arbitrarily modify small (typically rectangular) patches within the original image without constraint. The budget is given by the maximum area of the patch.

### References

* [Accelerated MRI reconstructions via variational network and feature domain learning](https://www.nature.com/articles/s41598-024-59705-0)
* [Solving Inverse Problems With Deep Neural Networks – Robustness Included?](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9705105)
* [On learning adaptive acquisition policies for undersampled multi-coil MRI reconstruction](https://proceedings.mlr.press/v172/bakker22a.html)
* [The troublesome kernel -- On hallucinations, no free lunches and the accuracy-stability trade-off in inverse problems](https://arxiv.org/abs/2001.01258)
* [On instabilities of deep learning in image reconstruction and the potential costs of AI](https://www.pnas.org/doi/full/10.1073/pnas.1907377117)
