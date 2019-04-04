from .models import Period
from .models import Order
from django.utils import timezone
import datetime
#未开始变为正在进行
def checkstatus1():
    #现在时间
    nowtime = timezone.now()
    periods = Period.objects.filter(status=2,starttime__lte=nowtime).all()
    for period in periods:
        period.status=1
        period.save()



#正在进行变为已经结束
#结束的order变为拼单完成
def checkstatus0():
    nowtime = timezone.now()
    periods = Period.objects.filter(status=1,endtime__lte=nowtime).all()
    for period in periods:
        period.status=0
        period.production.cutnumber+=period.cutnumber
        period.production.saveprie+=period.saveprie
        period.production.save()
        period.save()
        orders = Order.objects.filter(period_id=period.periodid).all()
        for order in orders:
            order.status=2
            order.time2=nowtime
            order.save()
