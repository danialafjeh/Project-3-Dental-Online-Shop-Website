from django import template

register = template.Library()

@register.filter
def my_intcomma(value):
    """
    جدا کردن سه‌رقمی اعداد مثل intcomma
    مثال: 1234567 -> 1,234,567
    """
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value

    # حذف .0 در صورتی که عدد اعشاری نیست
    if value.is_integer():
        value = int(value)

    # تبدیل به رشته و جداسازی سه‌رقمی
    return f"{value:,}"
