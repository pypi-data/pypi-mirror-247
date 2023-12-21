import numpy as np
from structured_light.structures import hg, lg, diagonal_hg


def fixed_order_basis(x, y, w0, order, basis='hg'):
    """
    Compute the fixed-order basis functions for a given set of coordinates.

    Args:
        x (array_like): x-coordinates of the points.
        y (array_like): y-coordinates of the points.
        w0 (float): Waist parameter.
        order (int): Order of the basis functions.
        basis (str, optional): Type of basis functions to compute. 
            Possible values are 'lg', 'hg', 'diagonal_hg'. 
            Defaults to 'hg'.

    Returns:
        (array_like): An array of basis functions.

    Raises:
        AssertionError: If an invalid basis name is provided.

    """
    assert basis in (
        'lg', 'hg', 'diagonal_hg'), "Known 'basis_name' are 'lg', 'hg', 'diagonal_hg'. Got %s." % basis

    if basis == 'lg':
        basis = np.array([lg(x, y, int(np.minimum(k, order-k)), 2*k - order, w0)
                          for k in range(order+1)])
    elif basis == 'hg':
        basis = np.array([hg(x, y, order-k, k, w0) for k in range(order+1)])
    elif basis == 'diagonal_hg':
        basis = np.array([diagonal_hg(x, y, order-k, k, w0)
                         for k in range(order+1)])

    return basis


def linear_combination(coefficients, basis):
    """Calculate a linear combinantion

    Args:
        coefficients (list): list containing the coefficients
        basis (list): list containing the basis elements

    Returns:
        (array_like): array defined by the linear combination
    """
    return np.sum([c * b for (c, b) in zip(coefficients, basis)], axis=0)
