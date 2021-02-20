from django.db import models as m


class Grantmaker(m.Model):
    name = m.CharField(max_length=250)
    kind = m.CharField(max_length=20,
                       choices=[("OPEN", "Open"),
                                ("PRIVATE", "Private"),
                                ("GOVT", "Government")])
    description = m.CharField(max_length=2500, null=True)
    mission = m.CharField(max_length=5000, null=True)
    address = m.CharField(max_length=250, null=True)
    address2 = m.CharField(max_length=250, null=True)
    city = m.CharField(max_length=250, null=True)
    state = m.CharField(max_length=20, null=True)
    zip_code = m.CharField(max_length=20, null=True)
    country = m.CharField(max_length=250, null=True)
    email = m.CharField(max_length=250, null=True)
    url = m.CharField(max_length=250, null=True)
    phone = m.CharField(max_length=20, null=True)
    extension = m.CharField(max_length=20, null=True)


class Grant(m.Model):
    grantmaker = m.ForeignKey('Grantmaker', on_delete=m.CASCADE)
    name = m.CharField(max_length=250)
    description = m.CharField(max_length=2500, null=True)
    deadline = m.DateTimeField(null=True)
    restricted = m.CharField(max_length=20,
                             choices=[("YES", "Restricted"),
                                      ("NO", "Unrestricted"),
                                      ("UNK", "Unknown")])
    restrictions = m.CharField(max_length=5000, null=True)


# Valid status strings include: "not applied", "in progress," "loi submitted",
# "submitted", "rejected", "offered", "accepted", "received in part", and
# "received in full." Each might have an amount of money, and each might
# have details.
#
# I think it'll be more elegant to let the abstraction layer enforce what must
# and may not have what values, but here's the list for documentation purposes.
#
# Statuses
#
# not applied: none
# in progress: amount (desired ask), details (notes)
# loi submitted: details (notes)
# submitted: amount (ask made), details (notes)
# rejected: details (reason)
# offered: amount (give offered), details (notes)
# accepted: details (notes)
# received: amount (give received), details (notes)
#     There may be multiple received statuses between an accepted status and the
#     next cycle's in progress status. Each represents one check or other form of
#     disbursement submitted by the grantor. A discrepancy here between amount
#     offered and the sum of amounts received can indicate an accounting concern.
class Status(m.Model):
    grant = m.ForeignKey('Grant', on_delete=m.CASCADE)
    status = m.CharField(max_length=50,
                         choices=[("LOISENT", "Letter of Intent Sent"),
                                  ("LOIACCEPTED", "Letter of Intent Accepted"),
                                  ("INPROGRESS", "Application in progress"),
                                  ("SUBMITTED", "Submitted"),
                                  ("REJECTED", "Rejected"),
                                  ("OFFERED", "Offered"),
                                  ("ACCEPTED", "Accepted"),
                                  ("RECEIVED", "Received")])
    amount = m.DecimalField(max_digits=18,
                            decimal_places=2,
                            null=True)
    details = m.CharField(max_length=5000,
                          null=True)
    updated_on = m.DateTimeField(auto_now_add=True)


class Obligation(m.Model):
    grant = m.ForeignKey('Grant', on_delete=m.CASCADE)
    due = m.DateTimeField(null=True)
    title = m.CharField(max_length=250)
    details = m.CharField(max_length=5000,
                          null=True)
    fulfilled = m.BooleanField(default=False)