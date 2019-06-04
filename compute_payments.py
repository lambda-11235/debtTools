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

parser = argparse.ArgumentParser(description = "Compute necessary payments for a compounded interest loan.")
parser.add_argument('principal', type=float,
        help="How much is initially owed.")
parser.add_argument('interest', type=float,
        help="The interest rate.")
parser.add_argument('freq', type=int,
        help="Compound frequency per year.")
parser.add_argument('-a', '--amount', type=float,
        help="Total amount wished to be paid off.")
parser.add_argument('-t', '--time', type=float,
        help="How many years it will take to pay off debt in years.")
parser.add_argument('-d', '--delta', type=float, default=2,
        help="""Constant for determining recommended minimum payment.
        Higher values favor higher total debt.
        It can be estimated as (change in total debt)/(change in principal). (default: %(default)s)""")
parser.add_argument('-g', '--graph', action='store_true',
        help="Graphs time to payoff versus period payment amount.")
args = parser.parse_args()


if args.amount is not None:
    minAmount = (1 + args.interest/args.freq)*args.principal

    if args.amount < minAmount:
        print("Error: amount paid off must be at least {:.2f}".format(minAmount))
        exit(1)

    p = paymentFromAmount(args.principal, args.interest, args.freq, args.amount)
elif args.time is not None:
    minTime = 1/args.freq

    if args.time < minTime:
        print("Error: time to pay off debt must be at least {:.2f}".format(minTime))
        exit(1)

    p = paymentFromTime(args.principal, args.interest, args.freq, args.time)

if args.amount is not None or args.time is not None:
    time = timeToPayOff(args.principal, args.interest, args.freq, p)
    paid = args.freq*time*p

    print("Should pay {:.2f} to pay debt off in {:.2f} years.".format(p, time))
    print("Total paid is {:.2f}, which is a {:.2f}% return on investment for lender.".format(
        paid, (paid - args.principal)/args.principal*100))
    print("")


pmin = paymentMinimum(args.principal, args.interest, args.freq)

pRec = paymentFromTotalDelta(args.principal, args.interest, args.freq, args.delta)
tRec = timeToPayOff(args.principal, args.interest, args.freq, pRec)
paidRec = args.freq*tRec*pRec

print("Minimum payment needed to maintain current debt is {:.2f}.".format(pmin))
print("Recommended minimum payment is {:.2f} for {:.2f} years for a total of {:.2f} ({:.2f}% return).".format(
    pRec, tRec, paidRec, (paidRec - args.principal)/args.principal*100))


if args.graph:
    if args.time is not None:
        timeUpper = args.time
    else:
        timeUpper = 2*tRec

    timeLower = args.freq if timeUpper > 1.0 else 1
    timeUpper = math.ceil(args.freq*timeUpper) + 1
    time = [t/args.freq for t in range(timeLower, timeUpper)]
    payment = [paymentFromTime(args.principal, args.interest, args.freq, t) for t in time]
    paid = [args.freq*t*p for (t, p) in zip(time, payment)]

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    l1 = "Amount paid per period"
    l2 = "Total amount paid"

    ax1.plot(time, payment, color="blue", label=l1)
    ax2.plot(time, paid, color="red", label=l2)

    ax1.set_xlabel("Time to pay off debt (years)")
    ax1.set_ylabel(l1)
    ax2.set_ylabel(l2)
    fig.legend()

    plt.show()
