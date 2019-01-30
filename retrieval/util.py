from ext import cpphandler as handler
from .models import Image as Img, LikeInfo
from django.contrib.auth.models import User
from django.conf import settings
import datetime
import os
import cv2
import numpy as np
import process

_img_load_time = 0
_candice_load_time = 0
_px_data = np.ones((1, 1))
_imgs = []  # [[],[],[]]
_candice = []
_img_dats = []
_imgs_candi = {}
_img_load_done = False


def import_img():
    base_path = '/Users/ZTR/Desktop/Images/to_be_imported/'
    tg_bp = '/Users/ZTR/Documents/RBS_MEDIA/imgs/'
    tg_path = ['20170329/1722/',
               '20170329/1922/',
               '20170329/1924/',
               '20170329/2113/',
               '20170402/0917/',
               '20170402/1202/',
               '20170402/2003/',
               '20170402/2148/',
               '20170403/0418/',
               '20170403/0821/',
               '20170403/1929/',
               '20170403/2322/',
               '20170411/0939/',
               '20170411/1011/',
               '20170411/1829/',
               '20170411/1848/',
               '20170415/0012/',
               '20170415/0100/',
               '20170415/2111/',
               '20170415/2123/']
    paths = os.listdir(base_path)
    paths = paths[1:len(paths)]  # ['airplane', 'beer_mug', 'face,person']
    img_id = 1
    usr = User.objects.get(username='thestra')
    for p in paths:
        imgs = os.listdir(base_path + p + '/')  # ['001.jpg','002.png','003,pillow.jpg']
        for i in imgs:
            name, ext = os.path.splitext(i)
            print ext
            if ext != '.jpg' and ext != '.png' and ext != '.jpeg':
                continue
            tags = p.split(',')
            to_be_tag = name.split(',')
            if len(to_be_tag) > 1:
                tags += to_be_tag[1:len(to_be_tag)]
            dst_name = str(img_id) + ext
            tg = tg_path[img_id % len(tg_path)]
            src_im = cv2.imread(base_path + p + '/' + i)
            if not os.path.exists(tg_bp + tg):
                os.makedirs(tg_bp + tg)
            cv2.imwrite(tg_bp + tg + dst_name, src_im)
            if len(tags) == 1:
                Img.objects.create(id=img_id, path=tg, tag1=tags[0], uploaded_by=usr)
            elif len(tags) == 2:
                Img.objects.create(id=img_id, path=tg, tag1=tags[0], tag2=tags[1], uploaded_by=usr)
            elif len(tags) == 3:
                Img.objects.create(id=img_id, path=tg, tag1=tags[0], tag2=tags[1], tag3=tags[2], uploaded_by=usr)
            print p + '/' + i + ' >>> ' + tg + dst_name
            img_id += 1


# cvt imgs to skt
def convert_to_sketch():
    src_bp = '/Users/ZTR/Documents/RBS_MEDIA/imgs/'
    dst_bp = '/Users/ZTR/Documents/RBS_MEDIA/img_skts/'
    rps = ['20170329/',
           '20170402/',
           '20170403/',
           '20170411/',
           '20170415/']
    for rp in rps:
        sps = os.listdir(src_bp + rp)  # get ['0928','1022']
        sps = sps[1:len(sps)]
        for sp in sps:  # '0928'
            imgs = os.listdir(src_bp + rp + sp + '/')  # ['1.png', '2.jpg']
            imgs = imgs[1:len(imgs)]
            for img in imgs:
                # name, ext = os.path.splitext(img)
                src_p = src_bp + rp + sp + '/' + img  #
                dst_p = dst_bp + rp + sp + '/' + img
                if not os.path.exists(dst_bp + rp + sp + '/'):
                    os.makedirs(dst_bp + rp + sp + '/')
                i = cv2.imread(src_p)
                o = process.to_sketch(i)
                cv2.imwrite(dst_p, o)
                print dst_p


def import_feature():  # src_bp + 20170402/*/*.jpg  >>>  dst_bp + 20170402/1.dat
    src_bp = '/Users/ZTR/Documents/RBS_MEDIA/img_skts/'
    dst_bp = '/Users/ZTR/Documents/RBS_MEDIA/dats/img_dats/'
    src_rps = ['20170329/',
               '20170402/',
               '20170403/',
               '20170411/',
               '20170415/']
    for rp in src_rps:
        sps = os.listdir(src_bp + rp)  # get ['0928','1022']
        sps = sps[1:len(sps)]
        rtv = handler.Retriever()
        rtv.initIdx()
        dat_id = 1
        dst_p = dst_bp + rp + str(dat_id) + '.dat'  # dst_p + 20170329/2.dat
        if not os.path.exists(dst_bp + rp):
            os.makedirs(dst_bp + rp)
        for sp in sps:  # '0928'
            imgs = os.listdir(src_bp + rp + sp + '/')  # ['1.png', '2.jpg']
            imgs = imgs[1:len(imgs)]
            for img in imgs:
                src_p = src_bp + rp + sp + '/' + img  #
                rtv.insert(src_p, rp + sp + '/' + img)  # 20170203/0238/23.jpg
        rtv.save(dst_p)


