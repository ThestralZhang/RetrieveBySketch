from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm, LoginForm, UploadFileForm
from .models import Image as Img, LikeInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth, sessions
from django.conf import settings
from django.forms import ValidationError
from ext import cpphandler as handler
import random
import util
import wrapper as wp
import json
import os
import time
import datetime
from PIL import Image
import numpy as np
import cv2


# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        userinfo = json.loads(request.body)
        username = userinfo['username']
        email = userinfo['email']
        password = userinfo['password']
        if User.objects.filter(username=username):
            return JsonResponse({'msg': 'Username exists already.'})
        elif User.objects.filter(email=email):
            return JsonResponse({'msg': 'Email registered already.'})
        else:
            user = User.objects.create_user(username, email, password)
            user.is_superuser = False
            user.is_staff = True
            user.save()
            return JsonResponse({'result': 'success'})
    return render(request, 'register.html')


@csrf_exempt
def login(request):
    print '111'
    if request.method == 'POST':
        userinfo = json.loads(request.body)
        username = userinfo['username']
        password = userinfo['password']
        user = authenticate(username=username, password=password)
        print '222'
        if User.objects.filter(username=username):
            if user is not None:
                auth.login(request, user)
                # response = redirect('home')
                response = JsonResponse({'result': 'success'})
                response.set_cookie('username', username, 3600)
                print '333'
                return response
        print '444'
        return JsonResponse({'msg': 'Unknown user or wrong password'})
    else:
        print '555'
        return render(request, 'login.html')


def logout_view(request):
    auth.logout(request)
    return redirect('login')


