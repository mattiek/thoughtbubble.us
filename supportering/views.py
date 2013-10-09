from django.shortcuts import render, HttpResponse
import json as JSON
from models import CommentSupport, Comment

def support_comment(request, id):
    result = {'status':'none'}
    noStatus = {'status':'none'}
    removedStatus = {'status':'removed'}
    addedStatus = {'status':'added'}

    if request.user.is_authenticated():
        try:
            comment = Comment.objects.get(id=id)
            try:
                g = CommentSupport.objects.get(user=request.user, comment=comment)
                g.delete()
                result['status'] = 'removed'
            except:
                CommentSupport.objects.create(user=request.user, comment=comment)
                result['status'] = 'added'
            result['count'] = CommentSupport.objects.filter(comment=comment).count()
        except:
            pass

    return HttpResponse(JSON.dumps(result), mimetype='application/json')
