# Copyright (c) 2025, Eactive Techonologies and contributors
# For license information, please see license.txt

import frappe

from frappe.model.document import Document
# from erpnext.accounts.party import get_party_account
# from erpnext.accounts.doctype.payment_entry.payment_entry import get_account_details


class SalesAppPaymentEntry(Document):
	
	@frappe.whitelist()
	def get_mode_of_payment_base_on_company_currency(self):
		company_currency = frappe.db.get_value("Company", self.company, "default_currency")
		account_with_company_currency = frappe.db.get_all("Account", 
			filters={
				"disabled": 0,
				"company": self.company,
				"account_currency": company_currency
			},
			pluck="name"
		)
		valid_mode_of_payments = []
		if account_with_company_currency:
			valid_mode_of_payments = frappe.db.get_all("Mode of Payment Account", 
				filters={
					"default_account": ["In", account_with_company_currency]
				},
				pluck="parent"
			)
		return valid_mode_of_payments

	
			