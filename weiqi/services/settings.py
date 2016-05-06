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

from binascii import a2b_base64
from PIL import Image
from io import BytesIO
from weiqi.services import BaseService, ServiceError


class InvalidImageError(ServiceError):
    pass


class SettingsService(BaseService):
    __service_name__ = 'settings'

    @BaseService.authenticated
    @BaseService.register
    def user_info(self):
        return {
            'email': self.user.email,
        }

    @BaseService.authenticated
    @BaseService.register
    def save_user_info(self, email):
        self.user.email = email

    @BaseService.authenticated
    @BaseService.register
    def upload_avatar(self, avatar):
        if not avatar.startswith('data:image/png;base64,'):
            raise InvalidImageError('only png images are supported')

        data = avatar.split(',', 1)[1]
        data = a2b_base64(data)
        img = Image.open(BytesIO(data))
        width, height = img.size

        if width > 256 or height > 256:
            raise InvalidImageError('image is too large, max 256x256 is allowed')

        self.user.avatar = data

    @BaseService.authenticated
    @BaseService.register
    def delete_avatar(self):
        self.user.avatar = None

    @BaseService.authenticated
    @BaseService.register
    def change_password(self, password):
        self.user.set_password(password)
