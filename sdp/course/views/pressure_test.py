from django.shortcuts import render_to_response

def test(request):
    return render_to_response('pressure_test.html')
