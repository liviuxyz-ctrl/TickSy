# from django.shortcuts import render
# from ticksy.ticketing.models import Employees
#
# def test(request):
#     return render(request, 'test.html')
#     # return HttpResponse('test')
#
#
# def register(request):
#     if request.method == 'POST':
#         if request.POST.get('name') and request.POST.get('email') and request.POST.get('department'):
#             e = Employees()
#             e.full_name = request.POST.get('name')
#             e.email = request.POST.get('email')
#             e.department = request.POST.get('department')
#             e.team_id = 1
#             e.save()
#             return render(request, 'test.html')
#         else:
#             return render(request, 'register.html')
#     else:
#         return render(request, 'register.html')
