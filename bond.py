import numpy as np
import pandas as pd


def discount_zc(p: float, y: float, m: float, coupon_freq: int):
    """
    p: principal in dollars
    y: annual market interest rate
    coupon_freq: times you get paid per year
    m: maturity in years
      e.g. if m = 2 and coupon_freq = 2 per year, then the maturity is 1 year
    """
    return p * (1 + y / coupon_freq) ** (-m * coupon_freq)


class FixedCouponBond:
    def __init__(
        self,
        coupon: float,
        principal: float,
        maturity: int,
        coupon_freq: int = 2,
    ):
        """
        maturity: maturity in years
        coupon: dollars payment per year
        coupon_freq: times you get paid per year, if coupon_freq = 2, then you get paid $coupon/2 twice a year
        """
        self._c = coupon
        self._p = principal
        self._m = maturity
        self._coupon_freq = coupon_freq

    @property
    def cash_flow(self) -> list[tuple[float, float]]:
        """
        returns list[(cash, time in years)]
        """
        return [
            (self._c / self._coupon_freq, t / self._coupon_freq)
            for t in range(1, self._coupon_freq * self._m + 1)
        ] + [(self._p, self._m)]

    def present_value(self, y: float):
        """
        y: annual market interest rate
        """
        return sum(
            discount_zc(cash, y, time, self._coupon_freq)
            for cash, time in self.cash_flow
        )

    def macaulay_duration(self, y: float):
        return sum(
            time * discount_zc(cash, y, time, self._coupon_freq)
            for cash, time in self.cash_flow
        ) / self.present_value(y)

    def modified_duration(self, y: float):
        """
        The modified duration is - 1 / PV * d(PV) / d(r)
        """
        return self.macaulay_duration(y) / (1 + y / self._coupon_freq)
