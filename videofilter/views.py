from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import cv2
import numpy as np
import os

def handle_uploaded_file(f):
    with open('./media/temp.mp4', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    convert_to_monochrome('./media/temp.mp4', './media/monochrome.mp4')

def convert_to_monochrome(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))), False)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gray_frame)
    
    cap.release()
    out.release()

def upload_and_convert(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        handle_uploaded_file(uploaded_file)
        fs = FileSystemStorage(location='./media/')
        with fs.open('monochrome.mp4') as mp4:
            response = HttpResponse(mp4, content_type='video/mp4')
            response['Content-Disposition'] = 'attachment; filename="monochrome.mp4"'
            return response
    
    return render(request, 'upload.html')
