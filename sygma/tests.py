import json, decimal
from datetime import datetime, timedelta
from . import views as v
from . import models as m
from django.test import TestCase, Client, RequestFactory
request_factory = RequestFactory()


class GrantmakersViewTestCase(TestCase):
    # TODO: Expand beyond the happy path tests.
    def setUp(self):
        self.gm = m.Grantmaker(name="The Feelgood Foundation",
                               kind="private")
        self.gm.save()
        self.known_id = self.gm.pk

    @staticmethod
    def test_post_new():
        """A post request with no id but which has required fields inserts a new row."""
        req = request_factory.post('/grantmaker/',
                                   {
                                       "name": "The Okay Foundation",
                                       "kind": "private"
                                   })
        res = v.grantmaker(req)
        assert res.status_code == 200

        content = json.loads(v.grantmaker(req).content)
        assert "The Okay Foundation" in content[0]['fields']['name']

    @staticmethod
    def test_post_new_invalid():
        no_name = {
            "kind": "private"
        }
        name_is_int = {
            "name": 42,
            "kind": "PRIVATE"
        }
        no_kind = {
            "name": "Nasty Foundation"
        }
        kind_is_int = {
            "name": "Nasty Foundation",
            "kind": 298
        }

        assert v.grantmaker(request_factory.post('/grantmaker/', no_name)).status_code == 400
        assert v.grantmaker(request_factory.post('/grantmaker/', name_is_int)).status_code == 400
        assert v.grantmaker(request_factory.post('/grantmaker/', no_kind)).status_code == 400
        assert v.grantmaker(request_factory.post('/grantmaker/', kind_is_int)).status_code == 400

    def test_get_one(self):
        """A GET request with a valid id--which exists--will return that row."""
        req = request_factory.get('/grantmaker/',
                                  {
                                      "id": self.known_id
                                  })
        res = v.grantmaker(req)
        assert res.status_code == 200
        assert json.loads(res.content)[0]['pk'] == self.known_id

    def test_get_one_invalid(self):
        does_not_exist = {
            "id": 9999
        }
        invalid_id = {
            "id": "fruitcake"
        }
        assert v.grantmaker(request_factory.get('/grantmaker/', does_not_exist)).status_code == 404
        assert v.grantmaker(request_factory.get('/grantmaker/', invalid_id)).status_code == 400

    def test_post_update(self):
        """A POST request with a valid id--which exists--will update that row."""
        req = request_factory.post('/grantmaker',
                                   {
                                       "id": self.known_id,
                                       "mission": "Feel good, man!"
                                   })
        res = v.grantmaker(req)

        assert res.status_code == 200
        assert "good" in json.loads(res.content)[0]['fields']['mission']

    def test_post_delete(self):
        """A POST request to /grantmaker/delete/ with a valid id will delete that row."""
        req = request_factory.post('/grantmaker/delete',
                                   {
                                       "id": self.known_id
                                   })
        res = v.delete_grantmaker(req)
        assert res.status_code == 200

        res2 = request_factory.get('/grantmaker/',
                                   {
                                       "id": self.known_id
                                   })
        assert v.grantmaker(res2).status_code == 404

    def test_get_all(self):
        """A GET request to /grantmakers/ will return all known grantmakers."""
        req = request_factory.get('/grantmakers/')
        res = v.grantmakers(req)
        assert "Feel" in json.loads(res.content)[0]['fields']['name']


class GrantViewTestCase(TestCase):
    def setUp(self):
        # Create an imaginary grantmaker
        self.gm = m.Grantmaker(name="The Feelgood Foundation",
                               kind="private")
        self.gm.save()

        # Give them an imaginary grant
        self.g = m.Grant(grantmaker=self.gm,
                         name="Feelin' Fine Funds",
                         restricted="NO")
        self.g.save()

    def test_select_one(self):
        """A GET request specifying our example grant's id will return it."""
        req = request_factory.get('/grant/',
                                  {
                                      "id": self.g.pk
                                  })
        res = v.grant(req)
        assert res.status_code == 200

        result = json.loads(res.content)[0]
        assert "Fine" in result['fields']['name']

    def test_select_all(self):
        """A GET request to /grants/ will return a list of all grants."""
        req = request_factory.get('/grants/')
        res = v.grants(req)
        assert "Fine" in json.loads(res.content)[0]['fields']['name']

    def test_post_new(self):
        new_data = {
            "grantmaker": self.gm.pk,
            "name": "Doing Decent Disbursement",
            "restricted": "YES"
        }
        req = request_factory.post('/grant/', new_data)
        res = v.grant(req)

        assert res.status_code == 200
        assert "Decent" in json.loads(res.content)[0]['fields']['name']
        pass

    def test_post_update(self):
        better_data = {
            "id": self.g.pk,
            "description": "It's all about feeling fine, you know?"
        }
        req = request_factory.post('/grant/', better_data)
        res = v.grant(req)

        assert res.status_code == 200
        assert "know" in json.loads(res.content)[0]['fields']['description']
        #raise ValueError(json.loads(res.content)[0]['fields'])

    def test_post_delete(self):
        # Try to delete it
        dead_data = {
            "id": self.g.pk
        }
        req = request_factory.post('/grant/delete/', dead_data)
        res = v.delete_grant(req)
        assert res.status_code == 200

        # Make sure it's gone
        req2 = request_factory.get('/grant/', dead_data)
        res2 = v.grant(req2)
        assert res2.status_code == 404


