from django.forms.widgets import Widget
from django.utils import datetime_safe, formats, six
from django.utils.html import conditional_escape, format_html
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.forms.util import flatatt

class FilePicker(Widget):
    def __init__(self, attrs=None):
        default_attrs = {}
        if attrs:
            default_attrs.update(attrs)
        super(FilePicker, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return format_html('<div{0}>\r\n{1}</div>',
                           flatatt(final_attrs),
                           force_text(value))


class NullWidget(Widget):
    def __init__(self, attrs=None):
        default_attrs = {}
        if attrs:
            default_attrs.update(attrs)
        super(NullWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return format_html('<div{0}>\r\n{1}</div>',
                           flatatt(final_attrs),
                           force_text(value))