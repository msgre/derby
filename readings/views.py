# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.views.generic import ListView
from django.http import Http404
from django.db.models import Sum

from childrens.models import Children
from .models import ReadingsTerm, ReadingsRecord

DEFAULT_COLOR = '#336699'

class BaseReadingView(ListView):

    def __init__(self, *args, **kwargs):
        super(BaseReadingView, self).__init__()
        self.childrens = {i.id: i for i in Children.objects.all()}

    def get_next_month(self, actual):
        """
        Vrati prvni den nasledujiciho mesice vuci `actual`.
        """
        out = actual + timedelta(days=40)
        return datetime(out.year, out.month, 1)

    def get_stats(self, date_from, date_to):
        """
        Vraci statistiku cteni pro zadane obdobi <date_from, date_to).

        Bacha! Pokud chci cele zari tak zadam <1.9., 1.10)!
        Bacha! Pokud bude v databazi zaznam treba pro 28.9 az 4.10, tak se
        do statistik nezapocte! Data v DB musi byt narezene na konce
        sledovanych obdobi (v pripade mesicu na mesice; v pripade tydnu
        by to byly tydny).

        Vraci seznam, ve kterem jsou zaznamy serazene podle poctu minut,
        od nejvetsiho po nejmensi. Co prvek, to:

            {
                'children': instance modelu Children (tj. podrobnosti o decku)
                'minutes':  pocet minut co decko precetlo
                'hours':    pocet hodin co decko precetlo (prepocitany klic 'minutes')
            }
        """
        # seznam terminu, ktere spadaji do zadaneho obdobi
        # NOTE: bacha! nevezme to terminy, ktere lezi pres nekterou z hranic
        terms = ReadingsTerm.objects.filter(date_from__gte=date_from, date_to__lt=date_to)

        # vytahnem si statistiky cteni a seradime je podle casu
        stats = ReadingsRecord.objects.filter(term__id__in=terms.values_list('id', flat=True))\
                                      .values('children')\
                                      .annotate(minutes=Sum('minutes'))\
                                      .order_by('children')
        stats = sorted(stats, cmp=lambda a, b: cmp(a['minutes'], b['minutes']), reverse=True)

        # vytvorime finalni set
        out = [{'children': self.childrens[i['children']],
                'id': i['children'],
                'minutes': i['minutes'],
                'hours': i['minutes'] / 60.0} for i in stats]

        return out

    def get_term_stats(self, date_from, date_to):
        """
        Udaje o terminu.
        """
        terms = ReadingsTerm.objects.filter(date_from__gte=date_from, date_to__lt=date_to).order_by('date_from')
        term = terms[0].get_year_interval()
        out = {'note': [], 'length': 1, 'year_from': term[0], 'year_to': term[1]}
        for term in terms:
            if term.note:
                out['note'].append(term.note)
            if term.length > out['length']:
                out['length'] = term.length
        out['note'] = u'<br>'.join(out['note'])
        return out

    def separate_stats(self, stats, limit=3):
        """
        Ze zadane statistiky oddeli zvlast zaznamy pro holky a kluky,
        pricemz vraci pouze `limit` prvnich zaznamu.
        """
        boys = [i for i in stats if i['children'].sex == 'M'][:limit]
        girls = [i for i in stats if i['children'].sex == 'F'][:limit]
        return (boys, girls)


class YearlyReadingsView(BaseReadingView):
    """
    Prehled cteni za cely skolni rok.
    """
    template_name = 'readings/yearly.html'
    context_object_name = 'months'

    def get_queryset(self):
        # mantinely celeho skolniho roku
        (self.year_date_from, self.year_date_to) = self.get_terms()

        # seznam obdobi, ve kterem decka neco cetla
        dates = ReadingsTerm.objects.filter(date_from__gte=self.year_date_from, \
                                            date_to__lt=self.year_date_to)\
                                    .dates('date_from', 'month').order_by('-date_from')

        # nejlepsi ctenari za jednotliva obdobi (mesice), rozdeleno na holky/kluky
        self.terms = []
        for date_from in dates:
            date_to = self.get_next_month(date_from)
            stats = self.get_stats(date_from, date_to)
            (boys, girls) = self.separate_stats(stats)
            self.terms.append({'date_from': date_from,
                               'date_to': date_to,
                               'boys': boys,
                               'girls': girls})

        # nejlepsi ctenari celeho roku
        self.total = self.get_stats(self.year_date_from, self.year_date_to)[:10] # 10 nejlepsich

        return dates

    def get_total_hours(self):
        ids = ReadingsTerm.objects.filter(date_from__gte=self.year_date_from, \
                                          date_to__lt=self.year_date_to).values_list('id', flat=True)
        minutes = ReadingsRecord.objects.filter(term__id__in=ids).aggregate(Sum('minutes'))
        return minutes['minutes__sum'] / (60.0 * 24)


    def get_context_data(self, **kwargs):
        out = super(YearlyReadingsView, self).get_context_data(**kwargs)
        out.update({
            'year_date_from': self.year_date_from,
            'year_date_to': self.year_date_to,
            'terms': self.terms,    # statistiky po mesicich
            'total': self.total,    # celkove statistiky za skolni rok
            'total_hours': self.get_total_hours(),
        })
        return out

    def get_terms(self):
        """
        Pomocna metoda, vraci limitni data pro skolni rok (dle parametru v URL).
        """
        if int(self.kwargs['year_start']) + 1 != int(self.kwargs['year_end']):
            raise Http404
        start = datetime(int(self.kwargs['year_start']), 9, 1)
        end = datetime(int(self.kwargs['year_end']), 7, 1)
        return (start, end)


class MonthlyReadingsView(BaseReadingView):
    """
    Detailni informace o prubehu cteni v ramci jednoho mesice.
    """
    template_name = 'readings/monthly.html'
    context_object_name = 'childrens'

    def get_queryset(self):
        # datum od
        try:
            self.date_from = datetime(int(self.kwargs['year']), int(self.kwargs['month']), 1)
        except ValueError:
            raise Http404

        # datum do
        self.date_to = self.get_next_month(self.date_from)
        return self.get_stats(self.date_from, self.date_to)

    def get_context_data(self, **kwargs):
        out = super(MonthlyReadingsView, self).get_context_data(**kwargs)
        out.update({
            'term_stats': self.get_term_stats(self.date_from, self.date_to),
            'date_from': self.date_from,
            'DEFAULT_COLOR': DEFAULT_COLOR
        })
        return out
