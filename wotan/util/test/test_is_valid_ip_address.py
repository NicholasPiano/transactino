
from django.test import TestCase
from ..is_valid_ip_address import is_valid_ip_address

class IsValidIpAddressTestCase(TestCase):
  def test_valid_ip_addresses(self):
    valid_ip_addresses = [
      '123.123.123.123',
      '1.2.3.123',
      '234.1.2.22',
    ]

    for valid_ip_address in valid_ip_addresses:
      self.assertTrue(is_valid_ip_address(valid_ip_address))

  def test_invalid_uuid(self):
    invalid_ip_addresses = [
      'some value',
      '1.2.1.',
      '2.3.2',
      '1234.1.1.2',
    ]

    for invalid_ip_address in invalid_ip_addresses:
      self.assertFalse(is_valid_ip_address(invalid_ip_address))
