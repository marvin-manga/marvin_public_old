#!/usr/bin/python

import os

import flask, sqlalchemy, json
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text
from flask import request, render_template, send_from_directory, current_app, jsonify, Response
from flask import session as current_session
from manga_utils import generalUtils as gu
from collections import defaultdict, OrderedDict

import numpy as np

from ..model.database import db
from ..utilities import makeQualNames, processTableData

try: from inspection.marvin import Inspection
except: from marvin.inspection import Inspection

import sdss.internal.database.utah.mangadb.DataModelClasses as datadb

try:
    from . import valueFromRequest, processRequest
except ValueError:
    pass 

feedback_page = flask.Blueprint("feedback_page", __name__)

@feedback_page.route('/marvin/feedback.html', methods=['GET','POST'])
@feedback_page.route('/feedback.html', methods=['GET','POST'])
def feedback():
    ''' User feedback page '''
    
    feedback = {}
    feedback['title'] = "Marvin | Feedback"
    
    # get inspection
    feedback['inspection'] = inspection = Inspection(current_session)
    feedback['ready'] = inspection.ready
    
    # build products
    #inspection.component = OrderedDict([('Marvin','marvin'),('DRP','mangadrp'),('DAP','mangadap'),('Mavis','mangacas')])
    inspection.set_component()
    feedback['products'] = inspection.component.keys()
    
    # build types
    #inspection.type = OrderedDict([('Feature Request','enhancement'), ('Bug','defect'), ('Use Case','task'), ('Other','task')])
    inspection.set_type()
    feedback['types'] = inspection.type.keys()
    
    # get form feedback and add to db
    if inspection.ready:
        addfeedback = valueFromRequest(key='feedback_form',request=request, default=None)
    
        # add feedback to db
        if addfeedback:
            form = processRequest(request=request)
            feedback['form'] = form
            inspection.submit_feedback(form=form)
    inspection.retrieve_feedbacks()
    result = inspection.result()
    
    return render_template('feedback.html',**feedback)

@feedback_page.route('/marvin/feedback/promotetracticket', methods=['GET','POST'])
def promotetracticket():
    ''' User feedback function to promote tracticket '''
    
    # get inspection
    inspection = Inspection(current_session)
    
    # get id from button and promote trac ticket
    if inspection.ready:
        id = valueFromRequest(key='id',request=request, default=None)
    
        # add feedback to db
        if id:
            inspection.message("inspection looking up feedback id=%r" % id)
            """inspection.set_feedback(id=id)
            inspection.promote_tracticket()"""

    return inspection.result
