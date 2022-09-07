from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from . serializer import *
from rest_framework.response import Response
from . models import Users, Attendance, Company
import telebot
import threading
from . system import *
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer
import datetime
import requests
from django.utils import timezone
import xlsxwriter
import pandas as pd
from string import ascii_lowercase
import itertools
import traceback
# 123
def home(request):


    return HttpResponse("<h1>404</h1>")

















class UserView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        print('post keldi')
        return Response({
            'status': 404,
            'data': "Xatolik post so'rovi yuboring"
        })
    def post(self, request):
        try:
            full_name = request.data['full_name']
            user_id = request.data['user_id']
            key = request.data['key']
            data = {
                "user_id": user_id,
                "full_name": full_name,
                "key": key
            }
        except Exception as e:
            print('1', e)
            try:
                full_name = request.query_params.get('full_name')
                user_id = request.query_params.get('user_id')
                key = request.query_params.get('key')
                data = {
                    "user_id": user_id,
                    "full_name": full_name,
                    "key": key
                }
            except Exception as e:
                print(e, '22')
                return Response({
                    'status': 400,
                    'data': f"Xatolik token yoki user_id xato! Yoki user bota start bermagan! {str(e)}"
                })
        try:
            company = Company.objects.get(key=key)
            Users.objects.create(
                full_name = full_name,
                user_id = user_id,
                company_key=company
            )

            return Response({
                "status": 201,
                "data": data
            })

        except Exception as e:
            print(e)
            return Response({
                "status": 400,
                "error": f"Xatolik sodir bo'ldi {str(e)}"
            })

class GetDataView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        print('post keldi')
        return Response({
            'status': 404,
            'data': "Xatolik post so'rovi yuboring"
        })

    def post(self, request):
        try:
            key = request.data['key']
            telegram_id = request.data['telegram_id']
        except Exception as e:
            print('1', e)
            try:
                key =request.query_params.get('key')
                telegram_id = request.query_params.get('telegram_id')
            except Exception as e:
                print(e, '22')
                return Response({
                    'status': 400,
                    'data': "Xatolik key yoki telegram_id xato! Yoki user bota start bermagan!"
                })

        try:
            if telegram_id and key:
                token = Company.objects.get(key = key)
                def send_file():
                    bot = telebot.TeleBot(token.bot_token)
                    try:
                        bot.send_document(
                            telegram_id,
                            open(excel(key), 'rb'),
                            caption = "<b><i>Ishchilar ro'yxati</i></b>",
                            parse_mode = 'html'
                        )
                    except Exception as e:
                        bot.send_message(telegram_id, str(traceback.format_exc()))

                thread = threading.Thread(target = send_file)
                thread.start()
                return Response({
                    'status': 200,
                    'data': "Bir necha soniyada fayl ko'rsatilgan bota yuboriladi!"
                })
            return Response({
                'status': 400,
                'data': "Xatolik token yoki telegram_id xato!"
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'data': "Xatolik token yoki telegram_id xato! Yoki user bota start bermagan!"
            })

class UserJoin(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request):
        from datetime import datetime
        try:
            user = Users.objects.get(company_key__key = request.data['key'], user_id=request.data['user_id'])
            company=Company.objects.get(key = request.data['key'])
            data = Attendance.objects.filter(
                company = company,
                user = user,
                date__day = timezone.now().day,
                date__month = timezone.now().month,
                date__year = timezone.now().year
            )
            if data.exists():
                data.update(join_date=datetime.now())
                bot_send_message(
                    user_id = request.data['user_id'],
                    key = request.data['key'],
                    text = "Foydalanuvchi ishga keldi"
                )
                return Response({
                    'status': 200,
                    'data': "Keldi"
                })

            Attendance.objects.create(
                company = company,
                user = user,
                join_date = datetime.now()
            )
            bot_send_message(
                user_id = request.data['user_id'],
                key = request.data['key'],
                text = "Foydalanuvchi ishga keldi"
            )
            return Response({
                'status': 200,
                'data': "Qo'shildi"
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'data': f"202: {str(traceback.format_exc())}"
            })

