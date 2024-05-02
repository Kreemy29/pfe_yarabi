from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.conf import settings
import pandas as pd
from sqlalchemy import create_engine
import logging
from .forms import UploadFileForm
from .utils import read_excel_file, process_excel_data

logger = logging.getLogger(__name__)


def create_engine_for_db():
    return create_engine(f"mysql+mysqlconnector://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return HttpResponse("Invalid username or password")
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def admin_dashboard(request):
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        files = request.FILES.getlist('files')
        all_results = []
        for file in files:
            try:
                df = read_excel_file(file)
                processed_data = process_excel_data(df)
                all_results.append(processed_data.to_dict('records'))
            except Exception as e:
                logger.error(f"Error processing file {file.name}: {str(e)}")
                return HttpResponse(f"Error processing file {file.name}: {str(e)}")
        request.session['results'] = all_results
        return redirect('view_results')
    return render(request, 'main/admin_dashboard.html', {'form': form})


@login_required
def view_results(request):
    results = request.session.get('results', [])
    results_html = []
    for result_set in results:
        try:
            df = pd.DataFrame(result_set)
            results_html.append(df.to_html(classes=["table", "table-striped"], border=0))
        except Exception as e:
            logger.error(f"Error converting results to DataFrame: {e}")
            results_html.append(f"Error processing results: {e}")
    return render(request, 'main/results.html', {'results_html': results_html})



@login_required
def gestionnaire_dashboard(request):
    return render(request, 'main/gestionnaire_dashboard.html')

@login_required
def consultant_dashboard(request):
    return render(request, 'main/consultant_dashboard.html')

@login_required
def import_files(request):
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        file = form.cleaned_data['file']
        try:
            df = read_excel_file(file)
            return render(request, 'main/results.html', {'dataframe': df.to_html()})
        except Exception as e:
            logger.error(f"Error reading Excel file: {e}")
            return render(request, 'main/import_files.html', {'form': form, 'error': str(e)})
    return render(request, 'main/import_files.html', {'form': form})



def upload_files(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('files')
            for file in files:
                print(file.name)  # Just print the file name or save it to a simple path
            return render(request, 'main/upload.html', {'form': form, 'success_message': 'Files uploaded successfully.'})
    else:
        form = UploadFileForm()
    return render(request, 'main/upload.html', {'form': form})