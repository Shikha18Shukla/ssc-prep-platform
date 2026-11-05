"""Production beta allowlist for completed SSC catalog sections."""

from app.config import settings

_SUBJECTS = {"maths", "reasoning", "gk-gs"}
_GK_SUBCATEGORIES = {"science"}


def subject_is_in_beta(exam_slug: str, subject_slug: str) -> bool:
    return (
        not settings.BETA_CATALOG_SCOPE
        or (exam_slug == "ssc" and subject_slug in _SUBJECTS)
    )


def subcategory_is_in_beta(subject_slug: str, subcategory_slug: str) -> bool:
    if not settings.BETA_CATALOG_SCOPE:
        return True
    if subject_slug == "gk-gs":
        return subcategory_slug in _GK_SUBCATEGORIES
    return subject_slug in _SUBJECTS


def chapter_is_in_beta(exam_slug: str, subject_slug: str, subcategory_slug: str | None) -> bool:
    if not settings.BETA_CATALOG_SCOPE:
        return True
    if not subject_is_in_beta(exam_slug, subject_slug):
        return False
    return subject_slug != "gk-gs" or subcategory_slug in _GK_SUBCATEGORIES
