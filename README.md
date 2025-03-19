# image-colorization-exploration
An attempt to colorize my old photos

![res](./assets/res.png)

![res2](./assets/res2.png)

# Usage Instructions

If you want to fork my project and explore new or existing techniques yourself, simply create a virtual environment and install the necessary dependencies as follows:

## 1. Clone the project and create a virtual environment

```bash
git clone https://github.com/agarnung/image-colorization-exploration.git
cd image-colorization-exploration
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

## 2. Install the mask creation application

```bash
cd colorMaskerApp && pip install -e .
```

## 3. Run the application from anywhere (inside the venv) with the grayscale image you want to colorize

```bash
colormaskerapp --input "path/to/grayscale.png" --output "path/to/result/mask.png"
```

# Main Article

[LINK TO MY ARTICLE - WHICH WILL BE BASICALLY THE SAME MARKDOWN WITH SOME ADDITIONAL RESULTS...]

Many times I have entered my old family house in the village and found extremely old photographs of relatives and distant acquaintances from 75, 100, or even 150 years ago. It is natural to mentally recolor these images, but the result usually does not meet our expectations virtually, and of course we are not going to go around drawing our great-grandmother’s hair with a marker. Therefore, in this post we will take some time to reflect on how we can design a semi-automatic system (that is, with some human "user" guidance) to colorize black and white images. This way, we can scan our old photos, process them with our software (much better than any Paint or Photoshop, of course...) and print the anachronistic result.

Of course, we will integrate variational methods. It might also be interesting to employ some type of GAN for colorization, as some commercial solutions already do [CITE EXAMPLES], although in this blog we favor the first techniques. We might also venture to say that graph-based techniques may perform better, as their nature favors the diffusion of color, which seems appropriate.

How will the application work? In a first approach we assert that one cannot invent color out of nothing unless we hallucinate it, after all. Thus, in a first approximation the user will make "a few" strokes (e.g. the skin tone for the face, the blonde for the hair, white for the clothes, green for the grass, blue and white for the sky and clouds, etc.) and the algorithm will "evolve" those colors until forming a more or less convincing image. If it is not convincing, the process can always be repeated, even using the unconvincing result as the initial seed.

In a second approach, we will model a quasi-intelligent artificial agent that will be trained with many real color images and their grayscale versions so that it can "reasonably hallucinate" the color of unknown grayscale images at test time.

This project is meant to be exemplary, so we will not focus on providing fancy results but on achieving a functional application that can serve as a basis for plug-and-play implementation of more refined methods if needed. Therefore, we will formulate an exemplary variational model and an exemplary deep learning architecture that fulfill their role correctly.

# Color Spaces

By way of introduction, we will say a few words about color spaces, which are the secondary protagonists in this story.

Intuitively, "inventing" three channels from nothing seems more complicated or even impossible compared to just two. Thus, instead of generating RGB channels, we will take the grayscale image as the luminance channel and generate the corresponding a and b channels in the Lab space. Similarly, we could fix the Y channel and generate the U and V channels of the YUV space, or another similar space. But with the first choice we do not lose generality, so we will work in Lab.

# Using Variational Methods

We will use a not-too-complex variational formulation that consists of a term that diffuses the color quite well, like the bilaplacian operator, and a term that restrains the color in regions of high gradient (object edges), in order to preserve regions with "blocky colors," such as total variation (TV). Even better, to promote "piecewise smooth" regions and achieve more visually pleasing results, we will use GTV instead of TV.

# With Deep Learning

## Discussion of Possible Solutions

### Through Diffusion Models

Diffusion models are a type of neural network that generate content from training data. First, they corrupt the original data until it becomes "unrecognizable," progressively adding noise; then, they learn to reverse this process step by step, reconstructing the data and generating new realistic samples. This process of "corruption" is called the "forward diffusion process."

This means that we design a data corruption process (forward diffusion process) that gradually reduces the amount of original information in an image until it eventually becomes completely random.

The noise added to each image at step k-1 in the process is sampled from a Gaussian distribution. The diffusion model is a neural network that learns each inverse step of the forward diffusion process—that is, it learns the denoising of the corrupted image. [https://medium.com/@erwannmillon/color-diffusion-colorizing-black-and-white-images-with-diffusion-models-269828f71c81]

What is the basic idea behind diffusion models? Fill an image with white noise and frame the problem as a denoising problem. In our case, we would corrupt the color channels of the image (with the grayscale image converted to a vector image) with white noise and frame the colorization task as a denoising problem on the a and b channels independently. Thus, we would train the model to learn to denoise the color channels using the grayscale image as conditioning.

[INSERT GIF TAKEN FROM https://miro.medium.com/v2/resize:fit:128/format:webp/1*OBfeMpUwCDdWdhT9g8u_Aw.gif]

## Our Solution

Among the countless architectural alternatives, we are going to design our own and train it with our own dataset. We will focus on scenes that contain people in natural, at most semi-rural landscapes.

# References

- With AutoEncoder (Inception-Resnet-v2): https://github.com/ajaychaudhary7/Image-Colorization
- Another with AutoEncoder [Medium](https://medium.com/@geokam/building-an-image-colorization-neural-network-part-1-generative-models-and-autoencoders-d68f5769d484) and [repo](https://github.com/PacktPublishing/Advanced-Deep-Learning-with-Keras/tree/master/chapter3-autoencoders)
- In Lab: Another with AutoEncoder + VGG as encoder (i.e., feature extractor) https://github.com/Ananyaa26/Image-Colorization-using-Deep-Learning
- With diffusion model: [Medium](https://medium.com/@erwannmillon/color-diffusion-colorizing-black-and-white-images-with-diffusion-models-269828f71c81) and [repo](https://medium.com/@erwannmillon/color-diffusion-colorizing-black-and-white-images-with-diffusion-models-269828f71c81)
- GAN + U-Net in Lab: https://github.com/moein-shariatnia/Deep-Learning/tree/main/Image%20Colorization%20Tutorial
- With VAE: https://github.com/alexandrasalem/image_colorization
- Awesome list (especially see section 2.1 based on scribble): https://github.com/MarkMoHR/Awesome-Image-Colorization?tab=readme-ov-file#21-based-on-scribble

- Mask CLI app inspired by https://github.com/aGIToz/PiMask/tree/main.

# TODO
- A small minimal app similar to the one at https://github.com/aGIToz/PiMask to colorize and save the RGB stroke masks that will be used. Using CLI to test the methods.
