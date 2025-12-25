import frappe
import requests
import uuid
from frappe.utils import now_datetime

@frappe.whitelist()
def send_message(message, session_id=None, context=None):
    settings = frappe.get_single("AI Assistant Settings")
    if not settings.enabled:
        frappe.throw("AI Assistant is disabled")

    if not session_id:
        session_id = str(uuid.uuid4())
        session = frappe.get_doc({
            "doctype": "AI Chat Session",
            "session_id": session_id,
            "user": frappe.session.user,
            "started_at": now_datetime(),
            "status": "Active"
        }).insert(ignore_permissions=True)
    else:
        session = frappe.get_doc("AI Chat Session", {"session_id": session_id})

    frappe.get_doc({
        "doctype": "AI Chat Message",
        "session": session.name,
        "sender": "User",
        "message": message,
        "timestamp": now_datetime()
    }).insert(ignore_permissions=True)

    payload = {
        "text": message,
        "session_id": session_id,
        "user": {
            "name": frappe.get_value("User", frappe.session.user, "full_name"),
            "email": frappe.session.user,
            "roles": frappe.get_roles()
        },
        "site": frappe.local.site,
        "context": context or {},
        "timestamp": now_datetime().isoformat()
    }

    response = requests.post(
        settings.n8n_webhook_url,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "X-ERP-AI-SECRET": settings.shared_secret
        },
        timeout=settings.request_timeout or 30
    )

    response.raise_for_status()
    result = response.json()

    frappe.get_doc({
        "doctype": "AI Chat Message",
        "session": session.name,
        "sender": "AI",
        "message": result.get("reply"),
        "raw_payload": result,
        "timestamp": now_datetime()
    }).insert(ignore_permissions=True)

    return result
