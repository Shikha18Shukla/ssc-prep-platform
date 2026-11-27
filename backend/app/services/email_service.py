"""Minimal, opt-in email delivery for password setup/recovery.

The default provider is ``none``: it sends nothing and callers must say so.
Only SMTP configuration supplied through server-side environment variables is
supported. Reset tokens are never logged and are only placed in the message
delivered to the account address.
"""

from email.message import EmailMessage
import smtplib
import ssl
from typing import Protocol

from app.config import settings


class EmailDeliveryError(Exception):
    """Raised when a configured provider cannot deliver a message."""


class EmailSender(Protocol):
    """Delivery integration point for password recovery messages."""

    def send_password_reset(self, to_email: str, reset_url: str) -> bool:
        """Return True when a provider accepted the message."""


class NoopEmailSender:
    """Default provider: no email is sent and no success is claimed."""

    def send_password_reset(self, to_email: str, reset_url: str) -> bool:
        return False


class SMTPEmailSender:
    """Standards-library SMTP provider using TLS credentials from settings."""

    def send_password_reset(self, to_email: str, reset_url: str) -> bool:
        message = EmailMessage()
        message["Subject"] = "SSC Prep password setup"
        message["From"] = settings.SMTP_FROM_EMAIL or ""
        message["To"] = to_email
        message.set_content(
            "Use the link below to set or reset your SSC Prep password.\n\n"
            f"{reset_url}\n\n"
            "This link is single-use and expires soon. If you did not request it, ignore this message.\n"
        )

        host = settings.SMTP_HOST or ""
        username = settings.SMTP_USERNAME or ""
        password = settings.SMTP_PASSWORD or ""
        context = ssl.create_default_context()
        try:
            if settings.SMTP_USE_STARTTLS:
                with smtplib.SMTP(host, settings.SMTP_PORT, timeout=10) as smtp:
                    smtp.ehlo()
                    smtp.starttls(context=context)
                    smtp.ehlo()
                    smtp.login(username, password)
                    smtp.send_message(message)
            else:
                with smtplib.SMTP_SSL(host, settings.SMTP_PORT, timeout=10, context=context) as smtp:
                    smtp.login(username, password)
                    smtp.send_message(message)
        except Exception as exc:
            raise EmailDeliveryError("Password setup email could not be delivered") from None
        return True


def get_email_sender() -> EmailSender:
    """Return the configured delivery provider."""
    if settings.EMAIL_PROVIDER == "smtp":
        return SMTPEmailSender()
    return NoopEmailSender()
