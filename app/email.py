
from . import mail
from flask_mail import Message
from flask import render_template, current_app

from threading import Thread


def send_email(to, subject, template, **kwargs):
	def send_async_email(app, msg):
		with app.app_context():
			mail.send(msg)
	app = current_app._get_current_object()
	msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
	              sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
	msg.body = render_template(template + '.txt', **kwargs)
	msg.html = render_template(template + '.html', **kwargs)
	job = Thread(target=send_async_email, args=[app, msg])
	job.start()
	return job