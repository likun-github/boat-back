from django.db import models

class Team(models.Model):
    teamid=models.CharField(max_length=50,primary_key=True,verbose_name="团队id")
    teamname=models.CharField(max_length=50,verbose_name="团队名称")
    logo=models.ImageField(upload_to="teamlogo",verbose_name="团队logo")
    time = models.DateTimeField(auto_now_add=True, verbose_name="期表创建时间")
    class Meta:
        get_latest_by = "time"
class User(models.Model):
    openid=models.CharField(max_length=100,primary_key=True,verbose_name="唯一身份标识openid")
    name = models.CharField(max_length=30, verbose_name="姓名")
    picture = models.ImageField(upload_to="userpic", verbose_name="微信头像")
    CHOICE = (
        (0, "未实名认证"),
        (1, "实名认证通过"),
    )
    status = models.IntegerField(choices=CHOICE, verbose_name="是否完成实名认证")
    number=models.CharField(null=True, blank=True,max_length=15,verbose_name="学号")
    telephone=models.CharField(null=True, blank=True,max_length=11,verbose_name="联系方式")
    department=models.CharField(null=True, blank=True,max_length=20,verbose_name="学院")
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL,related_name="user")#外键连接名称

class Merchant(models.Model):
    merchantid=models.CharField(primary_key=True,max_length=10,verbose_name="商家id")
    name=models.CharField(max_length=30,verbose_name="商户名称")
    location = models.CharField(max_length=50, verbose_name="商家位置")
    latitude=models.FloatField(verbose_name="商家纬度")
    longitude=models.FloatField(verbose_name="商家精度")
    reputation = models.IntegerField(verbose_name="商家评分")
    CHOICE = (
        (1, "健身"),
        (2, "驾校"),
        (3, "考研"),
        (4, "小语种"),
    )
    type=models.IntegerField(choices=CHOICE,verbose_name="商户类别")
    logo = models.ImageField(upload_to="photo", verbose_name="商家logo")
    pic1=models.ImageField(upload_to="photo",verbose_name="商户照片1")
    pic2 = models.ImageField(upload_to="photo", verbose_name="商户照片2")
    pic3 = models.ImageField(upload_to="photo", verbose_name="商户照片3")
#不同学校对应不同的产品
class  Production(models.Model):
    productionid=models.IntegerField(primary_key=True,verbose_name="产品id")
    team=models.ForeignKey(Team,models.CASCADE,related_name="production")
    merchant=models.ForeignKey(Merchant,on_delete=models.CASCADE,related_name="production")
    name=models.CharField(max_length=20,verbose_name="产品名称")
    reputation=models.IntegerField(verbose_name="产品评分")
    CHOICE = (
        (1, "健身"),
        (2, "驾校"),
        (3, "考研"),
        (4, "小语种"),
    )
    introduciton=models.ImageField(upload_to="production",verbose_name="产品介绍")
    type = models.IntegerField(choices=CHOICE, verbose_name="产品类别")
    cutnumber = models.IntegerField(verbose_name="砍价人次")
    saveprie = models.FloatField(verbose_name="累计节省")

class Period(models.Model):
    periodid=models.CharField(primary_key=True,max_length=50,verbose_name="期表id")
    production=models.ForeignKey(Production,on_delete=models.CASCADE,related_name="period")
    starttime=models.DateTimeField(verbose_name="起始时间")
    endtime=models.DateTimeField(verbose_name="结束时间")
    startprice=models.IntegerField(verbose_name="初始价格")
    bottomprice=models.IntegerField(verbose_name="底价")
    CHOICE = (
        (1, "健身"),
        (2, "驾校"),
        (3, "考研"),
        (4, "小语种"),
    )
    type = models.IntegerField(choices=CHOICE, verbose_name="产品类别")
    time = models.DateTimeField(auto_now_add=True, verbose_name="期表创建时间")
    CHOICE = (
        (0, "已结束"),
        (1, "正在进行中"),
        (2, "未开始"),
    )
    status=models.IntegerField(choices=CHOICE,verbose_name="订单状态")
    cutprice = models.IntegerField(verbose_name="降价")
    number = models.IntegerField(verbose_name="参团人数")
    cutnumber = models.IntegerField(verbose_name="砍价人次")
    saveprie = models.FloatField(verbose_name="累计节省")
    class Meta:
        get_latest_by="time"



class Steam(models.Model):
    steamid=models.CharField(max_length=50,primary_key=True,verbose_name="拼团小团队id")
    time = models.DateTimeField(auto_now_add=True, verbose_name="团队创建时间")
    cutprice=models.FloatField(verbose_name="团队整体优惠价格")
    steamnumber=models.IntegerField(verbose_name="团队人数")
    master=models.ForeignKey(User,null=True, blank=True, on_delete=models.SET_NULL,related_name="steam")

class Comment(models.Model):
    commentid=models.CharField(max_length=50,primary_key=True,verbose_name="评论id")
    production=models.ForeignKey(Production,on_delete=models.CASCADE,related_name="comment")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment")
    context=models.CharField(max_length=200,verbose_name="评论")
    time=models.DateTimeField(auto_now_add=True,verbose_name="评论时间")
    CHOICE = (
        (0, "未核查"),
        (1, "已核查"),
    )
    status=models.IntegerField(default=0,choices=CHOICE,verbose_name="是否审核")



class Order(models.Model):
    orderid=models.CharField(max_length=50,primary_key=True,verbose_name="订单编号")
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="order")
    period=models.ForeignKey(Period,on_delete=models.CASCADE,related_name="order")
    production=models.ForeignKey(Production,on_delete=models.CASCADE,related_name="order")
    steam = models.ForeignKey(Steam, on_delete=models.CASCADE,related_name="order")
    CHOICE = (
        (0, "订单取消"),
        (1, "预付完成"),
        (2, "拼团完成"),
        (3, "支付完成"),
        (4, "订单完成"),
        (5, "评价完成"),
    )
    ordertime=models.DateTimeField(auto_now=True,verbose_name="订单生成时间")
    status=models.IntegerField(choices=CHOICE,default=1,verbose_name="状态")
    cutprice=models.FloatField(verbose_name="参团成员砍价")
    time1 = models.DateTimeField(auto_now_add=True, verbose_name="预付完成时间")
    time2 = models.DateTimeField(null=True, blank=True, verbose_name="拼团完成时间")
    time3 = models.DateTimeField(null=True, blank=True, verbose_name="支付完成时间")
    time4 = models.DateTimeField(null=True, blank=True, verbose_name="订单完成时间")
    time5 = models.DateTimeField(null=True, blank=True, verbose_name="评价完成时间")
    time6=models.DateTimeField(null=True, blank=True, verbose_name="订单取消时间")
    comment=models.ForeignKey(Comment,on_delete=models.CASCADE,related_name="order",null=True, blank=True)

class Cutting(models.Model):
    cutid=models.CharField(primary_key=True,max_length=50,verbose_name="砍价编号")
    audience = models.ForeignKey(User, on_delete=models.CASCADE,related_name="cutting")
    steam=models.ForeignKey(Steam,on_delete=models.CASCADE,related_name="cutting")
    cutprice=models.FloatField(verbose_name="砍价")
    time = models.DateTimeField(auto_now_add=True, verbose_name="砍价时间")








# Create your models here.
