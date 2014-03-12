from django.forms.widgets import Widget, TextInput, RadioChoiceInput, ChoiceInput
from django.utils import datetime_safe, formats, six
from django.utils.html import conditional_escape, format_html
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.forms.util import flatatt
from django.contrib.admin.widgets import *

from floppyforms.widgets import RadioSelect


class FilePicker(Widget):
    def __init__(self, attrs=None):
        default_attrs = {}
        if attrs:
            default_attrs.update(attrs)
        super(FilePicker, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        else:
            value = format_html('<div class="cloak"><img src="%s"/></div>' % value.url)

        final_attrs = self.build_attrs(attrs, name=name)
        if not final_attrs.has_key('class'):
            final_attrs['class'] = ''
        final_attrs['class'] += ' file-picker-input'
        return format_html('<div{0}>{1}</div>',
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


class TypeAheadWidget(TextInput):
    def __init__(self, attrs=None):
        default_attrs = {}
        if attrs:
            default_attrs.update(attrs)
        super(TypeAheadWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        real_final_atts = final_attrs.copy()
        real_final_atts['type'] = 'hidden'
        final_attrs['id'] += '_tt'
        final_attrs['name'] += '_tt'
        return format_html('<input{0} /><input{1} />', flatatt(real_final_atts), flatatt(final_attrs))


class TypeAheadAdminWidget(AdminTextInputWidget):
    def __init__(self, attrs=None):
        final_attrs = {'class': 'vTextField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(TypeAheadAdminWidget, self).__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        real_final_atts = final_attrs.copy()
        real_final_atts['type'] = 'hidden'
        final_attrs['id'] += '_tt'
        final_attrs['name'] += '_tt'
        return format_html('<input{0} /><input{1} />', flatatt(real_final_atts), flatatt(final_attrs))


class SometimeWidget(ChoiceInput):
    template_name = 'widgets/sometime.html'