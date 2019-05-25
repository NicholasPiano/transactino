
from constants import method_constants
from .constants import fee_report_constants
from .create import create
from .get import get
from .activate import activate
from .delete import delete

def fee_report(args):
  if method_constants.CREATE in args:
    create(args)
  if method_constants.GET in args:
    get(args)
  if fee_report_constants.ACTIVATE in args:
    activate(args)
  if method_constants.DELETE in args:
    delete(args)
