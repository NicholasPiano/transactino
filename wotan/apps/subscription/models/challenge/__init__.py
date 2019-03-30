
import uuid

from django.db import models
from django.conf import settings

from util.gpg import GPG

from apps.base.models import Model, Manager, model_fields
from apps.base.schema.constants import schema_constants

from ...constants import mode_constants, APP_LABEL
from .constants import challenge_constants, challenge_fields
from .generate import generate_challenge_content
from .schema.common import ChallengeModelSchema
from .schema.superadmin import ChallengeSuperadminModelSchema

class ChallengeManager(Manager):
  def attributes(self, mode=None):
    fields = [
      challenge_fields.ENCRYPTED_CONTENT,
    ]
    if mode == mode_constants.SUPERADMIN:
      fields.extend([
        challenge_fields.ORIGIN,
        challenge_fields.CONTENT,
        challenge_fields.IS_OPEN,
        challenge_fields.HAS_BEEN_USED,
      ])

    return [
      field
      for field in self.model._meta.get_fields()
      if (
        not field.is_relation
        and field.name != model_fields.ID
        and field.name in fields
      )
    ]

  def serialize(self, instance, attributes=None, relationships=None, mode=None):
    serialized = {
      schema_constants.ATTRIBUTES: self.serialize_attributes(
        instance,
        attributes=attributes,
        mode=mode,
      ),
    }

    if mode == mode_constants.SUPERADMIN:
      serialized.update({
        schema_constants.RELATIONSHIPS: self.serialize_relationships(
          instance,
          relationships=relationships,
          mode=mode,
        ),
      })

    return serialized

  def schema(self, mode=None):
    if mode == mode_constants.SUPERADMIN:
      return ChallengeSuperadminModelSchema(self.model, mode=mode)

    return ChallengeModelSchema(self.model, mode=mode)

class Challenge(Model):
  objects = ChallengeManager()

  account = models.ForeignKey(
    challenge_constants.ACCOUNT_RELATED_MODEL,
    related_name=challenge_constants.ACCOUNT_RELATED_NAME,
    on_delete=models.CASCADE,
  )

  origin = models.UUIDField(default=uuid.uuid4)
  content = models.TextField(default=generate_challenge_content, editable=False)
  encrypted_content = models.TextField(
    default='',
    verbose_name=(
      'The secret content of the challenge encrypted'
      ' to the public key of the user. Decrypt this content'
      ' using your secret key.'
    ),
  )
  is_open = models.BooleanField(default=True)
  has_been_used = models.BooleanField(default=False)

  class Meta:
    app_label = APP_LABEL

  def encrypt_content(self):
    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    self.encrypted_content = gpg.encrypt_to_public_with_long_key_id(
      content=self.content,
      long_key_id=self.account.long_key_id,
    )

    self.save()

  def verify_content(self, content):
    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    decrypted_content = gpg.decrypt_from_private(content)

    if self.content == decrypted_content:
      self.is_open = False
      self.save()
      return True

    return False