def import_img1():
    base_path = '/Users/ZTR/Documents/256_ObjectCategories/'
    tg_bp = '/Users/ZTR/Documents/RBS_MEDIA/imgs/'
    tg_path = ['20170429/1722/',
               '20170429/1922/',
               '20170429/1924/',
               '20170429/2113/',
               '20170502/0917/',
               '20170502/1202/',
               '20170502/2003/',
               '20170502/2148/',
               '20170503/0418/',
               '20170503/0821/',
               '20170503/1929/',
               '20170503/2322/',
               '20170511/0939/',
               '20170511/1011/',
               '20170511/1829/',
               '20170511/1848/',
               '20170515/0012/',
               '20170515/0100/',
               '20170515/2111/',
               '20170515/2123/']
    paths = os.listdir(base_path)
    paths = paths[1:len(paths)]
    id = 1
    usr = User.objects.get(username='thestra')
    for p in paths:
        imgs = os.listdir(base_path + p + '/')
        for i in imgs:
            n, ext = os.path.splitext(i)
            print ext
            if ext != '.jpg' and ext != '.png' and ext != '.jpeg':
                continue
            tags = p.split('.')
            if tags[1] == 'hummingbird':
                if n[len(n) - 1] == 'f':
                    tags.append('flying_bird')
                elif n[len(n) - 1] == 's':
                    tags.append('standing_bird')
            elif tags[1] == 'people':
                if n[len(n) - 1] == 'i':
                    tags.append('sitting_person')
                elif n[len(n) - 1] == 'f':
                    tags.append('face')
            dst_name = str(id) + ext
            tg = tg_path[id % 20]
            date_st = tg.split('/')[0]
            y = int(date_st[0:4])
            m = int(date_st[4:6])
            d = int(date_st[6:8])
            print base_path + p + '/' + i
            print tg_bp + tg + dst_name
            src_im = cv2.imread(base_path + p + '/' + i)
            cv2.imwrite(tg_bp + tg + dst_name, src_im)
            if len(tags) == 2:
                Img.objects.create(id=id, path=tg, tag1=tags[1],
                                   uploaded_on=datetime.date(y, m, d), uploaded_by=usr)
            elif len(tags) == 3:
                Img.objects.create(id=id, path=tg, tag1=tags[1], tag2=tags[2],
                                   uploaded_on=datetime.date(y, m, d), uploaded_by=usr)
            elif len(tags) == 4:
                Img.objects.create(id=id, path=tg, tag1=tags[1], tag2=tags[2], tag3=tags[3],
                                   uploaded_on=datetime.date(y, m, d), uploaded_by=usr)
            print p + '/' + i + ' >>> ' + tg + dst_name
            id += 1


# to db,
def import_img2():
    ymds = [
        '20170110',
        '20170112',
        '20170113',
        '20170114',
        '20170115',
        '20170118',
        '20170119',
        '20170120',
        '20170122',
        '20170124',
        '20170127',
        '20170128',
        '20170201',
        '20170202',
        '20170204',
        '20170206',
        '20170207',
        '20170208',
        '20170210',
        '20170212',
        '20170213',
        '20170214',
        '20170215',
        '20170218',
        '20170219',
        '20170220',
        '20170222',
        '20170224',
        '20170227',
        '20170228',
    ] # 30
    hms = [
        '0010',
        '0529',
        '0748',
        '0932',
        '1004',
        '1531',
        '2040',
    ] # 7
    us = [
        User.objects.get(username='Sally'),
        User.objects.get(username='Jame'),
        User.objects.get(username='Maria'),
        User.objects.get(username='Dave'),
        User.objects.get(username='Sam'),
    ]

    im_bp = '/Users/ZTR/Desktop/Images/htmls/'
    sk_bp = '/Users/ZTR/Desktop/Images/imgs/'
    sk_ctl_ps = os.listdir(sk_bp)
    sk_ctl_ps = sk_ctl_ps[1:len(sk_ctl_ps)]
    f_n = 1
    for sk_ctl in sk_ctl_ps:
        sk_ps = os.listdir(sk_bp + sk_ctl)
        sk_ps = sk_ps[1:len(sk_ps)]
        for sk_p in sk_ps:
            ymd = ymds[f_n%30]
            hm = hms[f_n%7]
            u = us[f_n%5]
            y = int(ymd[0:4])
            m = int(ymd[4:6])
            d = int(ymd[6:8])
            count = Img.objects.count()
            Img.objects.create(id=count+1, path=ymd+'/'+hm+'/', tag1=sk_ctl,
                               uploaded_on=datetime.date(y, m, d), uploaded_by=u)

            im_ip = im_bp + sk_ctl + '_files' + '/' + sk_p
            im_op = settings.MEDIA_ROOT + '/' + ymd + '/' + hm + '/'
            name, ext = os.path.splitext(sk_p)
            if not os.path.exists(im_op):
                os.makedirs(im_op)
            im_op = im_op + str(f_n) + ext
            im = cv2.imread(im_ip)
            cv2.imwrite(im_op, im)

            sk_ip = sk_bp + sk_ctl + '/' + sk_p
            sk_op = settings.SKC_ROOT + '/' + ymd + '/' + hm + '/'
            if not os.path.exists(sk_op):
                os.makedirs(sk_op)
            sk_op = sk_op + str(f_n) + ext
            sk = cv2.imread(sk_ip)
            cv2.imwrite(sk_op, sk)

            f_n += 1
            print sk_ctl + ' , ' + sk_p