@csrf_exempt
def handle_uploaded_file(f):
    file_name = ""
    try:
        path = settings.MEDIA_ROOT + time.strftime('/%Y%m%d/%H%M/')
        if not os.path.exists(path):
            os.makedirs(path)
            file_name = path + f.name
            destination = open(file_name, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
    except Exception, e:
        print e
    return file_name


@csrf_exempt
@wp.anti_resubmit(page_key='home')
def home(request):
    if not request.user.is_authenticated():  # if not login, return to login
        return HttpResponseRedirect('/login/')
    # if request.method == 'POST':  # if login, and upload
    #     form = UploadFileForm(request.POST, request.FILES)  # get the form
    #     if form.is_valid():  # valid
    #         file_name = handle_uploaded_file(request.FILES['img'])
    #         tag1 = form.cleaned_data['tag1']
    #         tag2 = form.cleaned_data['tag2']
    #         tag3 = form.cleaned_data['tag3']
    #         print tag1
    #         print type(request.FILES['img'])
    #         n_form = UploadFileForm()  # new form
    #         return render_to_response('home.html', {'up_form': n_form, 'user_name': str(request.user)})
    #     else:
    #         raise ValidationError(form.errors)
    # else:
    #     form = UploadFileForm()
    return render_to_response('home.html', {'user_name': str(request.user)})


def my_like(request):
    if not request.user.is_authenticated():  # if not login, return to login
        return HttpResponseRedirect('/login/')
    return render(request, 'my_like.html')


def my_up(request):
    if not request.user.is_authenticated():  # if not login, return to login
        return HttpResponseRedirect('/login/')
    return render(request, 'my_up.html')


# input: sketch data
# output: image urls and candice
# @wp.anti_resubmit(page_key='load_imgs')
def load_imgs(request):
    data = json.loads(request.body)
    w = data['width']
    h = data['height']
    ones = data['ones']
    px_data = np.ones((h, w), dtype=np.uint8) * 255
    for i in ones:
        px_data[i / w, i % w] = 0
    imgs = util.get_img(px_data, 1)
    likes = util.get_like_info(imgs, request.user)
    owners = util.get_owners(imgs)
    print 'ready to show'
    return JsonResponse({'imgs': imgs, 'likes': likes, 'owners': owners})


def load_1st_candice(request):
    candice = util.get_1st_candice()
    return JsonResponse({'candice': candice})


# mean time, load candice
def load_candice(request):
    util.load_more_candice()
    return JsonResponse({'result': 'done'})


# when click load more imgs
def load_more(request):
    imgs = util.get_img()
    likes = util.get_like_info(imgs, request.user)
    owners = util.get_owners(imgs)
    return JsonResponse({'imgs': imgs, 'likes': likes, 'owners': owners})


# when click other candice
def change_candice(request):
    candice = util.switch_candice()
    return JsonResponse({'candice': candice})


# when select some candi
def select_candi(request):
    candi = request.GET['candi']
    imgs = util.get_candi_img(candi)
    likes = util.get_like_info(imgs, request.user)
    owners = util.get_owners(imgs)
    return JsonResponse({'imgs': imgs, 'likes': likes, 'owners': owners})


# when unselect candi
def unselect_candi(request):
    imgs = util.get_img(load_time=-1)
    likes = util.get_like_info(imgs, request.user)
    owners = util.get_owners(imgs)
    return JsonResponse({'imgs': imgs, 'likes': likes, 'owners': owners})


# when click like or unlike
def like_img(request):
    act = request.GET['act']
    src = request.GET['src']
    p = src.split('/')
    l = p[len(p) - 1]
    name = l.split('.')[0]
    if act == 'like':
        if not LikeInfo.objects.filter(image_path_id=name, liked_by=request.user):
            LikeInfo.objects.create(image_path_id=name, liked_by=request.user)
    elif act == 'unlike':
        obj = LikeInfo.objects.get(image_path_id=name, liked_by=request.user)
        obj.delete()
    return HttpResponse()


def load_likes(request):
    imgs = []
    owners = []
    like_objs = LikeInfo.objects.filter(liked_by=request.user)
    for like_obj in like_objs:
        img_id = like_obj.image_path_id
        img_obj = Img.objects.get(id=img_id)
        path = img_obj.path  # 20170318/2112/
        owner_id = img_obj.uploaded_by_id
        fp = settings.MEDIA_ROOT + '/' + path + str(img_id)
        if os.path.exists(fp + '.jpg'):
            imgs.append(path + str(img_id) + '.jpg')
        elif os.path.exists(fp + '.jpeg'):
            imgs.append(path + str(img_id) + '.jpeg')
        elif os.path.exists(fp + '.png'):
            imgs.append(path + str(img_id) + '.png')
        owner = User.objects.get(id=owner_id)
        owners.append(owner.username)
    imgs.reverse()
    owners.reverse()
    # util.import_img2()
    # util.import_f2()

    return JsonResponse({'imgs': imgs, 'owners': owners})


# decide the path YYYYmmDD/HHMM/id.jpg
# into db
# into file
# decide feature file path
# extract feature
def upload_imgs(request):
    if request.method == "POST":
        img = request.FILES.get('img')
        tag1 = request.POST.get('tag1')
        tag2 = request.POST.get('tag2')
        tag3 = request.POST.get('tag3')
        t = datetime.datetime.now()
        y = str(t.year)
        mo = str(t.month) if t.month > 9 else '0' + str(t.month)
        d = str(t.day) if t.day > 9 else '0' + str(t.day)
        h = str(t.hour + 8) if t.hour > 1 else '0' + str(t.hour + 8)
        mi = str(t.minute) if t.minute > 9 else '0' + str(t.minute)
        time_stamp1 = y + mo + d + '/'
        time_stamp2 = h + mi + '/'
        path = settings.MEDIA_ROOT + '/' + time_stamp1 + time_stamp2
        if not os.path.exists(path):
            os.makedirs(path)
        name, ext = os.path.splitext(img.name)
        img_id = Img.objects.count() + 1
        name = str(img_id) + ext
        if len(tag1) == 0:
            t1 = None
        else:
            t1 = tag1
        if len(tag2) == 0:
            t2 = None
        else:
            t2 = tag2
        if len(tag3) == 0:
            t3 = None
        else:
            t3 = tag3
        img_obj = Img(id=img_id, path=time_stamp1+time_stamp2, tag1=t1, tag2=t2, tag3=t3,
                      uploaded_by=request.user, uploaded_on=datetime.date(t.year, t.month, t.day))
        img_obj.save()
        with open(path+name, "wb") as f:
            for chunk in img.chunks():
                f.write(chunk)
        f.close()
        dat_path = settings.IMG_DAT_ROOT + '/' + time_stamp1
        if not os.path.exists(dat_path):
            os.makedirs(dat_path)
        dat_path += '1.dat'
        rtv = handler.Retriever()
        rtv.initIdx()
        if os.path.exists(dat_path):
            rtv.load(dat_path)
        rtv.insert(path + name, time_stamp1 + time_stamp2 + name)  # 20170203/0238/23.jpg
        rtv.save(dat_path)
        return HttpResponse("ok")


def load_ups(request):
    imgs = []  # [[p,d],[],[]]
    img_objs = Img.objects.filter(uploaded_by=request.user)
    for obj in img_objs:
        img = []
        path = obj.path + str(obj.id)
        fp = settings.MEDIA_ROOT + '/' + path  # root/20170102/2321/34
        if os.path.exists(fp + '.jpg'):
            img.append(path + '.jpg')
        elif os.path.exists(fp + '.jpeg'):
            img.append(path + '.jpeg')
        elif os.path.exists(fp + '.png'):
            img.append(path + '.png')
        ds = obj.path.split('/')[0]
        ds = ds[0:4] + '.' + ds[4:6] + '.' + ds[6:8]
        img.append(ds)
        imgs.append(img)
    imgs = sorted(imgs, key=lambda d: d[1], reverse=True)
    return JsonResponse({'imgs': imgs})


# 2 rp -> 3 np -> 10 p
def load_home(request):
    count = Img.objects.count()
    indice = range(1, count+1)
    random.shuffle(indice)
    indice = indice[0:50]
    imgs = []
    for idx in indice:
        obj = Img.objects.get(id=idx)
        path = obj.path + str(obj.id)
        fp = settings.MEDIA_ROOT + '/' + path  # root/20170102/2321/34
        if os.path.exists(fp + '.jpg'):
            imgs.append(path + '.jpg')
        elif os.path.exists(fp + '.jpeg'):
            imgs.append(path + '.jpeg')
        elif os.path.exists(fp + '.png'):
            imgs.append(path + '.png')
    likes = util.get_like_info(imgs, request.user)
    owners = util.get_owners(imgs)
    return JsonResponse({'imgs': imgs, 'likes': likes, 'owners': owners})


# def tt():
#     objs = Img.objects.all()
#     u1 = User.objects.get(username='Jame')
#     u2 = User.objects.get(username='Maria')
#     for obj in objs:
#         path = obj.path
#         ds = path.split('/')[0]
#         y = int(ds[0:4])
#         m = int(ds[4:6])
#         d = int(ds[6:8])
#         obj.uploaded_on = datetime.date(y, m, d)
#         if obj.id%13 == 2:
#             obj.uploaded_by = u1
#         elif obj.id%13 == 7:
#             obj.uploaded_by = u2
#         obj.save()
