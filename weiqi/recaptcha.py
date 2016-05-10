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

import requests
from weiqi import settings


class RecaptchaError(Exception):
    pass


def validate_recaptcha(response):
    backend = globals()[settings.RECAPTCHA['backend'] + '_validator']
    backend(response)


def dummy_validator(response):
    pass


def google_validator(response):
    res = requests.post('https://www.google.com/recaptcha/api/siteverify', {
        'secret': settings.RECAPTCHA['secret'],
        'response': response,
    })

    data = res.json()

    if not data['success']:
        raise RecaptchaError('reCAPTCHA verification did not return a success')