def import_f2():
    sk_1ps = os.listdir(settings.SKC_ROOT)
    if sk_1ps[0] == '.DS_Store':
        sk_1ps = sk_1ps[1:len(sk_1ps)]
    for sk_1p in sk_1ps:  # sk_1p: 20170202
        sk_2ps = os.listdir(settings.SKC_ROOT + '/' + sk_1p)
        if sk_2ps[0] == '.DS_Store':
            sk_2ps = sk_2ps[1:len(sk_2ps)]
        r_p = settings.IMG_DAT_ROOT + '/' + sk_1p
        if not os.path.exists(r_p):
            os.makedirs(r_p)
        r_p = r_p + '/1.dat'
        rtv = handler.Retriever()
        rtv.initIdx()
        for sk_2p in sk_2ps:  # sk_2p: 0402
            sk_ps = os.listdir(settings.SKC_ROOT + '/' + sk_1p + '/' + sk_2p)
            if sk_ps[0] == '.DS_Store':
                sk_ps = sk_ps[1:len(sk_ps)]
            for sk_p in sk_ps:
                sk_ip = settings.SKC_ROOT + '/' + sk_1p + '/' + sk_2p + '/' + sk_p
                rtv.insert(sk_ip, sk_1p + '/' + sk_2p + '/' + sk_p)
                print sk_1p + '/' + sk_2p + '/' + sk_p
        rtv.save(r_p)
        print 'feature: ' + sk_1p
    print 'done'


# retrieve imgs: get dat path and retrieve, return top 30
# load_time = 1: 2 img dats
# load_time > 1: 1 img dats
# no need of _imgs???
def get_img(px_data=_px_data, load_time=0):
    global _imgs
    global _img_load_time
    global _img_dats
    global _img_load_done
    imgs = []
    if load_time == 1:
        _img_load_done = False
        _img_load_time = 1
        dats = os.listdir(settings.IMG_DAT_ROOT)
        dats = dats[1:len(dats)]
        dats.reverse()  # ['3.dat','2.dat','1.dat']
        _img_dats = dats
        _imgs = []
        cv2.imwrite(settings.TEMP_SK_PATH, px_data)
        dat_p1 = settings.IMG_DAT_ROOT + '/' + dats[0] + '/1.dat'
        dat_p2 = settings.IMG_DAT_ROOT + '/' + dats[1] + '/1.dat'
        rs1 = retrieve(dat_p1, 100)
        rs2 = retrieve(dat_p2, 100)
        rs = dict(rs1, **rs2)
        result = sorted(rs.iteritems(), key=lambda d: d[1], reverse=True)
        for i in range(0, 30):
            if result[i][1] > 5000:
                imgs.append(result[i][0])
        _imgs.append(imgs)
    elif load_time == 0:
        # if len(_imgs) > 1 and _img_load_time < len(_imgs):  # unselect candi then load more
        #     _img_load_time += 1
        #     return _imgs[_img_load_time - 1]
        # elif _img_load_time >= len(_img_dats):
        #     return []
        # if _img_load_done:
        #     _img_load_time += 1
        #     return _imgs[_img_load_time - 1]
        # elif _img_load_time >= len(_img_dats):
        #     return []
        dats = _img_dats
        if len(dats) - 1 <= _img_load_time:
            imgs = []
            _img_load_done = True
        else:
            dat_p = settings.IMG_DAT_ROOT + '/' + dats[_img_load_time + 1] + '/1.dat'
            rs = retrieve(dat_p, 100)
            result = sorted(rs.iteritems(), key=lambda d: d[1], reverse=True)
            for i in range(0, 10):
                if result[i][1] > 3000:
                    imgs.append(result[i][0])
            _imgs.append(imgs)
        _img_load_time += 1
    elif load_time == -1:
        imgs = _imgs[0]
        _img_load_time = 1
    print 'img load done'
    return imgs


