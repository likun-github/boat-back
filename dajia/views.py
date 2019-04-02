from django.shortcuts import render
from django.utils import timezone
import pytz
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Count
from django.db.models import Max
from django.db.models import Sum
from .models import User,Team,Steam,Cutting
from .models import Order
from .models import Comment
from .models import Period
from .models import Production
from .models import Merchant
from dss.Serializer import serializer
import requests
import json
import random
import datetime
import  time
@csrf_exempt

def justtry(request):
    if request.method == 'GET':
        nowtime=timezone.now()
        order=Order.objects.first()
        order.time2=nowtime
        order.save()
        return JsonResponse({'success': True,'data':timezone.now()})

#登陆接口验证完成
#给定code,如果为注册用户，返回用户信息
#未注册，返回openid和默认teamid
def handle_upload_file(file,filename):
    path='userpic/'     #上传文件的保存路径，可以自己指定任意的路径
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path+filename,'wb+')as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return path+filename

@csrf_exempt
def login(request):
    if request.method == "POST":
        pic = handle_upload_file(request.FILES['file'], str(request.FILES['file']))
        code = request.POST.get('code')
        name = request.POST.get('name')
        appid = 'wx2b21ee85de8b10a9'
        appSecret = 'e3ce059551daa9fdd4657a6445d2b265'
        data = {
            'appid': appid,
            'secret': appSecret,
            'js_code': code,
            'grant_type': 'authorization_code',
        }
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (
            appid, appSecret, code)
        r = requests.get(url=url)
        response = r.json()
        openid = response['openid']
        account = User.objects.filter(openid=openid).exists()
        if account:
            newaccount = User.objects.get(openid=openid)
            back = serializer(newaccount)
            return JsonResponse(back)
        else:
            newaccount = User(openid=openid, name=name,picture=pic,status=0)
            newaccount.save()
            back = serializer(newaccount)
            return JsonResponse(back)



#实名认证验证通过
#未注册给定注册以及返回数据
#已注册返回该账户已注册
def verify(request):
    if request.method == 'GET':
        openid=request.GET.get('openid','')#openid
        teamid=request.GET.get('teamid','')#teamid
        name = request.GET.get('name', '')#姓名
        number = request.GET.get('number', '')  # 学号
        department = request.GET.get('department', '')#院系
        telephone = request.GET.get('telephone', '')#电话号码
        team=Team.objects.get(teamid=teamid)
        account = User.objects.filter(openid=openid,status=1).exists()
        if account:
            return JsonResponse("该账号已注册")
        else:
            account = User.objects.get(openid=openid)
            account.name = name
            account.number = number
            account.department = department
            account.telephone = telephone
            account.status = 1
            account.team = team
            account.save()
            return JsonResponse("true")


#首页认证
#成功,返回当前类别砍价最多以及参团人数最多
def home(request):
    if request.method == 'GET':
        pass
        teamid=request.GET.get('teamid','')
        home=Period.objects.filter(production__team_id=teamid,status=1).values('periodid','production','endtime','type', \
                                                                               'number')
        home=serializer(home)
        return JsonResponse(home)

#开始测试第二页接口
#给定teamid，type查询内容
#对datetime中用serializer库进行序列化用返回
#成功
def secondpage(request):
    if request.method == 'GET':
        type=request.GET.get('type','')
        teamid=request.GET.get('teamid','')
        #选择最近的一期
        nowtime=timezone.now()
        pass
        # peroidtoteams=Periodtoteam.objects.filter(type=type,team_id=teamid,period__status=1).values( "period__periodid", \
        #                                          "period__production__name","period__production__merchant__logo","period__production__merchant__latitude", \
        #                                          "period__production__merchant__longitude","period__production__merchant__location","period__production__reputation", \
        #                                         "period__startprice","maxcutprice","number","period__production__merchant__pic1")
        # data=serializer(peroidtoteams)
        # return JsonResponse({'success': True, 'data': data})


