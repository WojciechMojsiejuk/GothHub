from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr
import os

def show_function_plot(x_domain, y_domain, function_to_print):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Make data.
    x = np.arange(x_domain[0], x_domain[1], 0.1)
    y = np.arange(y_domain[0], y_domain[1], 0.1)
    x, y = np.meshgrid(x, y)
    expr = parse_expr(function_to_print)
    f = lambdify(symbols("x y"), expr, 'numpy')
    z = f(x,y)

    # Plot the surface.
    surf = ax.plot_surface(x, y, z, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    # ax.set_zlim(-1.0, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('F(X,Y)')
    fig.savefig(os.path.dirname(os.path.realpath(__file__))+"/function_plot.png")
    return fig


if __name__ == "__main__":
    print(show_function_plot(x_domain=[0, 1],y_domain=[0,3.14],function_to_print="x**2+sin(y)"))
