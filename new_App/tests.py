import shutil
import tempfile

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage, NewsletterSubscriber, PDFDocument

TEST_MEDIA = tempfile.mkdtemp(prefix="fgen-test-media-")


@override_settings(
    SECURE_SSL_REDIRECT=False,
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    MEDIA_ROOT=TEST_MEDIA,
    SITE_URL="https://www.fgen.ca",
)
class SiteSmokeTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA, ignore_errors=True)

    def test_healthz(self):
        r = self.client.get("/healthz/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {"status": "ok"})

    def test_public_pages_render(self):
        for name in ("home", "about_us", "programs", "events", "contact_us", "contact_success"):
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_admin_login_page(self):
        self.assertEqual(self.client.get("/admin/login/").status_code, 200)

    def test_contact_form_saves_and_notifies(self):
        r = self.client.post(
            reverse("contact_us"),
            {
                "name": "Test Person",
                "email": "test@example.com",
                "subject": "general_inquiry",
                "other_subject": "",
                "message": "Hello from CI",
            },
        )
        self.assertRedirects(r, reverse("contact_success"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_newsletter_signup(self):
        r = self.client.post(reverse("newsletter_signup"), {"email": "reader@example.com"})
        self.assertRedirects(r, reverse("home"))
        self.assertTrue(NewsletterSubscriber.objects.filter(email="reader@example.com").exists())

    def test_uploads_go_to_local_media_and_email_links_are_absolute(self):
        NewsletterSubscriber.objects.create(email="reader@example.com")
        doc = PDFDocument.objects.create(
            title="Spring",
            file=SimpleUploadedFile("spring.pdf", b"%PDF-1.4 test", content_type="application/pdf"),
        )
        self.assertTrue(doc.file.url.startswith("/media/pdfs/"))
        self.assertTrue(doc.file.storage.exists(doc.file.name))
        self.assertIn("https://www.fgen.ca/media/pdfs/", mail.outbox[-1].body)
