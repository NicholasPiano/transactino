
from apps.base.constants import model_fields
from apps.base.schema.constants import schema_constants
from apps.base.schema.methods.constants import method_constants
from apps.subscription.models import Payment, Subscription

from ..models import FeeReport
from .constants import api_constants

class ConsumerMethodsMixin():
  def send_fee_report(self, event):
    report_id = event.get(socket_constants.DATA)
    report = FeeReport.objects.get(id=report_id)

    payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          FeeReport.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {
                model_fields.ID: report._id,
              },
            },
          },
        },
      },
    }

    self.send_payload(payload=payload)

  def send_payment(self, event):
    payment_id = event.get(socket_constants.DATA)
    payment = Payment.objects.get(id=payment_id)

    payload = {
      api_constants.SCHEMA: {
        api_constants.MODELS: {
          Payment.__name__: {
            schema_constants.METHODS: {
              method_constants.GET: {
                model_fields.ID: payment._id,
              },
            },
          },
        },
      },
    }

    self.send_payload(payload=payload)
