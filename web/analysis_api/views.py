
# Create your views here.

from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
import json
from .nltk_processor import analyze
from .forms import AnalysisForm
from .serializers import Analysis, User
from .serializers import UserSerializer, UserSerializerSimple, AnalysisSerializer
from .chart_logic import stacked_bar_for_one, Chart


class RegisterApiView(generics.CreateAPIView):
    permission_classes = ''
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserSerializer

class UserApiView(generics.RetrieveAPIView):
    permission_classes = ''
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.kwargs['pk'])

class UsersAllApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializerSimple

    def get_queryset(self):
        return User.objects.all()

class AnalysisApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    # print('Analysis API View function hits: Line 31 analysis_api/view.py')
    serializer_class = AnalysisSerializer

    def get_queryset(self):
        usr_obj = User.objects.get(username=self.request.user.username)
        return Analysis.objects.filter(user_id=usr_obj.id)

    def perform_create(self, serializer):
        analysis_obj = analyze(self.request.data['text'])
        usr_obj = User.objects.get(username=self.request.user.username)
        try:
            db_analysis_obj = Analysis.objects.get(analysis=analysis_obj, user_id=usr_obj.id)
            print('Object Exists, Successfully Retrieved')
        except ObjectDoesNotExist:
            db_analysis_obj = Analysis.objects.create(analysis=analysis_obj, user_id=usr_obj.id)
            print('Object Does Not Exist, Successfully Created')
        # serializer(db_analysis_obj)
        res_obj = AnalysisSerializer(db_analysis_obj)
        json_obj = JSONRenderer.render(res_obj.data)
        print(json_obj)
        return Response(json_obj)


        # print(created)
        # if created is False:
        #     # data = {'Analysis': analysis_obj, 'user_id': usr_obj.id}
        #     # analysis = AnalysisSerializer(db_analysis_obj, data=data)
        #     # print(db_analysis_obj, "exists")
        #     # analysis.is_valid()
        #     # analysis.save()
        #     # print(analysis)
        #     # print('///////////')
        #     # print(analysis.data)
        #     # print(analysis_obj)
        #     return db_analysis_obj
        # print('Creating new obj')
        # serializer.save(analysis=analysis_obj, user_id=usr_obj.id)
        # return Response(analysis_obj.data['analysis'], status=201)
        # print(self.request.data['text'])
        # print(dir(self.request.data))
        # pass
        # serializer.save(user=self.request.user)


class AnalysisGraphApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnalysisSerializer

    def perform_create(self, serializer, *args, **kwargs):
        chart_type = self.kwargs['chart']
        if chart_type == "stacked_bar":
            analysis_obj = analyze(self.request.data['text'])
            usr_obj = User.objects.get(username=self.request.user.username)
            # serializer.save(analysis=analysis_obj, user_id=usr_obj.id)
            db_analysis_obj, created = Analysis.objects.get_or_create(analysis=analysis_obj)

            new_chart = Chart('stacked_bar', AnalysisSerializer(db_analysis_obj).data['analysis'])
            # print(db_analysis_obj)
            return new_chart.stacked_bar()
        else:
            return """Error: Choose a corresponding Graph:
            -> stacked_bar
            -> pie_chart
            -> compound_bar
            """



    # def get_queryset(self):
    #     usr_obj = User.objects.get(username=self.request.user.username)
    #     user_data = Analysis.objects.filter(user_id=usr_obj.id)
    #     for



# class ChartAPIView(generics.)



def home_view(request):
    return render(request, 'base/input.html')


def index(request):
    x= [1,3,5,7,9,11,13]
    y= [1,2,3,4,5,6,7]
    title = 'y = f(x)'

    plot = figure(title= title ,
        x_axis_label= 'X-Axis',
        y_axis_label= 'Y-Axis',
        plot_width =400,
        plot_height =400)

    plot.line(x, y, legend= 'f(x)', line_width = 2)
    #Store components
    script, div = components(plot)

    #Feed them to the Django template.
    return render_to_response( 'base/bokeh.html',
            {'script' : script , 'div' : div} )

# class AnalysisApiView(generics.RetrieveAPIView):
#     permission_classes = ''

#     def get_queryset(self):

#         return User.objects.filter(id=self.kwargs['pk'])
