
class TransactinoContext():
  def __init__(self, system=None, connection=None):
    self.system = system
    self.connection = connection

  def has_announcements(self):
    if self.system is None:
      return False

    return self.system.announcements.filter(is_active=True).exists()

  def get_ip(self):
    if self.connection is None:
      return None

    return self.connection.ip

  def get_account(self):
    ip = self.get_ip()
    if ip is None:
      return None

    return ip.account

  def is_anonymous(self):
    return self.get_account() is None

  def is_subscribed(self):
    if self.is_anonymous():
      return False

    return self.get_account().subscriptions.filter(is_active=True).exists()

  def is_locked(self):
    if self.is_anonymous():
      return False

    return self.get_account().is_locked

  def is_superadmin(self):
    if self.is_anonymous():
      return False

    return self.get_account().is_superadmin
