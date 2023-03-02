from django.shortcuts import render,redirect
import mysql.connector as m
from datetime import date
# Create your views here.
l=[]
name=""
def ms(request):
  return render(request,"home.html")
def login(request):
  global l
  conn=m.connect(host="localhost",user="root",password="aditya",database="ms")
  c=conn.cursor()
  p=request.POST.get("pass")
  if p=="password":
    c.execute("create table if not exists bills(billno int primary key,cname varchar(20),phno varchar(20),date varchar(30),products varchar(300),gt int)")
    conn.commit()
    return render(request,"buy.html",{"items":len(l)})
  else:
    r="Invalid Password"
    return render(request,"home.html",{"err":r})
def gab(request):
  global l
  return render(request,"buy.html",{"items":len(l)})
def addm(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="ms")
  c=conn.cursor()
  c.execute("create table if not exists products(pid int primary key,name varchar(20),category varchar(20),quantity int,price int)")
  conn.commit()
  pid=AID("products")
  return render(request,"products.html",{"addmed":"1","pid":pid})
def addmed(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  pid=request.GET.get("pid")
  name=request.GET.get("name")
  category=request.GET.get("c")
  q=request.GET.get("qty")
  p=request.GET.get("p")
  c.execute("insert into products values({},'{}','{}',{},{})".format(int(pid),name,category,int(q),int(p)))
  conn.commit()
  return redirect("/addm")
def dem(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  c.execute("select * from products")
  f=c.fetchall()
  conn.commit()
  if f!=[]:
    return render(request,"products.html",{"dpro":"1","pro":f})
  else:
    return render(request,"products.html",{"dpro":"1","np":"No Product Available"})
def em(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  c.execute("select * from products")
  f=c.fetchall()
  conn.commit()
  if f!=[]:
    return render(request,"products.html",{"epro":"1","pro":f})
  else:
    return render(request,"products.html",{"epro":"1","np":"No Product Available"})
def editp(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  pid=request.GET.get("pid")
  c.execute("select * from products where pid={}".format(pid))
  f=c.fetchone()
  conn.commit()
  return render(request,"products.html",{"d":f,"epro":"1"})
def editpro(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  pid=request.GET.get("pid")
  name=request.GET.get("name")
  category=request.GET.get("c")
  q=request.GET.get("qty")
  p=request.GET.get("p")
  c.execute("update products set name='{}',category='{}',quantity={},price={} where pid={}".format(name,category,int(q),int(p),pid))
  conn.commit()
  return redirect("/em")
def deletepro(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  pid=request.GET.get("pid")
  c.execute("delete from products where pid={}".format(pid))
  conn.commit()
  return redirect("/dem")
def search(request):
  global l,name
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  name=request.GET.get("name")
  c.execute("select * from products where name like '{}%' or category like '{}%' ".format(name,name))
  a=c.fetchall()
  conn.commit()
  if a!=[]:
    return render(request,"buy.html",{"pro":a,"items":len(l)})
  else:
    return render(request,"buy.html",{"na":"Product Not Available","items":len(l)})
def add(request):
  global l,name
  if l==[]:
    s=1
  else:
    s=(l[len(l)-1][0])+1
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  i=request.GET.get("id")
  q=request.GET.get("qty")
  c.execute("select * from products where pid={}".format(i))
  f=c.fetchall()
  conn.commit()
  qty=f[0][3]
  if qty<int(q) and qty!=int(q):
    c.execute("select * from products where name like '{}%' or category like '{}%' ".format(name,name))
    f=c.fetchall()
    conn.commit()
    return render(request,"buy.html",{"pro":f,"items":len(l),"nq":"Quantity not Available"})
  else:
    p=(f[0][4])*int(q)
    l.append((s,f[0][1],f[0][4],q,p))
    ql=qty-int(q)
    c.execute("update products set quantity={} where pid={}".format(ql,i))
    conn.commit()
    c.execute("select * from products where name like '{}%' or category like '{}%' ".format(name,name))
    f=c.fetchall()
    conn.commit()
    return render(request,"buy.html",{"pro":f,"items":len(l)})
def checkout(request):
  global l
  s=0
  for i in l:
    s+=i[4]
  today=date.today()
  if l!=[]:
    return render(request,"details.html",{"l":l,"gt":s,"date":today})
  else:
    return render(request,"details.html",{"cm":"The cart is empty"})
def bill(request):
  global l
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  bn=AID("bills")
  d=[bn,request.GET.get("name"),request.GET.get("phno"),date.today()]
  s=0
  for i in l:
    s+=i[4]
  p=[]
  for i in l:
    p.append(i[1])
  p=",".join(p)
  c.execute("insert into bills values({},'{}','{}','{}','{}',{})".format(int(bn),d[1],d[2],d[3],p,s))
  conn.commit()
  t=tuple(l)
  l=[]
  return render(request,"bill.html",{"l":t,"gt":s,"i":d,"p":p})
def pbill(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  c.execute("select * from bills")
  f=c.fetchall()
  conn.commit()
  if f!=[]:
    return render(request,"pastbills.html",{"bill":f})
  else:
    return render(request,"pastbills.html",{"nb":"No Bills Generated"})
def searchbill(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  x=conn.cursor()
  c=request.GET.get("category")
  n=request.GET.get("s")
  if c!="products":
    x.execute("select * from bills where {} like '{}%'".format(c,n))
    f=x.fetchall()
    if f!=[]:
      return render(request,"pastbills.html",{"bill":f})
    else:
      return render(request,"pastbills.html",{"nb":"No Bills Found"})
  else:
    k=[]
    x.execute("select * from bills")
    f=x.fetchall()
    for i in f:
      j=i[4].split(',')
      for g in j:
        if g.startswith(n.upper()):
          k.append(i)
    if k!=[]:
      return render(request,"pastbills.html",{"bill":k})
    else:
      return render(request,"pastbills.html",{"nb":"No Bills Found"})
def remove(request):
  conn=m.connect(host="localhost",user="root",password="aditya",database="MS")
  c=conn.cursor()
  bn=request.GET.get("bn")
  c.execute("delete from bills where billno={}".format(bn))
  conn.commit()
  return redirect("/pbill")
def back(request):
  global l
  return render(request,"buy.html",{"items":0})
def AID(table):
  conn=m.connect(host="localhost",user="root",password="aditya",database="ms")
  c=conn.cursor()
  c.execute("select * from {}".format(table))
  a=c.fetchall()
  conn.commit()
  if a==[]:
    return 1
  else:
    return a[len(a)-1][0]+1
