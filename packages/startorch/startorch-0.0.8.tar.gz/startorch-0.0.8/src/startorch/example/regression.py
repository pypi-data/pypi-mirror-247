from __future__ import annotations

__all__ = [
    "LinearRegressionExampleGenerator",
    "make_linear_regression",
    "get_uniform_weights",
]

from collections.abc import Sequence

import torch
from redcat import BatchDict, BatchedTensor
from redcat.utils.tensor import to_tensor
from torch import Tensor

from startorch import constants as ct
from startorch.example.base import BaseExampleGenerator
from startorch.example.utils import check_num_examples, check_std
from startorch.random import rand_normal, rand_uniform
from startorch.utils.seed import get_torch_generator


class LinearRegressionExampleGenerator(BaseExampleGenerator[BatchedTensor]):
    r"""Implements a regression example generator where the data are
    generated with an underlying linear model.

    The implementation is based on
    https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html

    Args:
    ----
        weights (``torch.Tensor`` of shape ``(feature_size,)`` or
            ``collections.abc.Sequence``): Specifies the linear
            weights in the underlying linear model.
        bias (float, optional): Specifies the bias term in the
            underlying linear model. Default: ``0.0``
        noise_std (float, optional): Specifies the standard deviation
            of the Gaussian noise. Default: ``0.0``

    Raises:
    ------
        ValueError if one of the parameters is not valid.

    Example usage:

    .. code-block:: pycon

        >>> from startorch.example import LinearRegression
        >>> generator = LinearRegression.create_uniform_weights()
        >>> generator
        LinearRegressionExampleGenerator(feature_size=100, bias=0.0, noise_std=0.0)
        >>> batch = generator.generate(batch_size=10)
        >>> batch
        BatchDict(
          (target): tensor([...], batch_dim=0)
          (feature): tensor([[...]], batch_dim=0)
        )
    """

    def __init__(
        self,
        weights: Tensor | Sequence[float],
        bias: float = 0.0,
        noise_std: float = 0.0,
    ) -> None:
        self._weights = to_tensor(weights)
        self._bias = bias

        check_std(noise_std, "noise_std")
        self._noise_std = float(noise_std)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(feature_size={self.feature_size:,}, "
            f"bias={self._bias}, noise_std={self._noise_std:,})"
        )

    @property
    def bias(self) -> float:
        r"""``float``: The bias of the underlying linear model."""
        return self._bias

    @property
    def feature_size(self) -> int:
        r"""``int``: The feature size."""
        return self._weights.shape[0]

    @property
    def noise_std(self) -> float:
        r"""``float``: The standard deviation of the Gaussian noise."""
        return self._noise_std

    @property
    def weights(self) -> Tensor:
        r"""``torch.Tensor``: The weights of the underlying linear
        model."""
        return self._weights

    def generate(
        self, batch_size: int = 1, rng: torch.Generator | None = None
    ) -> BatchDict[BatchedTensor]:
        return make_linear_regression(
            num_examples=batch_size,
            weights=self._weights,
            bias=self._bias,
            noise_std=self._noise_std,
            generator=rng,
        )

    @classmethod
    def create_uniform_weights(
        cls,
        feature_size: int = 100,
        informative_feature_size: int = 10,
        bias: float = 0.0,
        noise_std: float = 0.0,
        random_seed: int = 17532042831661189422,
    ) -> LinearRegressionExampleGenerator:
        # TODO: add documentation
        return cls(
            weights=get_uniform_weights(
                feature_size=feature_size,
                informative_feature_size=informative_feature_size,
                generator=get_torch_generator(random_seed),
            ),
            bias=bias,
            noise_std=noise_std,
        )


def make_linear_regression(
    weights: Tensor,
    bias: float = 0.0,
    num_examples: int = 100,
    noise_std: float = 0.0,
    generator: torch.Generator | None = None,
) -> BatchDict[BatchedTensor]:
    r"""Generates a regression dataset where the data are generated with
    an underlying linear model.

    The features are sampled from a Normal distribution.
    Then, the targets are generated by applying a random linear
    regression model.

    Args:
    ----
        weights (``torch.Tensor`` of shape ``(feature_size,)``):
            Specifies the linear weights in the underlying linear
            model.
        bias (float, optional): Specifies the bias term in the
            underlying linear model. Default: ``0.0``
        num_examples (int, optional): Specifies the number of examples
            to generate. Default: ``100``
        noise_std (float, optional): Specifies the standard deviation
            of the Gaussian noise. Default: ``0.0``
        generator (``torch.Generator`` or ``None``, optional):
            Specifies an optional random generator. Default: ``None``

    Returns:
    -------
        ``BatchDict``: A batch with two items:
            - ``'input'``: a ``BatchedTensor`` of type float and
                shape ``(num_examples, feature_size)``. This
                tensor represents the input features.
            - ``'target'``: a ``BatchedTensor`` of type float and
                shape ``(num_examples,)``. This tensor represents
                the targets.

    Raises:
    ------
        RuntimeError if one of the parameters is not valid.

    Example usage:

    .. code-block:: pycon

        >>> from startorch.example import make_linear_regression
        >>> batch = make_linear_regression(weights=torch.rand(10), num_examples=10)
        >>> batch
        BatchDict(
          (target): tensor([...], batch_dim=0)
          (feature): tensor([[...]], batch_dim=0)
        )
    """
    check_num_examples(num_examples)
    check_std(noise_std, "noise_std")
    feature_size = weights.shape[0]
    features = rand_normal(size=(num_examples, feature_size), generator=generator)
    targets = torch.mm(features, weights.view(feature_size, 1)) + bias
    if noise_std > 0.0:
        features += rand_normal(
            size=(num_examples, feature_size), std=noise_std, generator=generator
        )
    return BatchDict(
        {ct.TARGET: BatchedTensor(targets.flatten()), ct.FEATURE: BatchedTensor(features)}
    )


def get_uniform_weights(
    feature_size: int,
    informative_feature_size: int,
    generator: torch.Generator | None = None,
) -> Tensor:
    """Generates the weights of the linear combination used to generate
    the targets from the features.

    The weights of the informative features are sampled from a uniform
    distribution. The other weights are set to 0.
    This function was designed to be used with
    ``make_normal_regression``.

    Args:
    ----
        feature_size (int): Specifies the feature size i.e. the
            number of features.
        informative_feature_size (int): Specifies the number of
            informative features.
        generator (``torch.Generator`` or ``None``, optional):
            Specifies an optional random generator. Default: ``None``

    Returns:
    -------
        ``torch.Tensor`` of shape ``(feature_size,)``: The generated
            weights.

    Example usage:

    .. code-block:: pycon

        >>> from startorch.example.regression import get_uniform_weights
        >>> weights = get_uniform_weights(feature_size=10, informative_feature_size=5)
        >>> weights
        tensor([...])
    """
    informative_feature_size = min(feature_size, informative_feature_size)
    weights = torch.zeros(feature_size)
    weights[:informative_feature_size] = 100 * rand_uniform(
        size=(informative_feature_size,), generator=generator
    )
    permutation = torch.randperm(feature_size, generator=generator)
    return weights[permutation]
