
import argparse
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description = "Run a test.")
parser.add_argument('principal', type=float,
        help="How much is initially owed.")
parser.add_argument('payment', type=float,
        help="How much is paid each cycle.")
parser.add_argument('interest', type=float,
        help="The interest rate.")
parser.add_argument('n', type=int, default=12, nargs='?',
        help="Compound frequency per year.")
parser.add_argument('--pay-on-owed', type=float,
        metavar = "percentage",
        help="""Compute payments instead using a percentage of what is owed.
        payment gives the minimum payment that will be made.""")
parser.add_argument('--graph', action='store_true',
        help="Graph owed and paid amounts versus time")
args = parser.parse_args()

payOnOwed = args.pay_on_owed is not None
q = args.pay_on_owed

P = args.principal
p = args.payment
r = args.interest
n = args.n

divergent = False
years = None
nt = [0]
owed = [P]
paid = [0]

while not divergent and years is None:
    if payOnOwed:
        p = max(p, q*owed[-1])

    if owed[-1] < p:
        if years is None:
            years = (nt[-1] + 1)/n

        nextAmount = 0
        paid.append(paid[-1] + owed[-1])
    else:
        nextAmount = (owed[-1] - p)*(1 + r/n)
        paid.append(paid[-1] + p)

    if nextAmount > P:
        divergent = True

    nt.append(nt[-1] + 1)
    owed.append(nextAmount)

if divergent:
    print("Divergent amount owed, principal will never be paid off")
else:
    print("Will take {:.1f} years to pay off.".format(years))
    print("Total paid is {:.2f}, which is a {:.1f}% return on investment for lender.".format(
        paid[-1], (paid[-1] - P)/P*100))

    if args.graph:
        nt = np.array(nt)
        plt.plot(nt/n, owed)
        plt.plot(nt/n, paid)
        plt.plot(nt/n, len(nt)*[P])
        plt.legend(["Owed", "Paid", "Principal"])
        plt.show()
