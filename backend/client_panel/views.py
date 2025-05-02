from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def client_dashboard(request):
    return render(request, 'client_panel/dashboard.html')  # ← مهم!
