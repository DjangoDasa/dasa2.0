from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db import models


# Create your models here.
class Analysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analysis')

    analysis = models.CharField(max_length=8192, default='Null', unique=True)

    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __repr__(self):
        return '<Analysis: {}>'.format(self.analysis)

    def __str__(self):
        return '{}'.format(self.analysis)





# from datetime import datetime as dt
# from sqlalchemy.exc import DBAPIError
# from sqlalchemy.orm import relationship
# from .meta import Base
# from ..views.nltk_logic import analyze

# # from .associations import portfolios_associations
# import json

# from sqlalchemy import (
#     Column,
#     Index,
#     Integer,
#     Text,
#     DateTime,
#     ForeignKey,
#     String,
#     cast,
#     JSON,
# )


# class NLTKOutput(Base):
#     """ Create the nltk table
#     """
#     __tablename__ = 'nltk_output'
#     id = Column(Integer, primary_key=True)
#     nltk_result = Column(JSON)
#     account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
#     accounts = relationship('Account', cascade="all, delete", back_populates='nltk_output')
#     date_created = Column(DateTime, default=dt.now())
#     date_updated = Column(DateTime, default=dt.now(), onupdate=dt.now())

#     @classmethod
#     def new(cls, request, **kwargs):
#         """ Create a new nltk analysis
#         """
#         if request.dbsession is None:
#             raise DBAPIError
#         unmodified_obj = analyze(kwargs['text'])
#         mod_sent = {}
#         for sent in unmodified_obj['Sentences']:
#             mod_sent[sent] = unmodified_obj['Sentences'][sent][1]
#         mod_obj = {'Sentences': mod_sent, 'Body': unmodified_obj['Body']}
#         kwargs['nltk_result'] = json.dumps(mod_obj)
#         kwargs.pop('text', None)

#         # fake_obj = {"account_id": 1, "nltk_result": json.dumps(['string'])}
#         nltk = cls(**kwargs)
#         # nltk = cls(**fake_obj)
#         request.dbsession.add(nltk)
#         # request.dbsession.flush()
#         return [request.dbsession.query(cls).filter(
#             cast(cls.nltk_result, String) == kwargs['nltk_result']).one_or_none(),
#             unmodified_obj]

#     @classmethod
#     def all(cls, request):
#         """List all the results
#         """
#         if request.dbsession is None:
#             raise DBAPIError

#         return request.dbsession.query(cls).all()

#     @classmethod
#     def one(cls, request, pk=None):
#         """List one of the results
#         """
#         if request.dbsession is None:
#             raise DBAPIError
#         return request.dbsession.query(cls).get(pk)

#     @classmethod
#     def remove(cls, request=None, pk=None):
#         """ Remove a users nltk anaylsis from the db
#         """
#         if request.dbsession is None:
#             raise DBAPIError

#         return request.dbsession.query(cls).filter(cls.account_id == pk).delete()

