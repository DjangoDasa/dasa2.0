
# Create your views here.

from django.shortcuts import render, render_to_response
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
import json
from django.http import HttpResponse
from .nltk_processor import analyze
from .forms import AnalysisForm
from .serializers import Analysis, User
from .serializers import UserSerializer, UserSerializerSimple, AnalysisSerializer
from .chart_logic import Chart

# logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s -  %(message)s')
# # logging.disable(logging.CRITICAL)


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


class AnalysisApiView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnalysisSerializer

    def get(self, *args, **kwargs):
        usr_obj = User.objects.get(username=self.request.user.username)
        return HttpResponse(Analysis.objects.filter(user_id=usr_obj.id))

    def post(self, *args, **kwargs):
        analysis_obj = analyze(self.request.data['text'])
        usr_obj = User.objects.get(username=self.request.user.username)
        db_analysis, created = Analysis.objects.get_or_create(
            analysis=analysis_obj,
            user_id=usr_obj.id)
        return HttpResponse(db_analysis)



class AnalysisGraphApiView(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AnalysisSerializer

    def post(self, serializer, *args, **kwargs):
        chart_type = self.request.data['chart']
        analysis_obj = analyze(self.request.data['text'])
        usr_obj = User.objects.get(username=self.request.user.username)
        Analysis.objects.get_or_create(analysis=analysis_obj, user_id=usr_obj.id)
        analysis_obj = {'0': analysis_obj}
        chart_options = ['stacked_bar', 'compound_bar', 'pie_chart']
        if chart_type in chart_options:
            new_chart = Chart(chart_type, analysis_obj)
            if chart_type == "stacked_bar":
                new_chart = new_chart.stacked_bar()
            elif chart_type == "compound_bar":
                new_chart = new_chart.compound_bar()
            return HttpResponse(new_chart)
        else:
            return "Error: Choose a corresponding Graph: " + str(chart_options)



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
