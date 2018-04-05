from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import auth
from portal.models import Cost, Bus, Taxi
from xlrd import open_workbook
from django.http import HttpResponse
import json
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
import xlwt
from django.conf import settings

csv_file_path_looters = settings.MEDIA_ROOT +'/looters.xlsx'
csv_file_path_anc = settings.MEDIA_ROOT +'/looters.xlsx'
csv_file_path_fk = settings.MEDIA_ROOT +'/looters.xlsx'
csv_file_path_mess = settings.MEDIA_ROOT +'/looters.xlsx'
csv_file_path_others = settings.MEDIA_ROOT +'/looters.xlsx'


def index(request):
    return render(request, 'portal/index.html')


def contact(request):
    return render(request, 'portal/contact.html')

def papers1(request):
    return render(request, 'portal/papers1.html') 

def papers2(request):
    return render(request, 'portal/papers2.html')

def bus(request):
    current_user = request.user
    if current_user.is_authenticated:
        email = current_user.email
        if '@pilani.bits-pilani.ac.in' in email:
            query = Bus.objects.all().filter(email=email)
            x = False
            result = ""
            time = ""
            dest = ""
            if query.__len__() == 0:
                x = True
            elif query[0].has_cancelled:
                x = True
                result = query[0]
            else:
                x = False
                result = query[0]
                if result.bus_time == '0':
                    time = "Morning ( 9 AM)"
                else:
                    time = "Night (10 PM)"
                if result.destination == '0':
                    dest = "Jaipur"
                else:
                    dest = "Delhi"
            response = {"check": x, "query": result, "time": time, "dest": dest}
            return render(request, 'portal/bus.html', response)
        else:
            return redirect('loginPage')

    else:
        return render(request, 'portal/bus.html')


def logout(request):
    auth.logout(request)
    return redirect('loginPage')