# retrieve candice: get dat
# 30 dats every time
# return top 5 of the sum of the value of the top 10 in each dat
# use _candice[6]
# if loadtime > 6: return _candice
# if loadtime == 1: reset _candice
# can trigger 2 request at the same time? yes! 1 for imgs, 1 for candice at one time
def get_1st_candice():
    global _candice
    candice = []  # [[c11,c12,c13,c14,c15],[c21,c22,c23,c24,c25]]
    dats = os.listdir(settings.SKC_DAT_ROOT)
    # dats = dats[1:len(dats)]  # ['airplane.dat', 'apple.dat']
    nrs = {}  # {'airplane':123.41, 'apple':181.12}
    for j in range(0, len(dats), 6):
        dat_p = settings.SKC_DAT_ROOT + '/' + dats[j]
        rs = retrieve(dat_p, 20)
        score = 0.  # the sum of this dat
        for r in rs:
            score += (float(rs[r]) / 100)
        name, ext = os.path.splitext(dats[j])
        nrs[name] = score
    result = sorted(nrs.iteritems(), key=lambda d: d[1], reverse=True)
    c = []
    for r in result:
        if r[1] < 1200:
            break
        c.append(r[0])
    candice.append(c)
    _candice = candice
    print "1st candi done"
    return candice[0]


def load_more_candice():
    global _candice
    dats = os.listdir(settings.SKC_DAT_ROOT)
    dats = dats[1:len(dats)]  # ['airplane.dat', 'apple.dat']
    for i in range(1, 6):
        nrs = {}  # {'airplane':123.41, 'apple':181.12}
        for j in range(i, len(dats), 6):
            dat_p = settings.SKC_DAT_ROOT + '/' + dats[j]
            rs = retrieve(dat_p, 20)
            score = 0.  # the sum of this dat
            for r in rs:
                score += (float(rs[r]) / 100)
            name, ext = os.path.splitext(dats[j])
            nrs[name] = score
        result = sorted(nrs.iteritems(), key=lambda d: d[1], reverse=True)
        c = []
        for r in result:
            if r[1] < 1200:
                break
            c.append(r[0])
        if len(c) != 0:
            _candice.append(c)
    print 'cd done' + str(len(_candice))


def switch_candice():
    global _candice_load_time
    global _candice
    result = []
    print "num:" + str(len(_candice))
    if _candice_load_time < len(_candice):
        _candice_load_time += 1
        if _candice_load_time == 6 or _candice_load_time == len(_candice):
            _candice_load_time = 0
        result = _candice[_candice_load_time]
        print result
        return result
    print result
    return result


# return imgs in the candi
# imgs with the candi in the _img 1st
# other imgs with the candi 2nd
def get_candi_img(candi):
    global _imgs
    global _imgs_candi
    if _imgs_candi.has_key(candi):
        return _imgs_candi[candi]
    imgs = []
    for im1 in _imgs:
        for im2 in im1:
            p = im2.split('/')
            l = p[len(p) - 1]
            name = l.split('.')[0]
            im_obj = Img.objects.get(id=name)
            if im_obj.tag1 is not None:
                if im_obj.tag1 in candi or candi in im_obj.tag1:
                    imgs.append(im2)
            if im_obj.tag2 is not None:
                if im_obj.tag2 in candi or candi in im_obj.tag2:
                    imgs.append(im2)
            if im_obj.tag3 is not None:
                if im_obj.tag3 in candi or candi in im_obj.tag3:
                    imgs.append(im2)
    _imgs_candi[candi] = imgs
    return imgs


def get_more_candi_img(candi):
    pass


def get_like_info(imgs, user):
    likes = [0] * len(imgs)
    for index, item in enumerate(imgs):
        p = item.split('/')
        l = p[len(p) - 1]
        name = l.split('.')[0]
        if LikeInfo.objects.filter(image_path_id=name, liked_by=user):
            likes[index] = 1
    return likes


def get_owners(imgs):
    owners = []
    for img in imgs:
        p = img.split('/')
        l = p[len(p) - 1]
        name = l.split('.')[0]
        img_obj = Img.objects.get(id=name)
        owner_id = img_obj.uploaded_by_id
        owner = User.objects.get(id=owner_id)
        owners.append(owner.username)
    return owners


def retrieve(dat_path, num):
    rtv = handler.Retriever()
    rtv.initIdx()
    rtv.load(dat_path)
    rtv.retrieve_sketch(settings.TEMP_SK_PATH, 'rtv')
    result = {}
    n = min(num, rtv.getResultSize())
    for i in range(0, n):
        result[rtv.getResultKey(i)] = rtv.getResultVal(i)
    return result
