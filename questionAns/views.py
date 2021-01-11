from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as s
from .models import *
import uuid
import json, os
import traceback, sys
from .tfidf import rank_documents
import nltk
from .helppkg import get_keyword

nltk.download("wordnet")
# Create your views here.


class User_id(APIView):

    def get(self, request, *args, **kwargs):
        
        return Response({"status":"working"})
    
    def post(self, request, *args, **kwargs):
        raw_data = self.request.data
        try:
            username = raw_data["username"]
            key = str(uuid.uuid1().hex)
            user_type = raw_data["user_type"]
            UserData.objects.create(user_name=username,user_id=key,user_type=user_type).save()
            status = s.HTTP_201_CREATED
            response={
                "user_name":username,
                "key":key
            }
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            status = s.HTTP_500_INTERNAL_SERVER_ERROR
            response={"username":"internal server error"}

        return Response(response,status=status)


class ChatAnswer(APIView):

    def post(self, request, *args, **kwargs):
        try:
            country_name = request.GET[ 'cnt' ]
            print(">>>>>>>>>>>",country_name)
            woner_data = json.loads(open(os.getcwd()+"/questionAns/support_file/woner.json","r").read())
            tenet_data = json.loads(open(os.getcwd()+"/questionAns/support_file/tenet.json","r").read())
            raw_data=self.request.data
            question=raw_data["question"]
            key=raw_data["key"]
            dataObj = UserData.objects.get(user_id=key)

            if str(dataObj.user_type) == "woner":
                try:
                    data = list(filter(lambda answer: answer['question'] == question, woner_data))[0]["response"]
                    question_ans = True
                except:
                    data="unknown answer"
                    question_ans = False
            
            if str(dataObj.user_type) == "tenet":
                try:
                    data = list(filter(lambda answer: answer['question'] == question, tenet_data))[0]["response"]
                    question_ans = True
                except:
                    data="unknown answer"
                    question_ans = False
                    
            Chat.objects.create( user_id = dataObj, question=question,question_ans = question_ans, answer = data )
            response = {"answer":data}

        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            status = s.HTTP_500_INTERNAL_SERVER_ERROR
            response={"error":"internal server error"}
        return Response({"status":response})


def index(request):
    woner_data = json.loads(open(os.getcwd()+"/questionAns/support_file/woner.json","r").read())
    tenet_data = json.loads(open(os.getcwd()+"/questionAns/support_file/tenet.json","r").read())
    if request.method == "POST":
        try:
            msg = request.POST.get("msg")
            
            user_name=request.POST.get("username")
            
            try:
                dataObj = UserData.objects.get(user_name=request.session["username"])
            except:
                dataObj = None
            if dataObj ==None:
                if user_name:
                    dataObj = UserData.objects.get(user_name=user_name)
                    request.session["username"]=user_name
            if msg:
                qs_ans_rank_list=[]
                key_data = get_keyword(request,msg)
                print(">>>>> ",key_data[0])
                if key_data[0]:
                    data,question_ans = key_data

                else:
                    for i in tenet_data:
                        qs_ans_rank_list.append({"rank":rank_documents(request,msg,[i["question"]]),
                        "q":i["question"],
                        "a":i["response"]})
                    data =sorted(qs_ans_rank_list, key = lambda i: i['rank'],reverse=True)
                    dataObj = UserData.objects.get(user_name=request.session["username"])
                    if str(dataObj.user_type) == "woner":
                        try:
                            for i in woner_data:
                                qs_ans_rank_list.append({"rank":rank_documents(request,msg,[i["question"]]),
                                "q":i["question"],
                                "a":i["response"]})
                            rank_data =sorted(qs_ans_rank_list, key = lambda i: i['rank'],reverse=True)[0]
                            if float(rank_data["rank"][0]) ==float(0):
                                data="unknown answer"
                                question_ans = False
                            else:
                                data = rank_data['a']
                                question_ans = True
                        except Exception as e:
                            data="unknown answer"
                            question_ans = False
                    
                    if str(dataObj.user_type) == "tenet":
                        try:
                            for i in woner_data:
                                qs_ans_rank_list.append({"rank":rank_documents(request,msg,[i["question"]]),
                                "q":i["question"],
                                "a":i["response"]})
                            rank_data =sorted(qs_ans_rank_list, key = lambda i: i['rank'],reverse=True)[0]
                            if float(rank_data["rank"][0]) ==float(0):
                                data="unknown answer"
                                question_ans = False
                            else:
                                data = rank_data['a']
                                question_ans = True
                        except Exception as e:
                            data="unknown answer"
                            question_ans = False
                Chat.objects.create( user_id = dataObj, question=msg,question_ans = question_ans, answer = data )
            try:
                all_chat=list(Chat.objects.filter(user_id=dataObj).values())
            except:
                all_chat=[]
            return render(request, "index.html",{"key":dataObj,"chat":all_chat})
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return render(request, "index.html")
    return render(request, 'index.html')