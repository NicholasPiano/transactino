
from .constants import transaction_report_constants
from .create import create
from .get import get
from .activate import activate
from .delete import delete

def transaction_report(args):
  if transaction_report_constants.CREATE in args:
    create(args)
  if transaction_report_constants.GET in args:
    get(args)
  if transaction_report_constants.ACTIVATE in args:
    activate(args)
  if transaction_report_constants.DELETE in args:
    delete(args)