#详情页接口返回评论
#无足够评论信息，跳过
def thirdpage(request):
    if request.method == 'GET':
        periodid=request.GET.get('periodid','')
        period=Period.objects.get(periodid=periodid)
        comments=Comment.objects.filter(production_id=period.production_id,status=1).values("user__team__logo", \
                                                                                            "user__name","context","time").all()[0,5]
        comments=serializer(comments)
        return JsonResponse({'success': True, 'data': comments})
def scancomment(request):
    if request.method == 'GET':
        number=request.GET.get('number','')
        periodid = request.GET.get('periodid', '')
        period = Period.objects.get(periodid=periodid)
        comments = Comment.objects.filter(production_id=period.production_id, status=1).values("user__team__logo",  \
                                                                                               "user__name", "context", "time").all()[number, number+5]
        comments = serializer(comments)
        return JsonResponse({'success': True, 'data': comments})
#查询我的订单
#验证通过
def orderinformation(request):
    if request.method == 'GET':
        openid=request.GET.get('openid','')
        orders=Order.objects.filter(user_id=openid).values('orderid','period__endtime','status','production__name', \
                                                           'production__merchant__longitude', \
                                                           'production__merchant__latitude','production__merchant__logo', \
                                                           'production__reputation',"steam__cutprice" \
                                                           )
        orders=serializer(orders)
        return JsonResponse({'success':True,'data':orders})
#查询订单细节
#接口正常运行，细节的雕琢
def orderdetail(request):
    if request.method == 'GET':
        teamid=request.GET.get('teamid','')
        orderid=request.GET.get('orderid','')
        order=Order.objects.filter(orderid=orderid).values('production__merchant__logo','production__name', \
                                                           'production__merchant__latitude', \
                                                           'production__merchant__longitude', \
                                                           'production__reputation','period__number','period__status', \
                                                           'period__endtime', \
                                                           'period__startprice','period__cutprice','steam_id')
        onecut=Steam.objects.filter(steamid=order.steam_id).values('order__user__picture','order__user__name', \
                                                                   'order__cutprice')
        twocut =Steam.objects.filter(steamid=order.steam_id).values('cutting__audience__picture', \
                                                                    'cutting__audience__name','cutting__cutprice')
        order=serializer(order)
        onecut=serializer(onecut)
        twocut=serializer(twocut)
        return JsonResponse({"period":order,'oncut':onecut,'twocut':twocut})
#对取消接口进行验证
#取消接口验证完成
def cancel(request):
    if request.method == 'GET':
        orderid=request.GET.get('orderid','')
        order=Order.objects.get(orderid=orderid)
        order.status=0
        nowtime = timezone.now()
        order.time6 = nowtime
        order.save()
        return JsonResponse({'success':True})
#评论
#验证成功
def comment(request):
    if request.method == 'GET':
        orderid=request.GET.get('orderid','')
        context=request.GET.get('context','')

        order=Order.objects.get(orderid=orderid)
        user=order.user
        commentid=user.openid+order.period_id
        judge=Comment.objects.filter(commentid=commentid).exists()
        if judge:
            comment1=Comment.objects.get(commentid=commentid)
            comment1.context=context
            comment1.save()
        else:
            commenModel=Comment(commentid=commentid,context=context,user=user,order=order,status=0, \
                                production=order.production)
            nowtime = timezone.now()
            commenModel.save()
            order.time5 = nowtime
            order.comment=commenModel
            order.save()
        return JsonResponse({'success': True})
