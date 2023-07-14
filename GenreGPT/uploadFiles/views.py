from io import BytesIO
from itertools import count
import math
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from reportlab.pdfgen import canvas
import os
from django.views.generic import ListView, DetailView
from django.conf import settings
import os
import openai
from base64 import b64decode

itr=0 #global variablec
# Create your views here.
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('upload')

        for file in files:
            # file_type = magic.from_buffer(file.read(), mime=True)

            # if file_type == 'application/pdf':
            # # Handle PDF file
            #    return HttpResponse('The file is in PDF format.')
            # elif file_type == 'image/png':
            # # Handle PNG file
            #    return HttpResponse('The file is in PNG format.')

            f = UploadFiles(file= file)
            f.save()
            print("success")

    f2= UploadFiles.objects.all()
    context= {
        'f2' : f2
    }
    return render(request, "fileUpload.html", context)



def extract_keyword(text):
    openai.organization = "org-sXoFLu4TXWUPiZIPL8RSUqy4"
    openai.api_key = "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"
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt="Extract keywords from this text in a python list: (Just output the list)\n\n"+text,
      temperature=0.5,
      max_tokens=60,
      top_p=1.0,
      frequency_penalty=0.8,
      presence_penalty=0.0
    )
    
    print(response['choices'][0]['text'])
    story = response['choices'][0]['text']
    print(type(story))
    keywords = []
    for i in range(0,len(story)):
      if story[i]=='"' or story[i]=="'":
        for j in range(i+1, len(story)):
          if story[j] == '"' or story[j] == "'":
            keywords.append(story[i+1:j])
            break
    #print(keywords)
    final_keywords = []
    for i in keywords:
      if len(i)>2:
        final_keywords.append(i)
          
    print(final_keywords)
    final_keywords = final_keywords[:5]

    
    return final_keywords


def generateImage_AndSave(prompt, image_count):
    images = []
    response = openai.Image.create(
        prompt=prompt,
        n= image_count,
        size='512x512',
        response_format='b64_json'
    )

    for image in response['data']:
        images.append(image.b64_json)

    prefix = 'Img'
    for index,image in enumerate(images):
        global itr
        folder_path = os.path.join(settings.MEDIA_ROOT, '')

        with open(f'{folder_path}{prefix}_{index}{itr}.jpg','wb') as file:
            file.write(b64decode(image))
            print(file)
            itr += 1

def upload_text(request):
    if request.method == 'POST':
        folder_path = os.path.join(settings.MEDIA_ROOT, '')
        delete_files(folder_path)
        input= request.POST.get('text')
        # return redirect('pdf_template')

        

        openai.organization = "org-sXoFLu4TXWUPiZIPL8RSUqy4"
        openai.api_key = "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"
        text = input
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Write a Kid's story about the below topic\n\n"+text,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0
        )
        story= response['choices'][0]['text']
        request.session['input'] = story

        print(story)
   
    return render(request,'input_text.html')

def delete_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

def pdf_template(request, text):
    content=[]
    images = []
    openai.api_key = "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"
    keywords = extract_keyword( text)
    for word in keywords:
        generateImage_AndSave(word,image_count=1)
        print("image generated")

    folder_path = os.path.join(settings.MEDIA_ROOT, '')  # Replace 'folder_name' with the actual folder name
    for filename in os.listdir(folder_path):
            if filename.endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(settings.MEDIA_URL, '', filename)
                images.append(image_path)


    paragraph = str(request.session.get('input')) 
    print(paragraph)
    words = paragraph.split()
    para= math.floor(len(words)/len(images))
    chunks = [words[i:i+para] for i in range(0, len(words), para)]
    
    for i in chunks:
       content.append(' '.join(i))

    content_with_images = zip(content, images)
    

    context={
        #  'content': chunks,
        #  'images': images,
        'content_with_images': content_with_images 
    }
    return render(request, 'pdf_template.html',context)