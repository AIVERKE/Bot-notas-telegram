import math

def taylor_expansion_e_x(x, n):
    # Inicializamos el resultado de la suma de la serie de Taylor
    approximation = 0
    # Iteramos desde 0 hasta n (orden de la serie)
    for i in range(n + 1):
        approximation += (x**i) / math.factorial(i)
    return approximation

# Parámetros
x_value = 2.5  # Valor donde queremos aproximar
for i in range (1, 8):
    # Cálculo de la aproximación usando la serie de Taylor
    approx_value = taylor_expansion_e_x(x_value, i)
    print(f"Aproximación de e^{x_value} usando la serie de Taylor de orden {i}: {approx_value}")