class UserLeft(APIView):
    def post(self, request):
        from datetime import datetime
        try:
            data = Attendance.objects.filter(
                company = Company.objects.get(key = request.data['key']),
                user = Users.objects.get(company_key__key = request.data['key'], user_id = request.data['user_id']),
                date__day = timezone.now().day,
                date__month = timezone.now().month,
                date__year = timezone.now().year
            )
            if data.exists():
                try:
                    data.update(left_date=datetime.now())
                except Exception as e:
                    print(e)
                bot_send_message(
                    user_id = request.data['user_id'],
                    key = request.data['key'],
                    text = "Foydalanuvchi ishdan ketdi"
                )
                return Response({
                    'status': 201,
                    'data': "User ketdi"
                })

            return Response({
                'status': 400,
                'data': "Bunday user mavjud emas yoki bugun kelmagan"
            })

        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'data': str(e)
            })

class DeleteUser(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request):
        try:
            try:
                user_id = request.data['user_id']
                key = request.data['key']
            except Exception as e:
                print(e)
                user_id =request.query_params.get('user_id')
                key = request.query_params.get('key')
            newtoken = Company.objects.filter(key = key)
            Users.objects.filter(user_id = user_id).delete()
            return Response({
                'status': 200,
                'data': "O'chirildi"
            })

        except Exception as e:
            return Response({
                'status': 400,
                'data': str(e)
            })

class NewCompany(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request):
        try:
            serializer = CompanySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 201,
                    'data': serializer.data
                })
            return Response({
                'status': 400,
                'data': serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'data': str(e)
            })

class NewToken(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request):
        try:
            try:
                token = request.data['bot_token']
                key = request.data['key']
            except Exception as e:
                print('1', e)
                token =request.query_params.get('bot_token')
                key = request.query_params.get('key')

            newtoken = Company.objects.filter(key = key)
            if newtoken.exists():
                newtoken.update(bot_token = token)
                return Response({
                    'status': 201,
                    'data': "O'zgartirildi"
                })
            return Response({
                'status': 400,
                'data': "Xatolik topilmadi"
            })

        except Exception as e:
            return Response({
                'status': 400,
                'data': str(e)
            })

class NewChannel(APIView):
    def post(self, request):
        try:
            try:
                channel_id = request.data['channel_id']
                key = request.data['key']
            except Exception as e:
                print('1', e)
                channel_id =request.query_params.get('channel_id')
                key = request.query_params.get('key')

            newtoken = Company.objects.filter(key = key)
            if newtoken.exists():
                newtoken.update(channel_id = channel_id)
                return Response({
                    'status': 201,
                    'data': "O'zgartirildi"
                })
            return Response({
                'status': 400,
                'data': "Xatolik topilmadi"
            })

        except Exception as e:
            return Response({
                'status': 400,
                'data': str(e)
            })

class GetAllUserList(APIView):
    def post(self, request):
        try:
            key = request.data['key']
            telegram_id = request.data['telegram_id']
        except Exception as e:
            try:
                key =request.query_params.get('key')
                telegram_id = request.query_params.get('telegram_id')
            except Exception as e:
                return Response({
                    'status': 400,
                    'data': f"Xatolik key yoki telegram_id xato! Yoki user bota start bermagan! {str(e)}"
                })
        try:
            token = Company.objects.get(key = key)
            bot = telebot.TeleBot(token.bot_token)
            user_list = ''
            for i in Users.objects.filter(company_key__key = key):
                user_list += f'/{i.user_id} - {i.full_name}\n'
            if user_list:
                pass
            else:
                user_list = "Foydalanuvchilar topilmadi! Ushbu kompaniyaga tegishli Foydalanuvchilar yo'q"
            bot.send_message(
                telegram_id,
                user_list,
                parse_mode = 'html'
            )
            return Response({
                'status': 200,
                'data': "Success!"
            })
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'data': f"Xatolik key yoki telegram_id xato! Yoki user bota start bermagan! {str(e)}"
            })




























                #
