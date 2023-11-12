from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.core.exceptions import ValidationError
from threading import Semaphore


BALANCE = 1000
lock = Semaphore()


def index(request):
    amount = request.GET.get('amount', None)
    if amount is None:
        template = loader.get_template('program/index.html')
        return HttpResponse(template.render({'balance': BALANCE}))
    try:
        msg = transfer(int(amount))
        return HttpResponse(msg)
    except (ValidationError, ValueError) as err:
        return HttpResponseBadRequest(err)


def transfer(amount):
    global BALANCE, lock
    if 0 <= amount <= BALANCE:
        lock.acquire()
        new_balance = BALANCE - amount
        transfered = amount
        BALANCE = new_balance
        lock.release()
        return f"Transfered {transfered}. Your new balance is {new_balance}"
    raise ValidationError("Amount is higher than the balance")

