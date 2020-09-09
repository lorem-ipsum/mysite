from django.shortcuts import render

from django.http import HttpResponse, JsonResponse

from .models import Movie, Character, Comment

from django.db.models import Q

import json
import time


def movies(request):
    if(request.method == 'GET'):
        ms = Movie.objects.filter().order_by('-star')
        movielist = []
        page = int(request.GET['page'])
        print(page)
        i = 24*(page-1)
        while i < 24*page and i < ms.count():
            movielist.append(ms[i].mid)
            i += 1
        return JsonResponse({"movielist": movielist, "totalPageNum": ms.count()})


def movie(request, mid):
    if(request.method == 'GET'):
        m = Movie.objects.get(mid=mid)
        relatedchars = []
        for char in m.characters.all():
            relatedchars.append(char.cid)
        comments = []
        for cm in m.comment_set.all():
            comments.append(cm.comment_text)
        resp = {
            "mid": m.mid,
            "title": m.title,
            "mainPicSrc": m.mainPicSrc,
            "star": m.star,
            "summary": m.summary,
            "characters": relatedchars,
            "comments": comments
        }
        return JsonResponse(resp)


def characters(request):
    if(request.method == 'GET'):
        cs = Character.objects.filter()
        characterlist = []
        page = int(request.GET['page'])
        print(page)
        i = 24*(page-1)
        while i < 24*page and i < cs.count():
            characterlist.append(cs[i].cid)
            i += 1
        return JsonResponse({"characterlist": characterlist, "totalPageNum": cs.count()})


def character(request, cid):
    if(request.method == 'GET'):
        c = Character.objects.get(cid=cid)
        relatedmovies = []
        relatedcharsdict = dict()
        relatedchars = []
        for movie in c.charsmovies.all():
            relatedmovies.append(movie.mid)
        for movie in relatedmovies:
            for char in Movie.objects.get(mid=movie).characters.all():
                if char.cid == cid:
                    continue
                if char.cid in relatedcharsdict:
                    relatedcharsdict[char.cid] += 1
                else:
                    relatedcharsdict[char.cid] = 1
        for char in relatedcharsdict:
            relatedchars.append([char, relatedcharsdict[char]])
        relatedchars.sort(key=lambda char: -char[1])
        resp = {
            "cid": c.cid,
            "name": c.name,
            "mainPicSrc": c.mainPicSrc,
            "description": c.description,
            "relatedmovies": relatedmovies,
            "relatedchars": relatedchars
        }

        return JsonResponse(resp)


def comment(request, cmid):
    if(request.method == 'GET'):
        cm = Comment.objects.get(id=cmid)
        comment_text = cm.comment_text
        mid = cm.movie.mid
        return JsonResponse({"comment_text": comment_text, "mid": mid})


def search(request):
    if(request.method == 'GET'):
        time_start = time.time()
        item = request.GET['item']
        key = request.GET['key']
        print(item, key)
        if item == 'movie':
            ms = Movie.objects.filter(Q(title__contains=key) | Q(
                characters__name__contains=key)).distinct().order_by('-star')
            movielist = []
            page = int(request.GET['page'])
            print(page)
            i = 24*(page-1)
            while i < 24*page and i < ms.count():
                movielist.append(ms[i].mid)
                i += 1
            print(movielist)
            time_end = time.time()
            return JsonResponse({"movielist": movielist, "totalPageNum": ms.count(), "time": time_end-time_start})
        if item == 'character':
            cs = Character.objects.filter(Q(name__contains=key) | Q(
                charsmovies__title__contains=key)).distinct()
            characterlist = []
            page = int(request.GET['page'])
            print(page)
            i = 24*(page-1)
            while i < 24*page and i < cs.count():
                characterlist.append(cs[i].cid)
                i += 1
            print('characterlist', characterlist)
            time_end = time.time()
            return JsonResponse({"characterlist": characterlist, "totalPageNum": cs.count(), "time": time_end-time_start})
        if item == 'comment':
            cms = Comment.objects.filter(
                Q(comment_text__contains=key)).distinct()
            commentlist = []
            page = int(request.GET['page'])
            print(page)
            i = 24*(page-1)
            while i < 24*page and i < cms.count():
                commentlist.append(cms[i].id)
                i += 1
            print(commentlist)
            time_end = time.time()
            return JsonResponse({"commentlist": commentlist, "totalPageNum": cms.count(), "time": time_end-time_start})
