
from django.conf import settings

from util.gpg import GPG
from util.api import (
  Schema, StructureSchema,
  Response, StructureResponse,
  types, map_type,
  constants,
)

from .....system import System
from .....ip import IP
from ....constants import account_fields
from .errors import account_anonymous_method_errors
from .constants import create_constants

def disclaimer(ip=None, long_key_id=None):
  return '''
    #### Disclaimer ####

    Your account has been created with the IP address {ip} and long key
    id {long_key_id}, but you should be aware of the following matters:

    1. Until you have an active subscription, your account will be bound to
       the current IP address. Any user with access to this IP address will
       be treated equally with respect to this account. For this reason, it
       is recommended to secure access to an IP address that is restricted
       to your use only.
    2. This interface is provided with a guarantee on behalf of the published
       public key. Please refer to this guarantee for more information, but
       understand that there is no recognised authority that is bound to
       enforce the terms offered therein. Please exercise caution and ensure
       that all material transferred to the system is secured cryptographically.
    3. Although the system guarantees the integrity of the information provided
       via this interface, it is prudent to regularly check the results against
       other external sources. The information is drawn from a single common
       source (The Bitcoin Blockchain), allowing the reported data to be easily
       corroborated.
  '''.format(ip=ip, long_key_id=long_key_id)

class AccountCreatePublicKeyResponse(Response):
  def set_long_key_id(self, long_key_id=None):
    self.key_long_key_id = long_key_id

  def get_long_key_id(self):
    return self.key_long_key_id

class AccountCreatePublicKeySchema(Schema):
  def __init__(self, **kwargs):
    super().__init__(
      **kwargs,
      description=(
        'A valid GPG public key in ASCII armor format'
        ' with newlines replaced by their escaped equivalent (\\n)'
      ),
      response=AccountCreatePublicKeyResponse,
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        account_anonymous_method_errors.INVALID_PUBLIC_KEY(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    gpg = GPG(binary=settings.GPG_BINARY, path=settings.GPG_PATH)
    public_key_import = gpg.import_key(payload)

    if not public_key_import.is_valid:
      self.active_response.add_error(account_anonymous_method_errors.INVALID_PUBLIC_KEY())
      return False

    self.active_response.set_long_key_id(public_key_import.long_key_id)

    return passes_pre_response_checks

class AccountCreateSchema(StructureSchema):
  def __init__(self, Model, **kwargs):
    self.model = Model
    super().__init__(
      **kwargs,
      description=(
        'This method can be used to create an account on the system with the'
        ' specified public key. This account will be bound to the public key'
        ' from which the request or connection originates.'
      ),
      client=StructureSchema(
        description=(
          'If successful, the create function will return an acknowledgement'
          ' of the created account and a disclaimer.'
        ),
        children={
          create_constants.DISCLAIMER: Schema(
            description=(
              'The system disclaimer. This can also be found by accessing the System object.'
            ),
          ),
          create_constants.IP: Schema(
            description=(
              'The IP address used to create this account'
            ),
          ),
          create_constants.LONG_KEY_ID: Schema(
            description=(
              'The long key id of the GPG public key used to create this account'
            ),
          ),
        }
      ),
      children={
        account_fields.PUBLIC_KEY: AccountCreatePublicKeySchema(),
      }
    )

  def get_available_errors(self):
    return set.union(
      super().get_available_errors(),
      {
        account_anonymous_method_errors.PUBLIC_KEY_NOT_INCLUDED(),
        account_anonymous_method_errors.ACCOUNT_ALREADY_EXISTS(),
        account_anonymous_method_errors.IP_ALREADY_EXISTS(),
      },
    )

  def passes_pre_response_checks(self, payload, context):
    passes_pre_response_checks = super().passes_pre_response_checks(payload, context)

    if account_fields.PUBLIC_KEY not in payload:
      self.active_response.add_error(
        account_anonymous_method_errors.PUBLIC_KEY_NOT_INCLUDED(),
      )
      return False

    return passes_pre_response_checks

  def responds_to_valid_payload(self, payload, context):
    super().responds_to_valid_payload(payload, context)

    if self.active_response.has_errors():
      return

    existing_ip = IP.objects.get(value=context.connection.ip_value)
    if existing_ip is not None:
      self.active_response.add_error(
        account_anonymous_method_errors.IP_ALREADY_EXISTS(ip=context.connection.ip_value),
      )
      return

    public_key_response = self.active_response.get_child(account_fields.PUBLIC_KEY)
    public_key = public_key_response.render()
    public_key_long_key_id = public_key_response.get_long_key_id()

    existing_account = self.model.objects.get(long_key_id=public_key_long_key_id)
    if existing_account is not None:
      self.active_response.add_error(
        account_anonymous_method_errors.ACCOUNT_ALREADY_EXISTS(),
      )
      return

    account = self.model.objects.create(
      public_key=public_key,
      long_key_id=public_key_long_key_id,
    )
    ip = account.ips.create(value=context.connection.ip_value)
    context.connection.ip = ip
    context.connection.save()

    active_system = System.objects.active()
    self.active_response = self.client.respond(
      payload={
        create_constants.DISCLAIMER: active_system.disclaimer,
        create_constants.IP: context.connection.ip_value,
        create_constants.LONG_KEY_ID: public_key_long_key_id,
      },
    )
