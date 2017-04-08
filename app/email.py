from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

# __________________________________

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# __________________________________

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    msg = Message(app.config['%s_MAIL_SUBJECT_PREFIX' % app.config['PROJECT'].upper()] + ' ' + subject,
                  sender=app.config['%s_MAIL_SENDER' % app.config['PROJECT'].upper()], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
# __________________________________
