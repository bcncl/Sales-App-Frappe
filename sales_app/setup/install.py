import frappe

def after_install():
    try:
        permissions = [
        {'parent': 'Customer', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 0, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 0},
        {'parent': 'Currency', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 1, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 0},
        {'parent': 'File', 'role': 'Customer', 'if_owner': 1, 'permlevel': 0, 'select': 0, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 0},
        {'parent': 'Sales App Payment Entry', 'role': 'Customer', 'if_owner': 1, 'permlevel': 0, 'select': 1, 'read': 1, 'write': 1, 'create': 1, 'delete': 0, 'submit': 1, 'cancel': 0, 'report': 0, 'print': 0},
        {'parent': 'Sales Order', 'role': 'Customer', 'if_owner': 1, 'permlevel': 0, 'select': 1, 'read': 1, 'write': 1, 'create': 1, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 1},
        {'parent': 'Item', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 1, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 0},
        {'parent': 'Company', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 1, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 0},
        {'parent': 'GL Entry', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 1, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 1, 'print': 0},
        {'parent': 'Account', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 0, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 0},
        {'parent': 'Sales Invoice', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 1, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 1, 'print': 1},
        {'parent': 'Sales Invoice', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 1, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 1, 'print': 1},
        {'parent': 'Payment Ledger Entry', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 0, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 0},
        {'parent': 'Journal Entry', 'role': 'Customer', 'if_owner': 0, 'permlevel': 0, 'select': 0, 'read': 1, 'write': 0, 'create': 0, 'delete': 0, 'submit': 0, 'cancel': 0, 'report': 0, 'print': 0}
        ]
        
        for perm in permissions:
            # Check if the permission already exists
            existing_perm = frappe.get_all('Custom DocPerm', filters={
                'parent': perm['parent'],
                'role': perm['role'],
                'if_owner': perm['if_owner'],
                'permlevel': perm['permlevel']
            })
        
            if existing_perm:
                # Update existing permission
                doc = frappe.get_doc('Custom DocPerm', existing_perm[0].name)
                for key, value in perm.items():
                    setattr(doc, key, value)
                doc.save
            else:
                doc = frappe.get_doc({
                    'doctype': 'Custom DocPerm',
                    **perm
                })
                doc.insert()
        report_permission()
    except Exception as e:
        frappe.throw(f"{e}")


def report_permission():
    try:
        permissions = [
            {"report": "General Ledger"},
            {"report": "Accounts Receivable"}
        ]
        for perm in permissions:
            check = frappe.db.exists("Report",[['name','=', perm['report']],["Has Role","role","=","Customer"]])
            if not check:
                try:
                    report = frappe.get_doc("Report", perm["report"])
                    report.append("roles", {
                        "role": "Customer"
                    })
                    report.save()
                    print(f'Report Permission Created for {perm["report"]}')

                except Exception as err:
                    print(f'{err} for {perm["report"]}')
    
    except Exception as e:
        print(e)
        frappe.throw(f"Custom Role Setup Error: {str(e)}")
