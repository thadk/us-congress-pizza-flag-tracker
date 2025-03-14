import uuid
import random

#  for state_offices in office_codes_list:
#         usa_state = state_offices["usa_state"]
#         for office_code in state_offices["office_code"]:


def init_orders_table(office_codes_list, db):

    from models import OrderModel

    for x in range(10):
        order_number = x + 1
        theUuid = str(uuid.uuid4())
        usa_state_object = random.choice(office_codes_list)
        usa_state = usa_state_object.get("usa_state")
        order_status = random.randint(1, 10)
        home_office_code = random.choice(usa_state_object.get("office_code"))

        order_ = OrderModel(
            theUuid, usa_state, order_number, home_office_code, order_status
        )
        db.session.add(order_)
