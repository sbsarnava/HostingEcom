from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import random, string, requests

adminUser = 'admin'
adminPass = 'x9DSPICmaKu5Dk23'


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def randomNumber():
    letters = string.digits
    result_str = ''.join(random.choice(letters) for i in range(10))
    return result_str


def verifyConnection():
    data = {
        "adminUser": adminUser,
        "adminPass": adminPass
    }
    response = requests.post('https://panel.gitdev.in:8090/api/verifyConn', json=data)
    return response
