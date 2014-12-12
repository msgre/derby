# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.views.generic import FormView, View
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

from childrens.models import Children

from .models import ReadingsTerm, ReadingsRecord
from .forms import ReadingForm


def handle_terms(year_from, year_to):
    """
    Pomocnik pro automaticke generovani zaznamu ReadingsTerm.

    Nechtelo se mi delat explicitni formularove view pro zadani dalsiho obdobi
    (napr. mame v DB zaznamenany udaje pro zari, rijen, prijdu na stranky v
    pulce listopadu a musel bych udelat zaznam pro listopad manualne).

    Tahle funkce projede ReadingsTerm co mame ulozeny v DB, porovna to s
    aktualnim datumem a pokud zjisti, ze pro nejake obdobi chybi zaznam,
    tak ho dodela.
    """
    # nalezeni vsech zaznamu pro dany skolni rok
    date_from = datetime(year_from, 9, 1)
    date_to = datetime(year_to, 6, 1)
    terms = ReadingsTerm.objects.filter(date__gte=date_from, date__lte=date_to)
    now = datetime.now()

    # pomocna struktura
    dates = [str(i) for i in terms.dates('date', 'month')]

    # overeni datumu do vanoc
    for month in range(9, 12 + 1):
        d = datetime(year_from, month, 1)
        if str(d) not in dates:
            if d <= now and not ReadingsTerm.objects.filter(date=d).exists():
                ReadingsTerm.objects.create(date=d)

    # overeni datumu do prazdnin
    for month in range(1, 6 + 1):
        d = datetime(year_to, month, 1)
        if str(d) not in dates:
            if d <= now and not ReadingsTerm.objects.filter(date=d).exists():
                ReadingsTerm.objects.create(date=d)


class AdminRedirectView(View):
    """
    Pomocne redirect view. Pokud na nej nekdo primo vleze, hodi ho to
    na administraci aktualniho mesice.
    """

    def get(self, request, *args, **kwargs):
        (year_from, year_to, month) = self.get_dates()
        handle_terms(year_from, year_to)
        return HttpResponseRedirect(reverse('admin_month', args=[year_from, year_to, month]))

    def get_dates(self):
        """
        Vytahne nejcerstvejsi zaznam ReadingsTerm, a vrati interval let,
        do ktereho spada (interval odpovida skolnimu roku).
        """
        now = datetime.now()
        if now.month > 6 and now.month < 9:
            now = datetime(now.year, 6, 1)

        term = ReadingsTerm()
        out = list(term.get_year_interval(now)) + [now.month]
        return out


class AdminView(FormView):
    template_name = 'readings/admin.html'
    form_class = ReadingForm

    # --- custom osetreni get/post -------------------------------------------

    def get(self, request, *args, **kwargs):
        self.custom_handle(kwargs)
        return super(AdminView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.custom_handle(kwargs)
        return super(AdminView, self).post(request, *args, **kwargs)

    def custom_handle(self, kwargs):
        out = self.check_dates(kwargs)
        if out is not None:
            return out
        handle_terms(int(kwargs['year_from']), int(kwargs['year_to']))
        self.main_date = self.get_main_date(kwargs)

    def check_dates(self, kwargs):
        """
        Osetreni nesmyslnych datu v URL.
        """
        month = int(kwargs['month'])
        if (int(kwargs['year_from']) >= int(kwargs['year_to'])) or \
           (month < 1 or month > 12):
            # kdyby datumy byly nejake dodrbane, tak se sverime do pece autoredirectu
            return HttpResponseRedirect(reverse('admin_redir'))
        return None

    def get_main_date(self, kwargs):
        """
        Vrati datetime s prave aktualnim mesicem/rokem (zarovannym na prvni
        den mesice).
        """
        month = int(kwargs['month'])
        if month >= 9 and month <= 12:
            main_date = datetime(int(kwargs['year_from']), month, 1)
        else:
            main_date = datetime(int(kwargs['year_to']), month, 1)
        return main_date

    # --- kontext do sablony -------------------------------------------------

    def get_context_data(self, **kwargs):
        out = super(AdminView, self).get_context_data(**kwargs)
        out.update({
            'main_date': self.main_date,
            'terms': self.get_terms(),
            'childrens': self.childrens,
            'readings': self.readings,
        })
        return out

    # --- formularove metody -------------------------------------------------

    def get_initial(self):
        self.readings = self.get_readings()
        out = {'minutes_%i' % k: v for k, v in self.readings.items()}
        out['length'] = max(self.terms.values_list('length', flat=True))
        out['note'] = self.terms.values_list('note', flat=True)[0]
        return out

    def get_form_kwargs(self):
        self.childrens = self.get_childrens()
        out = super(AdminView, self).get_form_kwargs()
        out.update({
            'childrens': self.childrens,
            'terms': self.terms.values_list('id', flat=True)
        })
        return out

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.INFO, u'Formulář byl úspěšně uložen.')
        return super(AdminView, self).form_valid(form)

    def get_success_url(self):
        return self.request.path_info

    # --- data z db ----------------------------------------------------------

    def get_readings(self):
        """
        Vrati slovnik {<CHILDREN-ID>: <MINUTES>} pro mesic odpovidajici
        self.main_date.
        """
        # nalezeni terminu v zadanem intervalu
        self.terms = ReadingsTerm.objects.filter(date=self.main_date)

        # statistiky cteni
        readings = ReadingsRecord.objects.filter(term__id__in=self.terms.values_list('id', flat=True))\
                                         .values_list('children', 'minutes')
        readings = dict(readings)

        return readings

    def get_childrens(self):
        return Children.objects.all().order_by('lastname')

    def get_terms(self):
        """
        Vrati vsechny terminy pro aktualni skolni rok. Generujeme z nej
        pomocne menu nalevo.
        """
        qs = ReadingsTerm.objects.filter(date__gte=datetime(int(self.kwargs['year_from']), 9, 1),
                                         date__lte=datetime(int(self.kwargs['year_to']), 6, 1))
        return qs.order_by('-date')
