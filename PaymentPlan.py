
from math import *


class NeedOneUnknown(Exception):
    pass

class NeedTwoUnknowns(Exception):
    pass

class NeedPrincipal(Exception):
    pass

class PaymentTooLow(Exception):
    pass


class PaymentPlan:
    def __init__(self, rate, compFreq, payFreq, principal=None,
            payment=None, timeToPayoff=None):
        self.rate = rate
        self.compFreq = compFreq
        self.payFreq = payFreq
        self.principal = principal
        self.payment = payment
        self.timeToPayoff = timeToPayoff

        self.a = 1 + self.rate/self.compFreq
        self.nm = self.compFreq/self.payFreq

        if self.timeToPayoff is not None:
            self.compounds = self.compFreq*self.timeToPayoff


        numOfNone = 0

        if principal is None:
            numOfNone += 1
        if payment is None:
            numOfNone += 1
        if timeToPayoff is None:
            numOfNone += 1

        self.numOfNone = numOfNone

    def fillInMissing(self):
        if self.numOfNone != 1:
            raise NeedOneUnknown()

        if self.principal is None:
            self.principal = self.computePrincipal(self.payment, self.timeToPayoff)
        elif self.payment is None:
            self.payment = self.computePayment(self.principal, self.timeToPayoff)
        elif self.timeToPayoff is None:
            self.timeToPayoff = self.computeTimeToPayoff(self.principal, self.payment)

        self.numOfNone = 0

    def computePrincipal(self, payment, timeToPayoff):
        (a, nm, nt) = self.getCommon(timeToPayoff)
        return (a**(-nt) - 1)/(1 - a**nm)*payment

    def computePayment(self, principal, timeToPayoff):
        (a, nm, nt) = self.getCommon(timeToPayoff)
        return (1 - a**nm)/(self.a**(-nt) - 1)*principal

    def computeTimeToPayoff(self, principal, payment):
        (a, nm) = self.getCommon()

        tmp = (1 - a**nm)*principal/payment + 1

        if tmp <= 0 or a <= 0:
            raise PaymentTooLow()

        return -log(tmp)/(self.compFreq*log(self.a))

    def getCommon(self, timeToPayoff = None):
        a = 1 + self.rate/self.compFreq
        nm = self.compFreq/self.payFreq

        if timeToPayoff is not None:
            nt = self.compFreq*timeToPayoff
            return (a, nm, nt)
        else:
            return (a, nm)

    def owed(self, time):
        (a, nm) = self.getCommon()
        nt = self.compFreq*time
        return a**nt*self.principal - self.payment*(1 - a**nt)/(1 - a**nm)

    def getMinimumPayment(self):
        if self.principal is None:
            raise NeedPrincipal()

        (a, nm) = self.getCommon()
        return (a**nm - 1)*self.principal

    def getPlanFromTotalOwed(self, owed):
        if self.principal is None:
            raise NeedPrincipal()

        (a, nm) = self.getCommon()
        payment = self.computePayment(self.principal, 1)
        last = 0

        while abs(payment - last) > 1.0e-6:
            last = payment

            f = payment - (1 - a**nm)/(a**(-nm*owed/payment) - 1) * self.principal

            df = (a**nm - 1)/(payment**2 * (a**(-nm*owed/payment) - 1)**2)
            df *= nm*owed*log(a)*a**(-nm*owed/payment)/payment
            df *= self.principal
            df = 1 - df

            payment -= f/df

        plan = PaymentPlan(self.rate, self.compFreq, self.payFreq,
            self.principal, payment, None)

        plan.fillInMissing()

        return plan

    def totalPaid(self):
        return self.payFreq*self.timeToPayoff*self.payment

    def returnOnInvestment(self):
        return self.totalPaid()/self.principal - 1

    def getGraphValues(self, xMin, xMax):
        if self.numOfNone != 2:
            raise NeedTwoUnknowns()

        x = []
        y = []

        # TODO: Come up with good values for x range
        if self.timeToPayoff is None:
            xStep = 1/self.payFreq
        else:
            xStep = (xMax - xMin)/1000

        if self.principal is not None:
            xlabel = "Time To Payoff"
            ylabel = "Payment"

            t = xMin
            while t < xMax:
                t += xStep
                x.append(t)
                y.append(self.computePayment(self.principal, t))
        elif self.payment is not None:
            xlabel = "Time To Payoff"
            ylabel = "Principal"

            t = xMin
            while t < xMax:
                t += xStep
                x.append(t)
                y.append(self.computePrincipal(self.payment, t))
        elif self.timeToPayoff is not None:
            xlabel = "Payment"
            ylabel = "Principal"

            p = xMin
            while p < xMax:
                p += xStep
                x.append(p)
                y.append(self.computePrincipal(p, self.timeToPayoff))

        return (xlabel, ylabel, x, y)

    def strInfo(self):
        s = ""
        s += "Interest: {:.2f}\n".format(self.rate)
        s += "Compound Frequency: {:.2f}\n".format(self.compFreq)
        s += "Payment Frequency: {:.2f}\n".format(self.payFreq)
        s += "Principal: {:.2f}\n".format(self.principal)
        s += "Payment: {:.2f}\n".format(self.payment)
        s += "Time to Payoff: {:.2f}\n".format(self.timeToPayoff)
        s += "Total Paid: {:.2f}\n".format(self.totalPaid())
        s += "Return on Investment: {:.2f}%".format(100*self.returnOnInvestment())
        return s
