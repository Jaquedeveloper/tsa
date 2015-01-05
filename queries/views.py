from tsa.utils import json_response
from queries.forms import QueryForm
from tsa.models import Query

def create_query(request):
    if not request.user.is_authenticated():
        return json_response({'status': 'error', 'message': 'Please, login first'})

    if request.method != 'POST':
        return json_response({'status': 'error', 'message': 'Invalid request type'})

    form = QueryForm(request.POST)
    if form.is_valid():
        query = form.save(commit=False)
        query.user = request.user
        query.save()
        return json_response({
            'status': 'success',
            'message': 'Query successfully created',
            'query': query.to_dict()
        })

    return json_response({'status': 'error', 'message': 'Fill required fields'})


def get_my_queries(request):
    if not request.user.is_authenticated():
        return json_response({'status': 'error', 'message': 'Please, login first'})

    my_queries = Query.objects.filter(user=request.user).order_by('-date')
    queries = [q.to_dict() for q in my_queries]
    return json_response({'queries':queries})