def resources(request):
    return render(request,'portal/resources.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            print("Hey")
            auth.login(request, user)
            return HttpResponse(user)
        except ObjectDoesNotExist:
            bitsian = User.objects.create(email=username, password=password, username=username, first_name=request.POST['name'])
            auth.login(request, bitsian)
            return HttpResponse(bitsian)
    else:
        return HttpResponse("Some Error occured")


def login_page(request):
    return render(request, 'portal/login.html')


def services(request):
    return render(request, 'portal/services.html')
    # return redirect('services')


def cost(request):
    current_user = request.user
    if current_user.is_authenticated:
        email = current_user.email
        if '@pilani.bits-pilani.ac.in' in email:
            query = Cost.objects.all().filter(email=email)
            response = {"cost": query[0]}
            return render(request, 'portal/cost.html', response)
        else:
            return redirect('loginPage')

    else:
        return render(request, 'portal/cost.html')


def register_excel(request):

    data_reader = open_workbook(csv_file_path_looters).sheet_by_index(0)
    data_reader2 = open_workbook(csv_file_path_mess).sheet_by_index(0)
    data_reader3 = open_workbook(csv_file_path_anc).sheet_by_index(0)
    data_reader4 = open_workbook(csv_file_path_fk).sheet_by_index(0)
    data_reader5 = open_workbook(csv_file_path_others).sheet_by_index(0)

    for row_index in xrange(1, data_reader.nrows):
        costs = Cost()
        # cost.bitsian = request.user
        costs.institute_id = data_reader.cell(row_index, 0).value
        x = data_reader.cell(row_index, 0).value
        costs.name = data_reader.cell(row_index, 1).value
        costs.room_number = data_reader.cell(row_index, 2).value
        costs.bhavan = data_reader.cell(row_index, 3).value
        costs.cost_list_looters = data_reader.cell(row_index, 4).value
        costs.cost_list_anc = data_reader3.cell(row_index, 4).value
        costs.cost_list_fk = data_reader4.cell(row_index, 4).value
        costs.cost_list_mess = data_reader2.cell(row_index, 4).value
        costs.cost_list_others = data_reader5.cell(row_index, 4).value
        temp = x[:4]
        degree = x[4:5].lower()
        if degree != 'h' and degree != 'p':
            degree = 'f'

        if temp == '2017':
            temp = degree + '2017' + x[-4:] + '@pilani.bits-pilani.ac.in'

        else:
            temp = degree + temp + x[-3:] + '@pilani.bits-pilani.ac.in'

        costs.email = temp
        costs.save()

    return redirect('index')


def register_bus(request):
    current_user = request.user
    email = current_user.email
    user_details = Cost.objects.filter(email=email)[0]
    id = user_details.institute_id
    all_booked = Bus.objects.all()
    if request.method == 'POST':
        seat = request.POST['seat']
        date = request.POST['date']
        bus_time = request.POST['time']
        dest = request.POST['dest']
        flag_seat_booked = False
        flag_person_registered = False
        hasCancelled = False
        for newbus in all_booked:
            if newbus.seat_number == seat and newbus.date_of_bus == date and newbus.destination == dest and newbus.bus_time == bus_time and not newbus.has_cancelled:
                flag_seat_booked = True

            if newbus.email == email:
                flag_person_registered = True
                hasCancelled = newbus.has_cancelled

        if not flag_person_registered and not flag_seat_booked:
            bus = Bus()
            bus.email = email
            bus.institute_id = id
            bus.date_of_bus = date
            bus.seat_number = seat
            bus.bus_time = bus_time
            bus.destination = dest
            bus.has_cancelled = False
            bus.save()
            return HttpResponse("Successfully Booked")
        elif flag_person_registered and not flag_seat_booked and hasCancelled:
            bus = all_booked.filter(email=email)[0]
            bus.date_of_bus = date
            bus.seat_number = seat
            bus.bus_time = bus_time
            bus.destination = dest
            bus.has_cancelled = False
            bus.save()
            return HttpResponse("Successfully Booked")
        elif flag_person_registered and not hasCancelled:
            return HttpResponse("You have already booked once")
        elif flag_seat_booked:
            return HttpResponse(" This seat is already booked")
        else:
            return HttpResponse("Some error occured")


def cancel_bus(request):
    current_user = request.user
    email = current_user.email
    bus = Bus.objects.all().filter(email=email)[0]
    bus.has_cancelled = True
    bus.save()
    return HttpResponse("Cancelled Seat")


def update_excel(request):
    data_reader1 = open_workbook(csv_file_path_looters).sheet_by_index(0)
    data_reader2 = open_workbook(csv_file_path_mess).sheet_by_index(0)
    data_reader3 = open_workbook(csv_file_path_anc).sheet_by_index(0)
    data_reader4 = open_workbook(csv_file_path_fk).sheet_by_index(0)
    data_reader5 = open_workbook(csv_file_path_others).sheet_by_index(0)

    for row_index in xrange(1, data_reader1.nrows):
        x = data_reader1.cell(row_index, 0).value
        try:
            cost = Cost.objects.all().filter(institute_id=x)[0]
            cost.cost_list_looters = str(int(data_reader1.cell(row_index, 4).value) + int(cost.cost_list_looters)) 
            cost.cost_list_mess = str(int(data_reader2.cell(row_index, 4).value) + int(cost.cost_list_mess))
            cost.cost_list_anc = str(int(data_reader3.cell(row_index, 4).value) + int(cost.cost_list_anc))
            cost.cost_list_fk = str(int(data_reader4.cell(row_index, 4).value) + int(cost.cost_list_fk))
            cost.cost_list_others = str(int(data_reader5.cell(row_index, 4).value) + int(cost.cost_list_others))
            cost.save()
        except Exception as e:
            print "ONError"
    return redirect('index')


def get_valid_seats(request):
    if request.method == 'POST':
        date = request.POST['date']
        time = request.POST['time']
        destination = request.POST['dest']
        x = Bus.objects.all()\
            .filter(destination=destination).filter(bus_time=time).filter(date_of_bus=date).filter(has_cancelled=False)
        empty_seats = []
        count = 0
        for seat in x:
            empty_seats.insert(count, int(seat.seat_number))
            count += 1
        dict = json.dumps(empty_seats)
        print(dict)
        return HttpResponse(dict)
    else:
        return HttpResponse("Error")


def send_email(request):
    if request.method == 'POST':
        message = request.POST['body']
        name = request.POST['name']
        email = EmailMessage(name + "- SU Portal Message", message, to=['f2016632@pilani.bits-pilani.ac.in'])
        email.send()
        return HttpResponse("Success")


def export_bus_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bus.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Bus')
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['ID', 'Email ID', 'Date', 'Shift', 'Destination', 'Seat Booked', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    dest = ["Jaipur", "Delhi"]
    shift = ["Morning", "Night"]
    rows = Bus.objects.all().values_list('institute_id', 'email', 'date_of_bus', 'bus_time', 'destination',
                                         'seat_number', 'has_cancelled')
    for row in rows:
        row_num += 1
        x = shift[int(row[3])]
        y = dest[int(row[4])]
        if not row[6]:
            for col_num in range(len(row)-1):
                if col_num == 3:
                    ws.write(row_num, col_num, x, font_style)
                elif col_num == 4:
                    ws.write(row_num, col_num, y, font_style)
                else:
                    ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def cab(request):
    return render(request, 'portal/cab.html')


def cab_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        time = request.POST['time']
        contact = request.POST['contact']
        email = request.POST['email']
        cab_user = None
        time_arr = []
        name_arr = []
        contact_arr = []
        count = 0
        try:
            cab_user = Taxi.objects.get(email=email)
            cab_user.phone = contact
            cab_user.date = date
            cab_user.time = time
            cab_user.save()
        except ObjectDoesNotExist:
            cab_user = Taxi.objects.create(email=email, name=name, date=date, phone=contact, time=time)
        for x in Taxi.objects.all().filter(date=date):
            time_arr.insert(count, x.time)
            name_arr.insert(count, x.name)
            contact_arr.insert(count, x.phone)
            count = count+1
        dict = json.dumps({'names': name_arr, 'contacts': contact_arr, 'times': time_arr})
        print dict
        return HttpResponse(dict)
    else:
        return HttpResponse("Not AJAX")
