import frappe
import json


@frappe.whitelist()
def enqueue_update_expense_entries(expense_entries):
    """Enqueue background job to update expense_entries."""
    frappe.enqueue('expense_request.utils.expense_entry.update_expense_entries_in_background', expense_entries=expense_entries)
    return "Expense Entries update has been initiated."


@frappe.whitelist()
def update_expense_entries_in_background(expense_entries, batch_size=100):
    """Background job to update selected Expense Entry."""

    # Parse the expense_entries if it comes as a string (JSON format)
    if isinstance(expense_entries, str):
        expense_entries = frappe.parse_json(expense_entries)

    total_entries = len(expense_entries)
    batches = [expense_entries[i:i + batch_size] for i in range(0, total_entries, batch_size)]
    
    for batch in batches:
        for ex in batch:
            try:
                # Get the document for each Expense Entry
                ex_doc = frappe.get_doc("Expense Entry", ex)
                
                # Initialize row_total and row_count for each expense entry
                row_total = 0
                row_count = 0
                
                for ex_item in ex_doc.expenses:
                    if ex_item.expense_account:
                        row_total += ex_item.amount
                        row_count += 1  # Count each item row

                # Set the calculated values to the main form's fields
                frappe.db.set_value("Expense Entry", ex, {
                    "total": row_total,
                    "quantity": row_count
                }, update_modified=False)

                frappe.db.commit()
                
            except Exception as e:
                frappe.log_error(f"Error updating Expense Entry {ex}: {str(e)}")

    return "Expense Entries have been successfully updated."
