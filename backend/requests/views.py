from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import InquiryRequest
from django.utils import timezone


@csrf_exempt  # مؤقتًا، إلى أن نستخدم csrf_token فعليًا في الفورم
def submit_request(request, request_type):
    if request.method == 'POST':
        InquiryRequest.objects.create(
            full_name=request.POST.get('full_name'),
            company_name=request.POST.get('company_name'),
            job_title=request.POST.get('job_title'),
            employees_count=request.POST.get('employees_count'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            request_type=request_type,
            submitted_at=timezone.now()
        )
        return render(request, 'website/thank_you.html') 


    return redirect('/')  # لو أحد دخلها بدون POST