#给定openid,teamid,
#验证成功
def buyalone(request):
    if request.method =='GET':
        teamid = request.GET.get('teamid', '')
        openid = request.GET.get('openid', '')
        periodid = request.GET.get('periodid', '')
        period = Period.objects.get(periodid=periodid)
        user = User.objects.get(openid=openid)
        now = datetime.datetime.now()
        timeid = now.strftime('%Y%m%d%H%M%S')  # str类型,当前时间，年月日时分秒
        initial=period.startprice-period.bottomprice
        price = random.randint(int(0.1*initial), int(0.14*initial))  # 砍价金额
        steamid = openid + timeid
        orderid = openid + timeid
        steam = Steam(steamid=steamid, cutprice=price, steamnumber=1)
        period.number = period.number + 1
        #每人砍价
        if period.number<=100:
            cutprice = 0.001 * initial
            period.cutprice += cutprice
            print(period.cutprice)
        period.save()
        steam.save()
        order = Order(orderid=orderid, user=user, period=period, status=1, steam=steam, cutprice=price,
                      production=period.production)
        order.save()
        return JsonResponse({'success': True, 'reason': '参团成功', 'price': price})
def buytogether(request):
    teamid = request.GET.get('teamid', '')
    openid = request.GET.get('openid', '')
    steamid = request.GET.get('steamid', '')
    periodid = request.GET.get('periodid', '')
    period = Period.objects.get(periodid=periodid)
    user = User.objects.get(openid=openid)
    now = datetime.datetime.now()
    timeid = now.strftime('%Y%m%d%H%M%S')  # str类型,当前时间，年月日时分秒
    # 差价初值
    initial = period.startprice - period.bottomprice
    price = random.randint(int(0.1 * initial), int(0.14 * initial))  # 砍价金额
    orderid = openid + timeid
    steam = Steam.objects.get(steamid=steamid)

    if steam.steamnumber <= 4:
        steam.steamnumber = steam.steamnumber + 1
        steam.cutprice += price
        steam.save()
        order = Order(orderid=orderid, user=user, period=period, status=1, steam=steam, cutprice=price,
                      production=period.production)
        period.number = period.number + 1
        if period.number <= 100:
            cutprice = 0.0001 * initial
            period.cutprice += cutprice
        order.save()
        period.save()
        return JsonResponse({'success': True, 'reason': '参团成功', 'price': price})
    else:
        return JsonResponse({'success': False, 'reason': '团队人数已满'})



#团队外成员砍价
def cutprice(request):
    if request.method == 'GET':
        openid=request.GET.get('openid','')
        steamid=request.GET.get('steamid','')
        periodid=request.GET.get('period','')
        period=Period.objects.get(periodid=periodid)
        # 差价初值
        initial = period.startprice - period.bottomprice
        user=User.objects.get(openid=openid)
        steam=Steam.objects.get(steamid=steamid)
        if steam.cutprice<=0.7:
            price=random.randint(int(0.1*initial),int(0.7*initial))
        elif steam.cutprice<=0.8:
            price = random.randint(int(0.05 * initial), int(0.3 * initial))
        else:
            price = random.randint(int(0.01 * initial), int(0.1 * initial))
        price=price/100
        cutid=openid+steamid
        judge=Cutting.objects.filter(cutid=cutid).exists()
        if judge:
            return JsonResponse({'success': False})
        else:
            steam.cutprice += price
            steam.save()
            cutting = Cutting(cutid=cutid, audience=user, steam=steam, cutprice=price)
            cutting.save()
            return JsonResponse({'success': True, 'data': price})



#触发器正常运行
@receiver(post_save,sender=Period,dispatch_uid="period_save")
def period_save(sender,**kwargs):
    print("期表触发器正在运行")
    teams=Team.objects.all()
    period=Period.objects.latest()
    for team in teams:
        id=team.teamid+period.periodid
        # periodtoteam=Periodtoteam(Periodtoteamid=id,team=team,period=period,type=period.type,cutprice=0,maxcutprice=0,number=0)
        # periodtoteam.save()


@receiver(post_save,sender=Team,dispatch_uid="team_save")
def team_save(sender,**kwargs):
    print(kwargs['instance'].teamid)
    periods=Period.objects.all()
    team=Team.objects.latest()
    for period in periods:
        id = team.teamid + period.periodid
        # periodtoteam = Periodtoteam(Periodtoteamid=id, team=team, period=period, type=period.type, cutprice=0,
        #                              maxcutprice=0, number=0)
        # periodtoteam.save()











