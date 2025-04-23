from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect

from datamodel.definitions.template import *


def index(request):
    return redirect('/static/index.html')


def template_operation(request: HttpRequest) -> HttpResponse:
    """
    A view that handles template operations.
    """
    if request.method == "POST":
        json_data = json.loads(request.body)
        template = json_data['template']
        op_type = json_data['op_type']
        t = set()
        for path, t_str in template:
            path = s2path(f'<{path}>')
            t.add((path, t_str))
        src = json_data.get('src')
        dst = json_data.get('dst')
        if src:
            src = s2path(f'<{src}>')
        if dst:
            dst = s2path(f'<{dst}>')
        if op_type.lower() == 'move':
            if dst:
                res = Mv(t, src, dst)
            else:
                res = Delete(Extract(t, src) | t, src)

        elif op_type.lower() == 'delete':
            res = Delete(t, src)
        elif op_type.lower() == 'insert':
            if dst is None:
                res = {(src, json_data['add_type'])} | t
            else:
                res = Insert(dst, {(src, json_data['add_type'])}) | t
        else:
            return HttpResponse(status=400, content="Invalid operation type")
        nested_template = Nested_t(res)
        nested_dict = pprint_nested_template(nested_template, do_print=False, api=True)
        res_template = pprint_template(res, do_print=False)
        res_string = ""
        for path, t_str in res_template:
            res_string += f"{path}: {t_str}\n"

        # Empty containers are not part of the model
        t_json = json.dumps(nested_dict).replace(': "Container"', ': {}')
        nested_dict = json.loads(t_json)
        response = HttpResponse(
            content=json.dumps(
                {
                    'nested_template': nested_dict,
                    'template': res_string,
                }
            ),
            content_type='application/json',
        )
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response
    else:
        response = HttpResponse()
        response['allow'] = ','.join(['get', 'post', 'put', 'delete', 'options'])
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response
