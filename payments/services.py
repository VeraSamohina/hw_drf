import stripe

from courses.models import Course


def create_payment_intent(id):
    course = Course.objects.get(id=id)
    # Создание платежного намерения в stripe
    payment_intent = stripe.PaymentIntent.create(amount=int(course.price), currency='rub',
                                                 automatic_payment_methods={"enabled": True,
                                                                            "allow_redirects": "never"})

    # Подтверждение платежного намерения в stripe
    stripe.PaymentIntent.confirm(payment_intent.id, payment_method='pm_card_visa')
    return payment_intent
