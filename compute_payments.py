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
args = parser.parse_args()

P = args.principal
r = args.interest
freq = args.freq
t = args.time

p = paymentNeeded(args.principal, args.interest, args.freq, args.time)
pmin = paymentMinimum(args.principal, args.interest, args.freq)

time = timeToPayOff(args.principal, args.interest, args.freq, p)
if time is None:
    time = t

paid = freq*time*p


print("Should pay {:.2f} to pay debt off in {:.2f} years.".format(p, time))
print("Minimum payment needed to maintain current debt is {:.2f}.".format(pmin))
print("Total paid is {:.2f}, which is a {:.2f}% return on investment for lender.".format(
        paid, (paid - P)/P*100))
