# image-colorization-exploration
An attempt to colorize my old photos

![res](./assets/res.png)

## Our Solution

Among the countless architectural alternatives (see [LINK TO MY ARTICLE - WHICH WILL BE BASICALLY THE SAME MARKDOWN WITH SOME ADDITIONAL RESULTS...]), we will design our own solution and train it using our own dataset. We will focus natural images.

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
