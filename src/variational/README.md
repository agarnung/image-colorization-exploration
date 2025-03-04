Este modelo variacional se basa en la minimización de un funcional de energía que combina dos términos:
- Un **término de suavizado o regularización**, encargado de difundir el color por los objetos de la imagen.
- Un **término de fidelidad de datos**, que se encarga de que los colores impuestos por el usuario se mantengan consistentes con el resultado final.

Dada una imagen en escala de grises $I_L(x, y)$, que representa el canal de luminancia $L$ del espacio de color Lab, queremos encontrar los canales de color de dicho espacio, $I_a(x, y)$ y $I_b(x, y)$, que minimicen el siguiente funcional:

$$
E(I_a, I_b) = \lambda \int_\Omega \left( |\nabla I_a|^2 + |\nabla I_b|^2 \right) \ dx \ dy + \int_\Omega \left( \gamma (I_a - \tilde{I}_a)^2 + \gamma (I_b - \tilde{I}_b)^2 \right) \ dx \ dy = R(I_a, I_b) + D(I_a, I_b)
$$

Donde:
- $\Omega$ es el dominio de la imagen.
- $\lambda$ es un parámetro que controla la suavidad de los canales de color.
- $\gamma$ es un parámetro que controla la fidelidad a los valores de referencia $\tilde{I}_a$ y $\tilde{I}_b$.
- $\tilde{I}_a$ y $\tilde{I}_b$ son los valores de referencia para los canales $a$ y $b$, que pueden provenir de pistas de color proporcionadas por el usuario.
- $|\nabla I_a|^2$ y $|\nabla I_b|^2$ son los gradientes de los canales de color, que miden la variación espacial de los colores.

El **regularizador** $R(I_a, I_b)$ penaliza las variaciones bruscas en los canales de color, fomentando que los colores varíen suavemente en la imagen. Hemos querido darle suma importancia al concepto de suavidad en esta formulación, debido a que los trazos del usuario son muy _sparse_ y, por tanto, deben difundirse por enormes regiones en la imagen. Por eso elegimos la norma $L^2$ del gradiente como regularizador.

El **data term** $D(I_a, I_b)$ asegura que los canales de color $I_a$ e $I_b$ se mantengan cercanos a los valores de referencia $\tilde{I}_a$ y $\tilde{I}_b$ (a los trazos o indicaciones del usuario). El parámetro $\gamma$ controla cuánto se prioriza la fidelidad a las pistas de color.

Para minimizar el funcional, recurrimos a la teoría del cálculo variacional y derivamos sus ecuaciones de Euler-Lagrange, que son ecuaciones diferenciales parciales (PDES) que describen cómo deben evolucionar $I_a$ e $I_b$ para minimizar la energía.

Las ecuaciones de Euler-Lagrange para $I_a$ e $I_b$ son:

$$
\lambda \Delta I_a - \gamma (I_a - \tilde{I}_a) = 0
$$
$$
\lambda \Delta I_b - \gamma (I_b - \tilde{I}_b) = 0
$$

Donde:
- $\Delta I_a$ y $\Delta I_b$ son los laplacianos de $I_a$ e $I_b$, que miden la divergencia del gradiente (es decir, cómo varía la variación espacial de los colores).
- $\tilde{I}_a$ y $\tilde{I}_b$ son los valores de referencia para los canales $a$ y $b$.

Para resolver las ecuaciones de Euler-Lagrange numéricamente, adoptamos un enfoque sencillo y discretizamos las ecuaciones usando diferencias finitas, mediante un esquema explícito de descenso del gradiente:

$$
I_a^{t+1}(x, y) = I_a^t(x, y) + \alpha \left( \lambda \Delta I_a^t - \gamma (I_a^t - \tilde{I}_a) \right)
$$

$$
I_b^{t+1}(x, y) = I_b^t(x, y) + \alpha \left( \lambda \Delta I_b^t - \gamma (I_b^t - \tilde{I}_b) \right)
$$

Donde:
- $\alpha$ es el paso de actualización (tasa de aprendizaje).
- $\Delta I_a^t$ y $\Delta I_b^t$ son los laplacianos en la iteración $t$.

Además, para computar el Laplaciano $\Delta I$, lo aproximamos usando un kernel de convolución:

$$
\Delta I \approx \begin{bmatrix}
0 & 1 & 0 \\
1 & -4 & 1 \\
0 & 1 & 0
\end{bmatrix} * I
$$

Para respetar las condiciones iniciales proporcionadas por el usuario (trazas de color), integramos condiciones de contorno de Dirichlet en las regiones conocidas $\Omega \setminus D$, donde $D$ es la zona a colorizar, e introducimos una máscara $M(x, y)$ que indica las regiones donde los valores de $I_a$ e $I_b$ deben permanecer fijos (es decir, iguales a $\tilde{I}_a$ y $\tilde{I}_b$).

Las actualizaciones se modifican para incluir la máscara:

$$
I_a^{t+1}(x, y) = (1 - M(x, y)) \cdot \left( I_a^t(x, y) + \alpha \left( \lambda \Delta I_a^t - \gamma (I_a^t - \tilde{I}_a) \right) \right) + M(x, y) \cdot \tilde{I}_a
$$

$$
I_b^{t+1}(x, y) = (1 - M(x, y)) \cdot \left( I_b^t(x, y) + \alpha \left( \lambda \Delta I_b^t - \gamma (I_b^t - \tilde{I}_b) \right) \right) + M(x, y) \cdot \tilde{I}_b
$$

Donde:
- $M(x, y) = 1$ en las regiones donde se deben mantener los valores de referencia.
- $M(x, y) = 0$ en las regiones donde se permite la difusión del color.

Sin esta imposición, el algoritmo perdería precisión y control, resultando en colores incorrectos o no deseados. Por lo tanto, esta restricción no solo es matemáticamente necesaria, sino también práctica para obtener resultados útiles y coherentes.
