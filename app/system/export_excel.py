from app.models import Users, Attendance
import xlsxwriter
import pandas as pd
import datetime
from django.conf import settings
import random
from . bot import *

def excel(key):
    users = []
    data_date = []
    users_id = []
    user_join = []
    user_left = []
    work = []
    name = f"{str(settings.BASE_DIR)}/static/file/data_{datetime.datetime.now()}_{random.randint(1, 9999)}.xlsx"
    # name = f"output.xlsx"
    data = Users.objects.filter(
        company_key__key = key,
        # date__day = datetime.datetime.now().day,
        # date__year = datetime.datetime.now().year,
        # date__month = datetime.datetime.now().month,
    )
    for i in data:
        users.append(i.full_name)
        users_id.append(i.user_id)
        if i.join_date:
            user_join.append(i.join_date.strftime("%H:%M:%S"))
        if i.left_date:
            user_left.append(i.left_date.strftime("%H:%M:%S"))
        # data_date.append(i.strftime("%Y-%m-%d"))
        # print(int(i.join_date.strftime("%H")), int(i.left_date.strftime("%H")))
        if i.join_date and i.left_date:
            work.append(int(i.join_date.strftime("%H")) - int(i.left_date.strftime("%H")))
        else:
            work.append(0)
    df = pd.DataFrame()
    writer = pd.ExcelWriter(name, engine='xlsxwriter')
    workbook=writer.book
    date_bg = workbook.add_format({"border": 6, 'bold': True, "bg_color": "#daf013"})
    date_bg.set_align('center')

    id_bg = workbook.add_format({"border": 4, "bg_color": "#03fc03"})
    left_bg = workbook.add_format({"border": 7, "color": "red"})
    join_bg = workbook.add_format({"border": 7, "color": "blue"})
    work_bg = workbook.add_format({"border": 7, "color": "#03fc73"})
    df.to_excel(writer, sheet_name="Ishchilar ro'yxati")

    ws = writer.sheets["Ishchilar ro'yxati"]

    ws.merge_range(f"A1:A2", '№')
    ws.merge_range('B1:B2', 'ID')
    ws.merge_range('C1:C2', 'ISMI')
    for zz, dd in zip(range(data.count()), data):
        ws.write(f"A{zz+3}", zz + 1)
        ws.write(f"B{zz+3}", dd.user_id)
        ws.write(f"C{zz+3}", dd.full_name)
    dt = 0
    for q in line():
        date_now = datetime.datetime.now() - datetime.timedelta(days = dt)
        dt += 1
        da =  Attendance.objects.filter(
            company__key = key,
            date__day = date_now.day,
            date__year = date_now.year,
            date__month = date_now.month,
        )
        ws.merge_range(f"{q.split(' ')[0]}1:{q.split(' ')[2]}1", date_now.strftime("%Y-%m-%d"), date_bg)
        ws.write(f"{q.split(' ')[0]}2", 'KELDI', join_bg)
        ws.write(f"{q.split(' ')[1]}2", 'KETDI', left_bg)
        ws.write(f"{q.split(' ')[2]}2", 'ISHLADI', work_bg)
        for user_data, z in zip(da, range(da.count())):
            if user_data.join_date:
                ws.write(f"{q.split(' ')[0]}{users.index(user_data.user.full_name)+3}", user_data.join_date.strftime("%H:%M"))
            else:
                ws.write(f"{q.split(' ')[0]}{users.index(user_data.user.full_name)+3}", "-")
            if user_data.left_date:
                ws.write(f"{q.split(' ')[1]}{users.index(user_data.user.full_name)+3}", user_data.left_date.strftime("%H:%M"))
            else:
                ws.write(f"{q.split(' ')[1]}{users.index(user_data.user.full_name)+3}", "-")

            # ws.write(f"{q.split(' ')[2]}{users.index(user_data.user.full_name)+3}", work[z])
            # print((datetime.datetime.strptime(user_data.join_date.strftime("%H"), "%H") - datetime.datetime.strptime(user_data.left_date.strftime("%H"), "%H")))
            try:
                work_time = datetime.datetime.strptime(user_data.left_date.strftime("%H:%M"), "%H:%M")-datetime.datetime.strptime(user_data.join_date.strftime("%H:%M"), "%H:%M")
                sumH = datetime.datetime.strptime(str(work_time), "%H:%M:%S").hour
                sumM = datetime.datetime.strptime(str(work_time), "%H:%M:%S").minute
                # sumH = abs(int(user_data.join_date.strftime("%H")) - int(user_data.left_date.strftime("%H")))
                # sumM = abs(int(user_data.join_date.strftime("%M")) - int(user_data.left_date.strftime("%M")))
            except Exception as e:
                sumH = 0
                sumM = 0

            ws.write(
                f"{q.split(' ')[2]}{users.index(user_data.user.full_name)+3}",
                f"{sumH}.{sumM}"
            )


    writer.save()
    return name















def write_excel():
    data = []
    join_date = []
    left_date = []
    year = []
    for i in Attendance.objects.all():
        data.append(
            [
                i.user.user_id,
                i.user.full_name,
                i.left_date.strftime("%H:%M:%S")
            ]
        )
        join_date.append(
            [
                i.join_date.strftime("%H:%M:%S")
            ]
        )
        year.append(

            i.join_date.strftime("%Y-%m-%d")

        )
        left_date.append(
            [
                i.left_date.strftime("%H:%M:%S")
            ]
        )
    col = ['ID', 'ISMI']+year
    # data += join_date
    # data += left_date
    print(col)
    print(data)
    df1 = pd.DataFrame(
            data,
            # index=['row 1', 'row 2'],
            columns = col
          )
    def highlight_fifty(val):
        # if val in ['ID', 'ISMI', "Kelgan VAQT", "Ketgan"]:
        print(val)
        # color = '#ffffff'
        bg = '#e6ffe6'
        return f'background-color: {bg}'
    # df1 = df1.style.applymap(highlight_fifty, subset=['B1'])
    df1 = df1.style.applymap(highlight_fifty)

    name = f"{str(settings.BASE_DIR)}/static/file/data_{datetime.datetime.now()}_{random.randint(1, 9999)}.xlsx"
    df1.to_excel(name, sheet_name = "Ishchilar ro'yxati")
    return name
