
class TransactinoContext():
  def __init__(self, connection=None):
    self.connection = connection

  def get_ip(self):
    print(self.connection)
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
