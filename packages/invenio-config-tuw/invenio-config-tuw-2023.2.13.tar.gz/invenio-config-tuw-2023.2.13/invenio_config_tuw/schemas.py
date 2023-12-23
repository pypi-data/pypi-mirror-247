# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Various schemas to use in InvenioRDM."""

try:
    from invenio_app_rdm.users.schemas import NotificationsUserSchema as UserSchema
    from invenio_app_rdm.users.schemas import (
        UserPreferencesNotificationsSchema as UserPreferencesSchema,
    )
except ImportError:
    from invenio_users_resources.services.schemas import (
        UserSchema,
        UserPreferencesSchema,
    )

from marshmallow import Schema, fields


class UserPreferencesCurationSchema(Schema):
    """Schema for curation preferences."""

    consent = fields.Boolean(default=False)


class TUWUserPreferencesSchema(UserPreferencesSchema):
    """User preferences schema with TU Wien extensions."""

    curation = fields.Nested(UserPreferencesCurationSchema)


class TUWUserSchema(UserSchema):
    """User schema with TU Wien extensions."""

    preferences = fields.Nested(TUWUserPreferencesSchema)
