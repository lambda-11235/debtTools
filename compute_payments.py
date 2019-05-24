#!/usr/bin/env python

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


import argparse
import matplotlib.pyplot as plt
import math

from common import *

parser = argparse.ArgumentParser(description = "Run a test.")
parser.add_argument('principal', type=float,
        help="How much is initially owed.")
parser.add_argument('interest', type=float,
        help="The interest rate.")
parser.add_argument('freq', type=int,
        help="Compound frequency per year.")
parser.add_argument('time', type=float,
        help="How many years it will take to pay off debt in years.")
parser.add_argument('--delta', type=float, default=0.2,
        help="""Constant for determining recommended minimum payment.
        Higher values favor longer payoff periods.
        It can be estimated as (change in time)/(change in payment). (default: %(default)s)""")
parser.add_argument('--graph', action='store_true',
        help="Graphs time to payoff versus period payment amount.")
args = parser.parse_args()

P = args.principal
r = args.interest
freq = args.freq
t = args.time

p = paymentNeeded(args.principal, args.interest, args.freq, args.time)

time = timeToPayOff(args.principal, args.interest, args.freq, p)
if time is None:
    time = t

paid = freq*time*p

pmin = paymentMinimum(args.principal, args.interest, args.freq)

pRec = paymentRecommended(args.principal, args.interest, args.freq, args.delta)
tRec = timeToPayOff(args.principal, args.interest, args.freq, pRec)
paidRec = freq*tRec*pRec

print("Should pay {:.2f} to pay debt off in {:.2f} years.".format(p, time))
print("Total paid is {:.2f}, which is a {:.2f}% return on investment for lender.".format(
    paid, (paid - P)/P*100))
print("")
print("Minimum payment needed to maintain current debt is {:.2f}.".format(pmin))
print("Recommended minimum payment is {:.2f} for {:.2f} years for a total of {:.2f} ({:.2f}% return).".format(
    pRec, tRec, paidRec, (paidRec - P)/P*100))


if args.graph:
    timeUpper = math.ceil(args.freq*args.time) + 1
    timeLower = max(1, timeUpper//8)
    time = [t/args.freq for t in range(timeLower, timeUpper)]
    payment = [paymentNeeded(args.principal, args.interest, args.freq, t) for t in time]

    plt.plot(time, payment)
    plt.xlabel("Time to pay off debt (years)")
    plt.ylabel("Amount paid per period")
    plt.show()
