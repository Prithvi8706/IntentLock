import razorpay


def verify_payment_signature(key_secret: str, payment_id: str, order_id: str, signature: str) -> bool:
    try:
        razorpay.Utility(key_secret).verify_payment_signature({"razorpay_order_id": order_id,
                                                               "razorpay_payment_id": payment_id,
                                                               "razorpay_signature": signature})
        return True
    except Exception:
        return False

