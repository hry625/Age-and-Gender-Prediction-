import os.path

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View

from .tasks import dataset_preparation
from app.forms import FaceRecognitionForm, DataSetUploadForm, ModelUploadForm, CurrentModelForm
from app.ml import pipeline_model
from django.conf import settings
from app.models import FaceRecognition, MLModel, CurrentModel


def index(request):
    form = FaceRecognitionForm()

    if request.method == 'POST':
        form = FaceRecognitionForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            save = form.save(commit=True)

            # extract the image object from database
            primary_key = save.pk
            imgobj = FaceRecognition.objects.get(pk=primary_key)
            fileroot = str(imgobj.image)
            filepath = os.path.join(settings.MEDIA_ROOT, fileroot)
            results = pipeline_model(filepath)
            print(results)

            return render(request, 'index.html', {'form': form, 'upload': True, 'results': results})

    return render(request, 'index.html', {'form': form, 'upload': False})

class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        form = FaceRecognitionForm()
        return render(request, self.template_name, {'form': form, 'upload': False})

    def post(self, request):
        form = FaceRecognitionForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=True)
            # extract the image object from database
            fileroot = instance.image.path
            filepath = os.path.join(settings.MEDIA_ROOT, fileroot)
            results = pipeline_model(filepath)
            return render(request, self.template_name, {'form': form, 'upload': True, 'results': results})
        return render(request, self.template_name, {'form': form, 'upload': False})


class DatasetUploadView(View):
    template_name = 'admin_ui.html'
    form = DataSetUploadForm
    mlform = ModelUploadForm
    currentform = CurrentModelForm
    selectModel = 'selectedModel'

    def get(self, request):
        modelinfo = MLModel.objects.all().values()
        return render(request, self.template_name, {'Model': self.mlform, 'ModelInfo': modelinfo, })

    def post(self, request):
        if 'uploadDataSet' in request.POST:
            form = self.form(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save()
                print(instance)
                dataset_preparation.delay(dataset_id=instance.id)
                print('valid')
            else:
                print('not valid', type(form.errors))

            return render(request, self.template_name, context={'errors': form.errors})
        elif 'uploadModel' in request.POST:
            model = self.mlform(request.POST, request.FILES)
            if model.is_valid():
                model.save()
                print('File upload successfully')
            else:
                model = ModelUploadForm()
            modelinfo = MLModel.objects.all().values()

            return render(request, self.template_name, {'Model': self.mlform, 'ModelInfo': modelinfo
                                                        })

    def selectModel(request, pk):
        currentModel = CurrentModel.objects.getfilter(file='Fjuk inc')
        if not currentModel:
            curruntModelForm = self.currentform(request.POST, request.Files)
            if curruntModelForm.is_valid():
                CurrentModelForm.save()
                # The Queryset is empty ...
        else:
            curruntModelForm = self.currentform(
                request.POST, request.Files)
            if curruntModelForm.is_valid():
                curruntModelForm.update()
        return render(request, self.template_name, {'CurrentModel': self.mlform, 'ModelInfo': modelinfo})
