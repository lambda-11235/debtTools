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

parser = argparse.ArgumentParser(description = "Analyze a compound interest payment method.")
parser.add_argument('principal', type=float,
        help="How much is initially owed.")
parser.add_argument('interest', type=float,
        help="The interest rate.")
parser.add_argument('freq', type=int,
        help="Compound frequency per year.")
parser.add_argument('payment', type=float,
        help="How much is paid each cycle.")
parser.add_argument('--graph', action='store_true',
        help="Graph owed and paid amounts versus time")
args = parser.parse_args()

totalTime = timeToPayOff(args.principal, args.interest, args.freq, args.payment)

if totalTime is None:
    pmin = paymentMinimum(args.principal, args.interest, args.freq)
    print("Payment will take an unbounded amount of time to pay off (must be greater than {:.2f}).".format(pmin))
    exit(1)

time = [t/args.freq for t in range(0, math.floor(args.freq*totalTime))]
time.append(totalTime)

owed = [amountOwed(args.principal, args.interest, args.freq, t, args.payment) for t in time]
paid = [args.payment*args.freq*t for t in time]

print("Will take {:.2f} years to pay off.".format(totalTime))
print("Total paid is {:.2f}, which is a {:.2f}% return on investment for lender.".format(
    paid[-1], (paid[-1] - args.principal)/args.principal*100))

if args.graph:
    plt.plot(time, owed, color="red")
    plt.plot(time, paid, color="green")
    plt.plot(time, len(time)*[args.principal], color="blue")

    plt.legend(["Owed", "Paid", "Principal"])
    plt.xlabel("Time (years)")
    plt.show()