class StatusViewTestCase(TestCase):
    def setUp(self):
        # Create an imaginary grantmaker
        self.gm = m.Grantmaker(name="The Feelgood Foundation",
                               kind="private")
        self.gm.save()

        # Give them an imaginary grant
        self.g = m.Grant(grantmaker=self.gm,
                         name="Feelin' Fine Funds",
                         restricted="NO")
        self.g.save()

        self.s = m.Status(grant=self.g,
                          status="SUBMITTED",
                          amount=decimal.Decimal(20000.00),
                          details="Askin' for those feelgood funds")
        self.s.save()

    def test_select_one(self):
        req_data = {
            "id": self.g.pk
        }
        req = request_factory.get('/status/', req_data)
        res = v.status(req)

        assert res.status_code == 200
        assert "feelgood" in json.loads(res.content)[0]['fields']['details']

    def test_select_one_invalid(self):
        id_is_string = {
            "id": "kerfluffle"
        }
        id_is_missing = {}
        id_is_empty_str = {
            "id": ""
        }
        assert v.status(request_factory.get('/status/', id_is_string)).status_code == 400
        assert v.status(request_factory.get('/status/', id_is_missing)).status_code == 400
        assert v.status(request_factory.get('/status/', id_is_empty_str)).status_code == 400

    def test_select_all(self):
        """Make a select * request from statuses.
        TODO: Add various filters"""
        req = request_factory.get('/statuses/')
        res = v.statuses(req)

        assert res.status_code == 200
        assert "feelgood" in json.loads(res.content)[0]['fields']['details']

    def test_select_by_grant(self):
        # specify a grant.id to select by
        req = request_factory.get('/status/', {
            "grant": self.g.pk
        })
        res = v.status(req)

        assert res.status_code == 200
        assert "feelgood" in json.loads(res.content)[0]['fields']['details']

    def test_post_new(self):
        req_data = {
            "grant": self.g.pk,
            "status": "ACCEPTED",
            "amount": 25000.00,
            "details": "SO many good feels inbound"
        }
        req = request_factory.post('/status', req_data)
        res = v.status(req)

        assert res.status_code == 200
        assert "feels" in json.loads(res.content)[0]['fields']['details']

    def test_post_update(self):
        req_data = {
            "id": self.s.pk,
            "details": "Awful lotta good feels inbound"
        }
        req = request_factory.post('/status', req_data)
        res = v.status(req)
        assert res.status_code == 200
        assert "lotta" in json.loads(res.content)[0]['fields']['details']

    def test_post_delete(self):
        req_data = {
            "id": self.g.pk
        }
        req = request_factory.post('/status/delete/', req_data)
        res = v.delete_status(req)

        assert res.status_code == 200

        req2 = request_factory.get('/status/', req_data)
        res2 = v.status(req2)


class ObligationViewTestCase(TestCase):
    def setUp(self):
        # Create an imaginary grantmaker
        self.gm = m.Grantmaker(name="The Feelgood Foundation",
                               kind="private")
        self.gm.save()

        # Give them an imaginary grant
        self.g = m.Grant(grantmaker=self.gm,
                         name="Feelin' Fine Funds",
                         restricted="NO")
        self.g.save()

        self.s = m.Status(grant=self.g,
                          status="SUBMITTED",
                          amount=20000.00,
                          details="Askin' for those feelgood funds")
        self.s.save()

        six_days_from_now = str(datetime.now() + timedelta(days=6))
        self.o = m.Obligation(grant=self.g,
                              kind="REPORT",
                              due=six_days_from_now,
                              title="Talk about the vibes")
        self.o.save()

    def test_get_by_id(self):
        req = request_factory.get('/obligation/',
                                  {
                                      "id": self.o.pk
                                  })
        res = v.obligation(req)
        assert res.status_code == 200
        assert "Talk" in json.loads(res.content)[0]['fields']['title']

    def test_get_by_grant(self):
        req = request_factory.get('/obligations/',
                                  {
                                      "grant": self.g.pk
                                  })
        res = v.obligations(req)
        assert res.status_code == 200
        assert "Talk" in json.loads(res.content)[0]['fields']['title']

    def test_get_by_grantmaker(self):
        req = request_factory.get('/obligations/',
                                  {
                                      "grantmaker": self.gm.pk
                                  })
        res = v.obligations(req)
        assert res.status_code == 200
        assert "Talk" in json.loads(res.content)[0]['fields']['title']

    def test_get_all(self):
        req = request_factory.get('/obligations/')
        res = v.obligations(req)
        assert res.status_code == 200
        assert "Talk" in json.loads(res.content)[0]['fields']['title']

    def test_get_next_n_days(self):
        req = request_factory.get('/obligations/',
                                  {
                                      "days": 7
                                  })
        res = v.obligations(req)
        assert res.status_code == 200
        assert "Talk" in json.loads(res.content)[0]['fields']['title']

    def test_post_new(self):
        req = request_factory.post('/obligation/',
                                   {
                                       "grant": self.g.pk,
                                       "kind": "COMMITMENT",
                                       "due": str(datetime.now() + timedelta(days=5)),
                                       "title": "Show we shared the feels."
                                   })
        res = v.obligation(req)
        assert res.status_code == 200
        assert "shared the f" in json.loads(res.content)[0]['fields']['title']

    def test_post_update(self):
        req = request_factory.post('/obligation/',
                                   {
                                       "id": self.o.pk,
                                       "details": "We're going alright on it."
                                   })
        res = v.obligation(req)
        assert res.status_code == 200
        assert "alright" in json.loads(res.content)[0]['fields']['details']

    def test_post_delete(self):
        good_id = self.o.pk
        req = request_factory.post('/obligation/delete/',
                                   {
                                       "id": good_id
                                   })
        res = v.delete_obligation(req)
        assert res.status_code == 200

        req2 = request_factory.get('/obligation/',
                                  {
                                      "id": good_id
                                  })
        res2 = v.obligation(req2)
        assert res2.status_code == 404
