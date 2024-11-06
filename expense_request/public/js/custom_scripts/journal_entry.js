frappe.ui.form.on('Journal Entry', {
    custom_expense_entry: function(frm) {
        console.log("Entering expense");

        // Call the server-side method to fetch the remaining amount
        frappe.call({
            method: 'expense_request.utils.journal_entry.calling_remain_values',  // Update with your actual method path
            args: {
                expense_entry: frm.doc.custom_expense_entry  // Pass the selected expense entry
            },
            callback: function(response) {
                if (response.message) {
                    console.log("res");
                    console.log(response.message);
                    // Assuming response.message contains the remaining amount
                    frm.set_value('custom_expense_amount', response.message);
                }
            }
        });
    },
    before_submit: function(frm) {
        console.log("enter in jdjdj");
        // Fetch total debit and custom expense amount from the form
        const total_debit = frm.doc.total_debit; // Assuming you have this field
        const custom_expense_amount = frm.doc.custom_expense_amount; // Your custom field

        // Check if total_debit is greater than custom_expense_amount
        if (total_debit > custom_expense_amount) {
            frappe.throw(__('Debit amount cannot be greater than the custom expense amount.'));
        }

        // Optionally, you can also set a paid amount in the Expense Entry
        update_expense_entry(frm);
    }
});




// Function to update the Expense Entry's paid_amount
function update_expense_entry(frm) {
    console.log("enter in update method;");
    // Get the expense entry from the form
    const expense_entry = frm.doc.expense_entry; // Assuming you have a field linking to Expense Entry

    if (expense_entry) {
        frappe.call({
            method: 'expense_request.utils.journal_entry.update_paid_amount',
            args: {
                expense_entry: expense_entry,
                paid_amount: frm.doc.total_debit // Or any logic you want for paid amount
            },
            callback: function(response) {
                if (!response.exc) {
                    frappe.show_alert(__('Paid amount updated successfully.'));
                }
                

            }
        });
    }
}
