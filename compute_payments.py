
import argparse
import math

parser = argparse.ArgumentParser(description = "Run a test.")
parser.add_argument('principal', type=float,
        help="How much is initially owed.")
parser.add_argument('interest', type=float,
        help="The interest rate.")
parser.add_argument('time', type=float,
        help="How many years it will take to pay off debt in years.")
parser.add_argument('n', type=int, default=12, nargs='?',
        help="Compound frequency per year.")
args = parser.parse_args()

P = args.principal
r = args.interest
n = args.n
t = args.time

# Calculate payment needed.
a = 1 + r/n
p = r*P/(n*(a - a**(1 - n*t)))


# Calculate total payments.
owed = P
paid = 0
stuck = False
while p < owed:
    last = owed
    owed = (owed - p)*a
    paid += p
    if last == owed:
        stuck = True
        break
paid += owed

if stuck:
    paid = n*t*p


print("Should pay {:.2f} to pay debt off in {:.1f} years.".format(p, t))
print("Total paid is {:.2f}, which is a {:.1f}% return on investment for lender.".format(
        paid, (paid - P)/P*100))
