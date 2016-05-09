# weiqi.gs
# Copyright (C) 2016 Michael Bitzi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import smtplib
from email.mime.text import MIMEText
from weiqi import settings


def send_mail(to, subject, body):
    backend = globals()[settings.MAILER['backend'] + '_mailer']
    backend(to, subject, body)


def console_mailer(to, subject, body):
    print('To: %s\nSubject: %s\nBody:\n%s' % (to, subject, body))


def smtp_mailer(to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = settings.MAILER['from']
    msg['To'] = to

    with smtplib.SMTP(settings.MAILER['smtp_host']) as smtp:
        smtp.sendmail(settings.MAILER['from'], [to], msg.as_string())
