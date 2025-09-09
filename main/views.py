from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'nama' : 'Derrick',
        'npm' : '2406351440',
        'kelas' : 'PBP C'
    }
    
    return render(request, "main.html", context)