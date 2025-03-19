# image-colorization-exploration
An attempt to colorize my old photos

![res](./assets/res.png)

## Our Solution

Among the countless architectural alternatives (see [LINK TO MY ARTICLE - WHICH WILL BE BASICALLY THE SAME MARKDOWN WITH SOME ADDITIONAL RESULTS...]), we are going to design our own and train it with our own dataset. We will focus on scenes that contain people in natural, at most semi-rural landscapes.

We use two approaches for the colorization task:

- A variational approach (see this(README VARIACIONAL)): blablab.la.

![res2](./assets/res2.png)

- A Deep Learning aproach (see this(README DL)): blablabla

[INSERT GIF similar TAKEN FROM https://miro.medium.com/v2/resize:fit:128/format:webp/1*OBfeMpUwCDdWdhT9g8u_Aw.gif]

# Usage Instructions

If you want to fork my project and explore new or existing techniques yourself, simply create a virtual environment and install the necessary dependencies as follows:

**1. Clone the project and create a virtual environment**

```bash
git clone https://github.com/agarnung/image-colorization-exploration.git
cd image-colorization-exploration
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

**2. Install the mask creation application**

```bash
cd colorMaskerApp && pip install -e .
```

**3. Run the application from anywhere (inside the venv) with the grayscale image you want to colorize**

```bash
colormaskerapp --input "path/to/grayscale.png" --output "path/to/result/mask.png"
```

# References

- With AutoEncoder (Inception-Resnet-v2): https://github.com/ajaychaudhary7/Image-Colorization
- Another with AutoEncoder [Medium](https://medium.com/@geokam/building-an-image-colorization-neural-network-part-1-generative-models-and-autoencoders-d68f5769d484) and [repo](https://github.com/PacktPublishing/Advanced-Deep-Learning-with-Keras/tree/master/chapter3-autoencoders)
- In Lab: Another with AutoEncoder + VGG as encoder (i.e., feature extractor) https://github.com/Ananyaa26/Image-Colorization-using-Deep-Learning
- With diffusion model: [Medium](https://medium.com/@erwannmillon/color-diffusion-colorizing-black-and-white-images-with-diffusion-models-269828f71c81) and [repo](https://medium.com/@erwannmillon/color-diffusion-colorizing-black-and-white-images-with-diffusion-models-269828f71c81)
- GAN + U-Net in Lab: https://github.com/moein-shariatnia/Deep-Learning/tree/main/Image%20Colorization%20Tutorial
- With VAE: https://github.com/alexandrasalem/image_colorization
- Awesome list (especially see section 2.1 based on scribble): https://github.com/MarkMoHR/Awesome-Image-Colorization?tab=readme-ov-file#21-based-on-scribble
- Mask CLI app inspired by https://github.com/aGIToz/PiMask/tree/main.

