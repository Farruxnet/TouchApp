import telebot
from TestApp.models import *
from string import ascii_lowercase
import itertools

# -1544567759
def bot_send_message(user_id, key, text):
    company = Company.objects.get(key = key)
    user = Users.objects.get(user_id = user_id, company_key = company)
    try:
        bot = telebot.TeleBot(company.bot_token)
        # import requests
        # res = requests.post(f'https://api.telegram.org/bot{company.bot_token}/sendMessage?chat_id={company.channel_id}&text=Hello World!')
        # res2 = requests.post(f'https://api.telegram.org/bot{company.bot_token}/getUpdates')
        # print(res.json())
        # print(res2.json())
        print(f'{company.channel_id}\n'+str(user.full_name) + '\n' + str(text))
        bot.send_message(chat_id = f'{company.channel_id}', text = str(user.full_name) + '\n' + str(text), parse_mode='HTML')
    except Exception as e:
        print(e)


def line():
  c = 1
  d = 1
  ls = []
  a = ''
  def iter_all_strings():
    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(s)

  for s in iter_all_strings():
      a += s.upper() + ' '
      if c % 3 == 0:
          ls.append(a)
          a = ''
          d += 1
      c += 1
      if d == 31:
          break
  return ls[1:]
