from html import escape
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.schemas.auth import SUPPORTED_UI_LOCALES
from app.services import email_service
from app.services.email_service import _render_template, _safe_html


def test_render_template_escapes_user_controlled_values():
    html = _render_template(
        "contact.html",
        {
            "email_title": "Contact",
            "logo": "FreeLingo",
            "from_label": "From",
            "subject_label": "Subject",
            "message_label": "Message",
            "sender_email": 'attacker@example.com"><img src=x onerror=alert(1)>',
            "subject": '<a href="https://phishing.example">Click</a>',
            "description": "<strong>urgent</strong> & dangerous",
            "footer": "Footer",
            "base_url": "https://freelingo.example",
        },
    )

    assert "<img src=x onerror=alert(1)>" not in html
    assert '<a href="https://phishing.example">Click</a>' not in html
    assert "<strong>urgent</strong>" not in html
    assert '<html lang="en">' in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html
    assert "&lt;a href=&quot;https://phishing.example&quot;&gt;Click&lt;/a&gt;" in html
    assert "&lt;strong&gt;urgent&lt;/strong&gt; &amp; dangerous" in html


@pytest.mark.parametrize("locale", [*sorted(SUPPORTED_UI_LOCALES), "unsupported"])
@pytest.mark.parametrize(
    ("send", "args", "catalog"),
    [
        (
            email_service.send_verification_email,
            ("student@example.com", "Student", "test-token"),
            email_service._VERIFY_I18N,
        ),
        (
            email_service.send_reset_password_email,
            ("student@example.com", "Student", "test-token"),
            email_service._RESET_I18N,
        ),
        (
            email_service.send_welcome_email,
            ("student@example.com", "Student"),
            email_service._WELCOME_I18N,
        ),
        (
            email_service.send_account_deleted_email,
            ("student@example.com", "Student"),
            email_service._DELETION_I18N,
        ),
        (
            email_service.send_contact_email,
            ("student@example.com", "Subject", "Description"),
            email_service._CONTACT_I18N,
        ),
        (
            email_service.send_feedback_notification,
            ("feature", "Title", "Description", "student", 1),
            email_service._FEEDBACK_I18N,
        ),
        (
            email_service.send_review_notification,
            ("Student", 5, None, "en-GB", 1),
            email_service._REVIEW_I18N,
        ),
    ],
    ids=["verification", "reset", "welcome", "deletion", "contact", "feedback", "review"],
)
async def test_email_declares_the_language_of_its_rendered_content(
    monkeypatch, locale, send, args, catalog
):
    send_message = AsyncMock()
    monkeypatch.setattr(email_service.settings, "EMAIL_ENABLED", True)
    monkeypatch.setattr(email_service.settings, "CONTACT_EMAIL", "admin@example.com")
    monkeypatch.setattr(email_service, "_get_mail_config", lambda: None)
    monkeypatch.setattr(
        email_service, "FastMail", lambda _: SimpleNamespace(send_message=send_message)
    )

    await send(*args, locale=locale)

    send_message.assert_awaited_once()
    message = send_message.await_args.args[0]
    expected_locale = locale if locale in SUPPORTED_UI_LOCALES else "en"
    assert f'<html lang="{expected_locale}">' in message.body
    assert escape(catalog[expected_locale]["footer"], quote=True) in message.body
    assert "{{" not in message.body


def test_render_template_preserves_explicitly_trusted_html():
    html = _render_template(
        "verify_email.html",
        {
            "greeting": "Hi Student,",
            "body": _safe_html("Welcome.<br /><strong>Verify now</strong>"),
            "button": "Verify",
            "link_fallback": "Copy this link:",
            "footer": "Footer",
            "url": "https://freelingo.example/verify-email?token=abc123",
            "base_url": "https://freelingo.example",
        },
    )

    assert "Welcome.<br /><strong>Verify now</strong>" in html
    assert "Welcome.&lt;br /&gt;&lt;strong&gt;Verify now&lt;/strong&gt;" not in html


def test_review_template_escapes_review_fields():
    html = _render_template(
        "review_submitted.html",
        {
            "email_title": "Review",
            "logo": "FreeLingo",
            "author_label": "Submitted by",
            "user_display_name": "<img src=x onerror=alert(1)>",
            "rating_label": "Rating",
            "rating": "5/5",
            "language_label": "Learning language",
            "target_language": "en-US",
            "comment_label": "Comment",
            "comment": '<a href="https://phishing.example">Click</a>',
            "cta": "View",
            "admin_url": "https://freelingo.example/admin/reviews",
            "footer": "Footer",
            "base_url": "https://freelingo.example",
        },
    )

    assert "<img src=x onerror=alert(1)>" not in html
    assert '<a href="https://phishing.example">Click</a>' not in html
    assert "&lt;img src=x onerror=alert(1)&gt;" in html
    assert "&lt;a href=&quot;https://phishing.example&quot;&gt;Click&lt;/a&gt;" in html
