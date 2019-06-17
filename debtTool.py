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

from PaymentPlan import *

parser = argparse.ArgumentParser(description =
    """This program analyzes compound interest loans to help manage payment
    plans."""
)

parser.add_argument('interest', type=float,
        help="The interest rate.")
parser.add_argument('compound_freq', type=int,
        help="Compound frequency per year.")
parser.add_argument('payment_freq', type=int,
        help="Payment frequency per year.")
parser.add_argument('--principal', '-P', type=float,
        help="How much is initially owed.")
parser.add_argument('--payment', '-p', type=float,
        help="How much is paid each cycle.")
parser.add_argument('--time-to-payoff', '-t', type=float,
        help="How long it takes to completely payoff all debts.")
parser.add_argument('--recommended', action='store_true',
        help="List the recommended payment plan.")
parser.add_argument('-r', '--return', type=float, default=0.25,
        dest="ret",
        help="""Constant for determining recommended minimum payment.
        Return on investment by lender. (default: %(default)s)""")
parser.add_argument('--graph-tradeoff', type=float, nargs=2,
        metavar=("MIN", "MAX"),
        help="""Graph tradeoffs given two unknowns.
        Requires the user to give the minimum and maximum x values.
        x values are in time to payoff or amount paid each cycle,
        with time to payoff having preference.""")
parser.add_argument('--graph-timeline', action='store_true',
        help="Graph the whole payment time line.")
args = parser.parse_args()

plan = PaymentPlan(args.interest, args.compound_freq, args.payment_freq,
        args.principal, args.payment, args.time_to_payoff)

if args.graph_tradeoff:
    (xMin, xMax) = args.graph_tradeoff
    (xlabel, ylabel, x, y) = plan.getGraphValues(xMin, xMax)

    plt.plot(x, y, color="blue")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
else:
    try:
        plan.fillInMissing()
        print(plan.strInfo())
    except NeedOneUnknown:
        print("Too many unknowns, please provide only one unknown value.")
    except PaymentTooLow:
        print("Payments are too low to ever pay off debt.")

    if plan.principal is not None and args.recommended:
        recPlan = plan.getPlanFromTotalOwed((1 + args.ret)*plan.principal)

        print("\nRecommended payment plan is")
        print(recPlan.strInfo())

    if args.graph_timeline:
        time = []
        owed = []
        paid = []

        time.append(0)
        owed.append(plan.principal)
        paid.append(0)
        while time[-1] < plan.timeToPayoff:
            time.append(time[-1] + 1/plan.payFreq)
            owed.append(plan.owed(time[-1]))
            paid.append(paid[-1] + plan.payment)

        l1 = "Amount Owed"
        l2 = "Total Amount Paid"

        plt.plot(time, owed, color="red", label=l1)
        plt.plot(time, paid, color="green", label=l2)

        plt.xlabel("Time (years)")
        plt.ylabel("Amount")
        plt.legend()

        plt.show()

