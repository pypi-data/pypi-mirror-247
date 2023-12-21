# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.report import Report
from trytond.transaction import Transaction
from itertools import zip_longest


class AccountTaxCodeStatement(Report):
    __name__ = 'account.tax.code.statement'

    @classmethod
    def get_context(cls, records, header, data):
        pool = Pool()
        Company = pool.get('company.company')
        Fiscalyear = pool.get('account.fiscalyear')
        Period = pool.get('account.period')
        context = Transaction().context

        report_context = super().get_context(records, header, data)
        report_context['company'] = Company(context['company'])

        values = {}
        if data.get('model_context') is not None:
            Context = pool.get(data['model_context'])
            for field in Context._fields:
                if field in context:
                    values[field] = context[field]
            report_context['ctx'] = Context(**values)
        else:
            company_id = context.get('company')
            fiscalyear_id = (context.get('fiscalyear')
                or Fiscalyear.find(company_id))
            values['fiscalyears'] = Fiscalyear(fiscalyear_id).rec_name

            if context.get('periods'):
                periods = context['periods']
                start_period = Period(periods[0])
                end_period = Period(periods[-1])
                values['start_period'] = start_period
                values['end_period'] = end_period
                start_fiscalyear = start_period.fiscalyear
                end_fiscalyear = end_period.fiscalyear
                values['fiscalyears'] = start_fiscalyear.rec_name
                if start_fiscalyear != end_fiscalyear:
                    values['fiscalyears'] += ' - ' + end_fiscalyear.rec_name

            report_context['ctx'] = values
        codes = zip_longest(records, data.get('paths') or [], fillvalue=[])
        if not context.get('show_empty_lines'):
            codes = [(r, p) for r, p in codes if r.amount != Decimal('0')]
        report_context['codes'] = codes
        return report_context
