Este modelo de deep learning se basa en BLABLABLA.

- El script test.py sirve para poner a prueba nuestro modelo de colorización con la imagen de entrada, e.g.:

```bash
test.py /full/path/to/image.png
```

Se guardará el resultado en el mismo path desde el que se invoca el comando.

Problemas principales en el colorizig?:

- **Color bleeding**: el problema por le cual el color de una región se trasnfiere a lo largo y ás allá de las frontesras que separan objetos que deberían tener colores distintos, causnado un esparcimiento incoherente del color y problemas de blending y innacuracies en el resultado final colorizado.

**Estado del arte**:

Referimos al _Related Works_ del artículo [TÍTULO](https://arxiv.org/pdf/2208.08295v1) para una revisión de varios métodos exitosos de colorización de imágenes, divididos en vraios grupos:
1. **User-guided colorization**: Métodos que requieren intervención humana, donde el usuario proporciona trazos o puntos de color en la imagen en escala de grises. Estos colores iniciales se propagan por la imagen basándose en la similitud de luminancia, bordes o texturas e incluso funciones de edge-stopping para prevenir el color bleeding entre regiones. Algunos métodos combinan esta técnica con aprendizaje profundo para reducir el esfuerzo manual.
2. **Example-guided colorization**: Métodos que utilizan imágenes de referencia para transferir colores de la referencia al resultado deseado. Pueden basarse en estadísticas globales como la media y la varianza del color, o en transferencias más detalladas que consideran la estructura de la imagen a nivel de píxel o segmentos. La calidad del resultado depende en gran medida de la imagen de referencia utilizada.
3. **Learning-based colorization**: Métodos completamente automáticos que utilizan redes neuronales entrenadas con grandes conjuntos de datos para aprender patrones de colorización. Algunos enfoques combinan información semántica ("modelos multimodales") con modelos de aprendizaje profundo para mejorar la coherencia de los colores en distintos objetos y escenas. Otros buscan manejar la variabilidad de los colores naturales generando múltiples posibles colorizaciones.
4. **Image colorization with GANs**: Métodos basados en redes generativas adversariales (GANs), donde un modelo aprende a generar imágenes en color a partir de versiones en escala de grises. Algunas aproximaciones utilizan auto-supervisión para mejorar la calidad del color y la coherencia semántica, mientras que otras combinan múltiples redes (paralelas) para manejar mejor el color en diferentes partes de la imagen, y luego fusionan sus salidas en un resultdao final.

Tanto los métodos tradicionales como los de3 prendizaje automático incorporan términos matemáticos localizables en sus funciones de coste, como regularizadores, para promover cierta característica deseable para buscar una solucion coherente en el vasto espacio de imágenes.

# Features

- Se usa Conformal Prediction para, además del resultado de la imagen colorizada RGB, se usa un set de calibración gracias al que se calibra el modelo para proporcionar un conjunto de 3 matrices R^mxnx2 con rango de conformidad (1-alpha) % para los R, G, y B verdaderos. Es decir, tres máscaras que contienen aquellos rangos de valores (R, G, B) dentro de los que está el color verdadero con una probabilidad empírica y teóricamente probale de (1-alpha) %, bajo el supuesto de intercambiabilidad.

[INSERTAR IMAGEN EXPLICATIVA TODO SISTEMA DL y SALIDA CONFOMAL PREDICTION](./dl.png)

# References

- With AutoEncoder (Inception-Resnet-v2): https://github.com/ajaychaudhary7/Image-Colorization
- Another with AutoEncoder [Medium](https://medium.com/@geokam/building-an-image-colorization-neural-network-part-1-generative-models-and-autoencoders-d68f5769d484) and [repo](https://github.com/PacktPublishing/Advanced-Deep-Learning-with-Keras/tree/master/chapter3-autoencoders)
- In Lab: Another with AutoEncoder + VGG as encoder (i.e., feature extractor) https://github.com/Ananyaa26/Image-Colorization-using-Deep-Learning
- With diffusion model: [Medium](https://medium.com/@erwannmillon/color-diffusion-colorizing-black-and-white-images-with-diffusion-models-269828f71c81) and [repo](https://medium.com/@erwannmillon/color-diffusion-colorizing-black-and-white-images-with-diffusion-models-269828f71c81)
- GAN + U-Net in Lab: https://github.com/moein-shariatnia/Deep-Learning/tree/main/Image%20Colorization%20Tutorial
- With VAE: https://github.com/alexandrasalem/image_colorization
- Grayscale Image Colorizations using GANs: [gan-image-colorizer](https://github.com/prajwaldp/gan-image-colorizer)

- Awesome list (especially see section 2.1 based on scribble): https://github.com/MarkMoHR/Awesome-Image-Colorization?tab=readme-ov-file#21-based-on-scribble
- ParaColorizer: [web](https://deepai.org/publication/paracolorizer-realistic-image-colorization-using-parallel-generative-networks) y [paper](https://arxiv.org/pdf/2208.08295v1).