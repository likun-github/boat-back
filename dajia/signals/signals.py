from django.dispatch import Signal

from django.dispatch import receiver
from django.db.models.signals import post_save
from dajia.models import User,Order,Comment,Merchant,Team,Periodtoteam
from dajia.models import Period



@receiver(post_save,sender=Period,dispatch_uid="period_save")
def period_save(sender,**kwargs):
    print("期表触发器正在运行")
    teams=Team.objects.all()
    period=Period.get_latest_by()
    for team in teams:
        id=team.teamid+period.periodid
        periodtoteam=Periodtoteam(Periodtoteamid=id,team=team,period=period,type=period.type,cutprice=0,realprice=period.startprice,maxcutprice=0,number=0)
        periodtoteam.save()


@receiver(post_save,sender=Team,dispatch_uid="team_save")
def team_save(sender,**kwargs):
    periods=Period.objects.all()
    team=Team.get_latest_by()
    for period in periods:
        id = team.teamid + period.periodid
        periodtoteam = Periodtoteam(Periodtoteamid=id, team=team, period=period, type=period.type, cutprice=0,
                                    realprice=period.startprice, maxcutprice=0, number=0)
        periodtoteam.save()
