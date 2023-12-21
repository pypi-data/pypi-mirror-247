# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

from .account import TYPES


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'

    def _get_tax_rule_pattern(self):
        pattern = super(PurchaseLine, self)._get_tax_rule_pattern()

        type, legal_form = None, None
        if (self.product
                and self.product.type in [i[0] for i in TYPES]):
            type = self.product.type
        if self.purchase:
            legal_form = self.purchase.party.legal_form

        pattern['type'] = type
        pattern['legal_form'] = legal_form
        return pattern

    @fields.depends('_parent_purchase.party')
    def on_change_product(self):
        super(PurchaseLine, self).on_change_product()
