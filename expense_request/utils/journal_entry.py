import frappe

@frappe.whitelist()
def calling_remain_values(expense_entry):
    """Fetch remaining amount for the given Expense Entry."""
    if expense_entry:
        # Get the Expense Entry document
        expense_doc = frappe.get_doc("Expense Entry", expense_entry)
        total_amount = expense_doc.total  # Ensure this is the correct field name
        paid_amount = expense_doc.paid_amount if expense_doc.paid_amount else 0  # Set to 0 if not present

        # Calculate remaining amount
        if total_amount is not None:  # Check if total_amount is not None
            # Set remaining amount to 0 if total_amount equals paid_amount
            if total_amount == paid_amount:
                remaining_amount = 0
            else:
                remaining_amount = total_amount - paid_amount
            
            return remaining_amount
        
    return 0  # Return 0 if no expense entry is provided

    
    


@frappe.whitelist()
def update_paid_amount(expense_entry, paid_amount):
    """Update the paid_amount and payment_status fields in the Expense Entry."""
    if expense_entry:
        # Get the Expense Entry document
        expense_doc = frappe.get_doc("Expense Entry", expense_entry)
        
        # Update the paid_amount
        frappe.db.set_value("Expense Entry", expense_entry, "paid_amount", paid_amount, update_modified=False)
        
        # Determine and update the payment_status
        if paid_amount >= expense_doc.total:
            payment_status = "Paid"
        else:
            payment_status = "Partially"  # Use "Partially Paid" for clarity

        frappe.db.set_value("Expense Entry", expense_entry, "payment_status", payment_status, update_modified=False)

        # Commit changes to the database
        frappe.db.commit()
    else:
        frappe.throw("Expense Entry not found.")


