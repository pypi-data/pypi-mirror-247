import requests_mock
from django.test import SimpleTestCase, TestCase
from wagtail.coreutils import get_dummy_request
from wagtail.models import Site

from wagtail_indexnow import wagtail_hooks
from wagtail_indexnow.utils import get_key

from .models import TestPage


class KeyTestCase(SimpleTestCase):
    def test_stable_key(self):
        self.assertEqual(get_key(), get_key())


class KeyViewTestCase(SimpleTestCase):
    def test_returns_key(self):
        response = self.client.get(f"/indexnow-{get_key()}.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), get_key())

    def test_incorrect_key(self):
        response = self.client.get("/indexnow-notthekey.txt")
        self.assertEqual(response.status_code, 404)


@requests_mock.Mocker()
class IndexNowTestCase(TestCase):
    def setUp(self):
        self.root_page = Site.objects.first().root_page

        self.root_page.add_child(instance=TestPage(title="Test page"))

        self.page = self.root_page.get_children().get()

    def test_pings(self, m):
        m.register_uri("POST", "https://api.indexnow.org/indexnow")

        setattr(self.page, wagtail_hooks.SHOULD_NOTIFY_PAGE_ATTRIBUTE, True)

        wagtail_hooks.notify_indexnow(get_dummy_request(), self.page)

        self.assertEqual(m.call_count, 1)

        self.assertEqual(
            m.request_history[0].json(),
            {
                "host": "localhost",
                "urlList": [self.page.full_url],
                "key": "indexnow-" + get_key(),
            },
        )

    def test_noop_if_should_not_notify(self, m):
        setattr(self.page, wagtail_hooks.SHOULD_NOTIFY_PAGE_ATTRIBUTE, False)

        wagtail_hooks.notify_indexnow(get_dummy_request(), self.page)

        self.assertEqual(m.call_count, 0)
