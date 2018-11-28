
from .constants import fee_report_constants
from .create import create
from .get import get

def fee_report(args):
  if fee_report_constants.CREATE in args:
    create(args)
  if fee_report_constants.GET in args:
    get(args)
