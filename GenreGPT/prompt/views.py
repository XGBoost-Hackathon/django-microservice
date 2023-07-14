from django.shortcuts import redirect, render
from travel.views import pdf_template
# Create your views here.
def input(request):
    if request.method == 'POST':
        text= request.POST.get('text')
        print(text)
        genre= request.POST.get('genre')
        print(genre)

        if genre == 'Travel':
            pdf_template(request,text)
        elif genre == 'Kids':
            pdf_template(request,text)

    return render(request, 'input.html')