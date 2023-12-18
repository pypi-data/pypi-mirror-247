from __future__ import annotations

__all__ = ["PoissonSequenceGenerator", "RandPoissonSequenceGenerator"]


import torch
from coola.utils import str_indent, str_mapping
from redcat import BatchedTensorSeq
from torch import Generator

from startorch.random import rand_poisson
from startorch.sequence.base import BaseSequenceGenerator, setup_sequence_generator
from startorch.sequence.constant import ConstantSequenceGenerator
from startorch.utils.conversion import to_tuple


class PoissonSequenceGenerator(BaseSequenceGenerator):
    r"""Implements a class to generate sequence by sampling values from a
    Poisson distribution.

    The rates of the Poisson distribution are generated by the rate
    generator. The rate generator should return the rate for each value
    in the sequence. The rate values should be greater than 0.

    Args:
    ----
        rate (``BaseSequenceGenerator`` or dict): Specifies the
            rate generator or its configuration. The rate generator
            should return valid rate values.

    Example usage:

    .. code-block:: pycon

        >>> from startorch.sequence import RandUniform, Poisson
        >>> generator = Poisson(rate=RandUniform(low=1.0, high=2.0))
        >>> generator
        PoissonSequenceGenerator(
          (rate): RandUniformSequenceGenerator(low=1.0, high=2.0, feature_size=(1,))
        )
        >>> generator.generate(seq_len=6, batch_size=2)
        tensor([[...]], batch_dim=0, seq_dim=1)
    """

    def __init__(self, rate: BaseSequenceGenerator | dict) -> None:
        super().__init__()
        self._rate = setup_sequence_generator(rate)

    def __repr__(self) -> str:
        args = str_indent(str_mapping({"rate": self._rate}))
        return f"{self.__class__.__qualname__}(\n  {args}\n)"

    def generate(
        self, seq_len: int, batch_size: int = 1, rng: Generator | None = None
    ) -> BatchedTensorSeq:
        return BatchedTensorSeq(
            torch.poisson(
                self._rate.generate(seq_len=seq_len, batch_size=batch_size, rng=rng).data,
                generator=rng,
            )
        )

    @classmethod
    def generate_uniform_rate(
        cls,
        min_rate: float = 0.01,
        max_rate: float = 1.0,
        feature_size: tuple[int, ...] | list[int] | int = 1,
    ) -> PoissonSequenceGenerator:
        r"""Implements a sequence generator where the rates of the
        Poisson distribution are sampled from a uniform distribution.

        Args:
        ----
            min_rate (float, optional): Specifies the minimum rate
                value. Default: ``0.01``
            max_rate (float, optional): Specifies the maximum rate
                value. Default: ``1.0``
            feature_size (tuple or list or int, optional): Specifies the
                feature size. Default: ``1``

        Returns:
            ``Poisson``: A sequence generator
                where the rates of the Poisson distribution are
                sampled from a uniform distribution
                (``UniformConstantSequenceGenerator``).
        """
        # The import is here to do not generate circular dependencies
        from startorch.sequence.uniform import RandUniformSequenceGenerator

        return cls(
            rate=ConstantSequenceGenerator(
                generator=RandUniformSequenceGenerator(
                    low=min_rate,
                    high=max_rate,
                    feature_size=feature_size,
                )
            ),
        )


class RandPoissonSequenceGenerator(BaseSequenceGenerator):
    r"""Implements a class to generate sequence by sampling values from a
    Poisson distribution.

    Args:
    ----
        rate (float, optional): Specifies the rate of the Poisson
            distribution. This value has to be greater than 0.
            Default: ``1.0``
        feature_size (tuple or list or int, optional): Specifies the
            feature size. Default: ``1``

    Raises:
    ------
        ValueError if ``rate`` is not a positive number.

    Example usage:

    .. code-block:: pycon

        >>> from startorch.sequence import RandPoisson
        >>> generator = RandPoisson(rate=1.0)
        >>> generator
        RandPoissonSequenceGenerator(rate=1.0, feature_size=(1,))
        >>> generator.generate(seq_len=6, batch_size=2)
        tensor([[...]], batch_dim=0, seq_dim=1)
    """

    def __init__(
        self,
        rate: float = 1.0,
        feature_size: tuple[int, ...] | list[int] | int = 1,
    ) -> None:
        super().__init__()
        if rate <= 0:
            raise ValueError(f"rate has to be greater than 0 (received: {rate})")
        self._rate = float(rate)
        self._feature_size = to_tuple(feature_size)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__qualname__}(rate={self._rate}, feature_size={self._feature_size})"
        )

    def generate(
        self, seq_len: int, batch_size: int = 1, rng: Generator | None = None
    ) -> BatchedTensorSeq:
        return BatchedTensorSeq(
            rand_poisson(
                size=(batch_size, seq_len) + self._feature_size,
                rate=self._rate,
                generator=rng,
            )
        )
