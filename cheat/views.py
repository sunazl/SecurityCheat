from django.shortcuts import render

# Create your views here.
from heart_beat import check_thread

check_thread.run()

print("1111111111111111111")