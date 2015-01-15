from django.contrib.auth.decorators import login_required

from tsa.utils import json_response
from queries.forms import QueryForm
from queries.models import Query


@login_required
def create_query(request):
    if request.method != 'POST':
        return json_response({'status': 'error', 'message': 'Invalid request type'})

    form = QueryForm(request.POST)
    if form.is_valid():
        query = Query(**form.cleaned_data)
        query.user = request.user
        query.is_public = form.cleaned_data['is_public'] == u'True'
        query.save()
        return json_response({
            'status': 'success',
            'message': 'Query successfully created',
            'query': query.to_dict()
        })

    return json_response({'status': 'error', 'message': 'Fill required fields'})


@login_required
def get_my_queries(request):
    my_queries = Query.objects.filter(user=request.user).order_by('-date')
    queries = [q.to_dict() for q in my_queries]
    return json_response({'queries': queries})


@login_required
def delete_query(request):
    try:
        id = int(request.POST.get('id'))
    except:
        id = -1

    query = Query.objects.filter(user=request.user, pk=id)
    if query:
        query.delete()
        return json_response({'status': 'success'})

    return json_response({'status': 'error'})