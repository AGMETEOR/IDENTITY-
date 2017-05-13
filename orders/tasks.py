from celery import task
from django.core.mail import send_mail
from .models import Order



@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    note='Thank you for shopping on identity! Delivery will be done within a day.\n\n You are receiving an order confirmation email. \n This email is intended for {}.\n (c) 2017 iDENTITY UG. \n Kampala, Uganda'.format(order.firstname)  
    subject = 'Order no. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order at iDentity.\n Your order id is {}.\n\n {}'.format(order.firstname,order.id,note)
    mail_sent = send_mail(subject,message,'admin@identity.com',[order.email])
    return mail_sent
    

