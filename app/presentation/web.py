from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..di import build_customer_service, build_policy_service


web_bp = Blueprint("web", __name__)


@web_bp.get("/policies")
def list_policies():
    service = build_policy_service()
    order = request.args.get("order", "asc")
    policies = service.list_policies(order)
    return render_template(
        "policies/list.html",
        policies=policies,
        current_order=order,
    )


@web_bp.get("/policies/new")
def new_policy():
    service = build_policy_service()
    options = service.get_form_options()
    return render_template(
        "policies/form.html",
        form_title="Create policy",
        policy=None,
        options=options,
        selected_destinations=set(),
    )


@web_bp.post("/policies/new")
def create_policy():
    service = build_policy_service()
    payload = _extract_payload(request)
    try:
        service.create_policy(payload)
    except ValueError as exc:
        options = service.get_form_options()
        flash(str(exc), "error")
        return render_template(
            "policies/form.html",
            form_title="Create policy",
            policy=None,
            options=options,
            selected_destinations={int(x) for x in payload.get("destinations", [])},
            form_data=payload,
        )
    return redirect(url_for("web.list_policies"))


@web_bp.get("/policies/<int:policy_id>/edit")
def edit_policy(policy_id: int):
    service = build_policy_service()
    policy = service.get_policy(policy_id)
    options = service.get_form_options()
    selected = {destination.id for destination in policy.destinations}
    return render_template(
        "policies/form.html",
        form_title="Edit policy",
        policy=policy,
        options=options,
        selected_destinations=selected,
    )


@web_bp.post("/policies/<int:policy_id>/edit")
def update_policy(policy_id: int):
    service = build_policy_service()
    payload = _extract_payload(request)
    try:
        service.update_policy(policy_id, payload)
    except ValueError as exc:
        options = service.get_form_options()
        flash(str(exc), "error")
        return render_template(
            "policies/form.html",
            form_title="Edit policy",
            policy=service.get_policy(policy_id),
            options=options,
            selected_destinations={int(x) for x in payload.get("destinations", [])},
            form_data=payload,
        )
    return redirect(url_for("web.list_policies"))


@web_bp.post("/policies/<int:policy_id>/delete")
def delete_policy(policy_id: int):
    service = build_policy_service()
    service.delete_policy(policy_id)
    return redirect(url_for("web.list_policies"))


@web_bp.get("/customers")
def list_customers():
    service = build_customer_service()
    customers = service.list_customers()
    return render_template("customers/list.html", customers=customers)


@web_bp.get("/customers/new")
def new_customer():
    return render_template(
        "customers/form.html",
        form_title="Create customer",
        customer=None,
    )


@web_bp.post("/customers/new")
def create_customer():
    service = build_customer_service()
    payload = _extract_customer_payload(request)
    try:
        service.create_customer(payload)
    except ValueError as exc:
        flash(str(exc), "error")
        return render_template(
            "customers/form.html",
            form_title="Create customer",
            customer=None,
            form_data=payload,
        )
    return redirect(url_for("web.list_customers"))


@web_bp.get("/customers/<int:customer_id>/edit")
def edit_customer(customer_id: int):
    service = build_customer_service()
    customer = service.get_customer(customer_id)
    return render_template(
        "customers/form.html",
        form_title="Edit customer",
        customer=customer,
    )


@web_bp.post("/customers/<int:customer_id>/edit")
def update_customer(customer_id: int):
    service = build_customer_service()
    payload = _extract_customer_payload(request)
    try:
        service.update_customer(customer_id, payload)
    except ValueError as exc:
        flash(str(exc), "error")
        return render_template(
            "customers/form.html",
            form_title="Edit customer",
            customer=service.get_customer(customer_id),
            form_data=payload,
        )
    return redirect(url_for("web.list_customers"))


@web_bp.post("/customers/<int:customer_id>/delete")
def delete_customer(customer_id: int):
    service = build_customer_service()
    service.delete_customer(customer_id)
    return redirect(url_for("web.list_customers"))


def _extract_payload(request_obj):
    return {
        "base_premium": request_obj.form.get("base_premium", "0"),
        "coverage_start": request_obj.form.get("coverage_start", ""),
        "coverage_end": request_obj.form.get("coverage_end", ""),
        "trip_type": request_obj.form.get("trip_type", "leisure"),
        "is_family": request_obj.form.get("is_family", ""),
        "family_size": request_obj.form.get("family_size", "1"),
        "agent_id": request_obj.form.get("agent_id", "0"),
        "customer_id": request_obj.form.get("customer_id", "0"),
        "destinations": request_obj.form.getlist("destinations"),
    }


def _extract_customer_payload(request_obj):
    return {
        "full_name": request_obj.form.get("full_name", ""),
        "age": request_obj.form.get("age", ""),
        "gender": request_obj.form.get("gender", ""),
        "health_state": request_obj.form.get("health_state", ""),
        "health_condition": request_obj.form.get("health_condition", ""),
    }
