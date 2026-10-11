"""Memberships and purchases. PLACEHOLDER: no payment processor is connected yet (Adder, 2026-10-11: Stripe
later; put a placeholder for it now).

What is real here: the list of plans the site offers, which the membership, student and teacher pages read.
What is not: checkout. `checkout_url` returns None until Stripe is set up, and the pages say checkout opens soon.

To connect Stripe later:
  1. Create the products and prices in the Stripe dashboard; put each price id in PLANS[...]["stripe_price"].
  2. Set STRIPE_SECRET_KEY and STRIPE_WEBHOOK_SECRET in .env (config/settings reads them; empty means off).
  3. In checkout_url, create a Checkout Session (mode "subscription" or "payment" per plan) with the user's id as
     client_reference_id, success_url back to the account page, cancel_url back to /membership/.
  4. Add a webhook view for checkout.session.completed / customer.subscription.updated / deleted that sets
     Profile.full_access (students) or records the class license (teachers). Grant access from the webhook only,
     never from the success redirect.
  5. Receipts, refunds and cancellation (board: money-3) come from Stripe's customer portal.
"""
from django.conf import settings

PLANS = {
    "student": {
        "who": "student",
        "name": "Student membership",
        "price": "[Price to come]",
        "kind": "subscription",
        "gives": ["Units 4 to 10: notes, practice, quizzes, AP test prep and unit tests",
                  "More full-length practice exams", "Your work and scores saved across devices"],
        "stripe_price": "",
    },
    "materials": {
        "who": "teacher",
        "name": "Course materials",
        "price": "[Price to come]",
        "kind": "one-time",
        "gives": ["Every printable packet, quiz, test and answer key, Units 1 to 10",
                  "Teacher slide decks for every lesson", "Yours to print and teach from, no student accounts needed"],
        "stripe_price": "",
    },
    "class": {
        "who": "teacher",
        "name": "Class subscription",
        "price": "[Price to come]",
        "kind": "subscription",
        "gives": ["Full access for every student in your classes", "Automatic grading with your review and score edits",
                  "Class dashboard, released results, printable forms and slide decks"],
        "stripe_price": "",
    },
}


def payments_enabled():
    return bool(getattr(settings, "STRIPE_SECRET_KEY", "")) and all(p["stripe_price"] for p in PLANS.values())


def checkout_url(request, plan_key):
    """Where the Buy button sends someone. None while payments are off (the page then shows "opens soon")."""
    if plan_key not in PLANS or not payments_enabled():
        return None
    raise NotImplementedError("Stripe Checkout goes here; see this module's docstring.")
