frappe.listview_settings["Expense Entry"] = {
    onload: function(listview) {
        listview.page.add_action_item(__('<i class="fa fa-edit"></i> Update Totals'), () => {
            let checked_items = listview.get_checked_items(true);  
            console.log("chec");
            console.log(checked_items);

            if (checked_items.length > 0) {
                frappe.call({
                    method: "expense_request.utils.expense_entry.enqueue_update_expense_entries",  
                    args: {
                        expense_entries: checked_items  
                    },
                   
                    callback: function(r) {
                        if (r.message) {
                            frappe.msgprint(__(r.message));
                            
                        } else {
                            frappe.msgprint(__('Expense Entries updated successfully'));
                        }
                        listview.refresh();  
                    },
                    error: function(err) {
                        frappe.msgprint(__('An error occurred while updating Expense Entries'));
                    }
                });
            } else {
                frappe.msgprint(__('Please select at least one Expense Entries'));
            }
        });
    }
};





