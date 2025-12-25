frappe.pages['ai-chat'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'AI Chat Assistant',
        single_column: true
    });

    const chat = $('<div style="height:70vh; overflow:auto; padding:10px;"></div>').appendTo(page.body);
    const input = $('<input class="form-control" placeholder="Type a message...">').appendTo(page.body);

    input.on('keypress', function(e) {
        if (e.which === 13 && input.val()) {
            const msg = input.val();
            input.val('');
            chat.append(`<div style="text-align:right">${msg}</div>`);

            frappe.call({
                method: 'erpn8n.api.send_message',
                args: { message: msg },
                callback: function(r) {
                    if (r.message) {
                        chat.append(`<div>${r.message.reply}</div>`);
                        chat.scrollTop(chat.prop("scrollHeight"));
                    }
                }
            });
        }
    });
};
