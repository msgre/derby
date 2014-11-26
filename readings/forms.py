# -*- coding: utf-8 -*-

from django import forms
from django.forms.utils import ErrorList

from .models import ReadingsRecord, ReadingsTerm
from childrens.models import Children


class PErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return u''.join(['<p style="padding-top:5px;color:red">%s</p>' % e for e in self])


class ReadingForm(forms.Form):
    """
    Dynamicky formular, ktery vytvori sadu integer policek "minutes_X",
    kde X je ID ditete. Potrebuje dodat parametr "childrens" s querysetem
    deti.
    """
    length = forms.IntegerField(label=u"Délka tratě (v minutách)", initial=500, widget=forms.NumberInput(attrs={'class': 'form-control input-sm'}))
    note = forms.CharField(label=u"Poznámka", required=False, widget=forms.Textarea(attrs={'class': 'form-control input-sm', 'rows': '3'}))

    def __init__(self, *args, **kwargs):
        self.excluded_fields = ['length', 'note']
        kwargs['error_class'] = PErrorList
        childrens = kwargs.pop('childrens')
        self.terms = kwargs.pop('terms')
        super(ReadingForm, self).__init__(*args, **kwargs)
        for child in childrens:
            widget = forms.NumberInput(attrs={'class': 'form-control input-sm'})
            self.fields['minutes_%i' % child.id] = forms.IntegerField(initial=0, widget=widget)
            self.fields['add_%i' % child.id] = forms.IntegerField(initial=0, widget=widget)

    def clean(self):
        cleaned_data = self.cleaned_data
        keys = cleaned_data.keys()
        for k in keys:
            if k == 'note':
                continue
            if cleaned_data[k] < 0:
                self.add_error(k, u"Políčko obsahuje záporné číslo.")
            elif cleaned_data[k] > 10000:
                self.add_error(k, u"Políčko obsahuje moc velké číslo.")
        return cleaned_data

    def save(self, *args, **kwargs):
        # ulozeni minut
        ids = set([int(i.split('_')[-1]) for i in self.cleaned_data.keys() if i not in self.excluded_fields])
        for _id in ids:
            minutes = self.cleaned_data['minutes_%i' % _id] + self.cleaned_data['add_%i' % _id]
            for term_id in self.terms:
                try:
                    record = ReadingsRecord.objects.get(children__id=_id, term__id=term_id)
                except ReadingsRecord.DoesNotExist:
                    record = ReadingsRecord(children=Children.objects.get(id=_id),
                                            term=ReadingsTerm.objects.get(id=term_id))
                record.minutes = minutes
                record.save()
        # ulozeni udaju o terminu
        self.terms.update(length=self.cleaned_data['length'], note=self.cleaned_data['note'])
