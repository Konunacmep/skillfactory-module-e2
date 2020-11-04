from .forms import MailForm
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.core.mail import send_mail
from threading import Thread
from time import sleep
from datetime import datetime
from .models import SentMail

ACTIVE_MAILS = {}


# как сказано в документации - поток прекращает работу как тоьлко происходит возврат из функции. т.е. руками закрывать нет нужды
def send_mail_in_tread(iD):
    sleep(ACTIVE_MAILS[iD][0].seconds)
    send_mail(
        subject = ACTIVE_MAILS[iD][0].subject,
        message = ACTIVE_MAILS[iD][0].body,
        recipient_list = ACTIVE_MAILS[iD][1],
        from_email = 'module E2',
    )
    ACTIVE_MAILS[iD][0].sending_time = datetime.now()
    ACTIVE_MAILS[iD][0].save()
    del ACTIVE_MAILS[iD]
    return


class MailFormView(FormView):
    template_name = 'send_form.html'
    success_url = 'list/'
    form_class = MailForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        new_mail = SentMail(
            subject = form.cleaned_data['subject'] if form.cleaned_data['subject'] else ' ',
            body = form.cleaned_data['body'] if form.cleaned_data['body'] else ' ',
            to = ' ,'.join(form.cleaned_data['to']),
            seconds = form.cleaned_data['seconds'],
            creation_time = datetime.now(),
        )
        new_mail.save()
        # new_mail.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ACTIVE_MAILS[new_mail.id] = [new_mail, form.cleaned_data['to']]
        Thread(target=send_mail_in_tread, args=(new_mail.id, )).start()
        return super().form_valid(form)


class MailLast10View(TemplateView):
    template_name = 'mails_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_mails'] = reversed(SentMail.objects.all().order_by('-id')[:10])
        return context
