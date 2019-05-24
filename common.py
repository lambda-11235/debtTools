# Debt analysis tools for compound interest.
# Copyright (C) 2019  Taran Lynn
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from math import *

def amountOwed(principal, rate, freq, time, payment):
    """
    Amount owed after a certain time period.

    :principal: How much is initially owed.
    :rate:      The interest rate.
    :freq:      Compound frequency per year.
    :time:      How many years payments have been made for.
    :payment:   How much is paid each cycle.
    """
    a = (1 + rate/freq)
    return principal*a**(freq*time) - payment * freq*(a**(freq*time) - 1)/rate

def timeToPayOff(principal, rate, freq, payment):
    """
    The time it will take to pay off all debts given set payments.

    :principal: How much is initially owed.
    :rate:      The interest rate.
    :freq:      Compound frequency per year.
    :payment:   How much is paid each cycle.
    """
    a = (1 + rate/freq)
    tmp = freq*payment - rate*principal

    if tmp <= 0:
        # Time frame is to long to accurately calculate.
        return None
    else:
        return (log(freq*payment) - log(tmp))/(freq*log(a))

def paymentNeeded(principal, rate, freq, time):
    """
    The payment per period needed to pay off all debts in a given time span.

    :principal: How much is initially owed.
    :rate:      The interest rate.
    :freq:      Compound frequency per year.
    :time:      How many years payments will be made for.
    """
    a = 1 + rate/freq
    return rate*a**(freq*time)/(freq*(a**(freq*time) - 1)) * principal

def paymentMinimum(principal, rate, freq):
    """
    The absolute minimum payment that needs to be made to maintain current debt
    levels.

    :principal: How much is initially owed.
    :rate:      The interest rate.
    :freq:      Compound frequency per year.
    """
    return rate*principal/freq

def paymentFromTimeDelta(principal, rate, freq, delta):
    """
    The payment amount such that `d(time)/d(payment) = -delta`.

    :principal: How much is initially owed.
    :rate:      The interest rate.
    :freq:      Compound frequency per year.
    :delta:     The tradeoff fraction.
    """
    a = 1 + rate/freq
    tmp = rate*principal
    return (tmp + sqrt(tmp**2 + 4*tmp/(delta * log(a))))/(2*freq)

def paymentFromTotalDelta(principal, rate, freq, delta):
    """
    The payment amount such that `d(total paid)/d(principal) = delta`.

    :principal: How much is initially owed.
    :rate:      The interest rate.
    :freq:      Compound frequency per year.
    :delta:     The tradeoff fraction.
    """
    if delta <= 1:
        raise RuntimeError("delta must greater then 1, is {}".format(delta))

    return rate*delta/(freq*(delta - 1)) * principal
