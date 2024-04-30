import os
import django
import json
from helpers import RedisConnection
from datetime import datetime, date, timedelta


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_web_system.settings")

django.setup()



from books.models import BorrowBookRecords


def mapping_data(payload):
    penalty_list = []



    if payload is not None:
        for data in payload:
            if data is not None:
                qr_code = data.reservation.qr_code

                # Check if qr_code already exists in penalty_list
                existing_penalty = next((penalty for penalty in penalty_list if penalty['qr_code'] == qr_code), None)

                if existing_penalty:
                    # Append the book_borrow value only if it's not already in the existing penalty
                    book_borrow = data.reservation.book.title
                    if book_borrow not in existing_penalty['book_borrow']:
                        existing_penalty['book_borrow'].append(book_borrow)
                else:
                    # Create a new penalty
                    penalty = {
                        'qr_code': qr_code,
                        'email': data.reservation.reservee.email,
                        'name' : f"{data.reservation.reservee.get_full_name()}", 
                        'date_to_return': data.date_to_return.date().isoformat(),
                        'book_borrow': [data.reservation.book.title]
                    }
                    penalty_list.append(penalty)

            # return penalty_list

    return penalty_list



def filter_past_day_date(dates):

    current_date = date.today()
    past_date =  current_date - timedelta(days=7)

    penalty_record =  []

    past_day_dates = list(map(lambda x: x if x.date_to_return.date() == past_date else None, dates))
    
    # print(past_day_dates)
    test_penalty = mapping_data(past_day_dates)

    return test_penalty

def check_borrow_status():


    book_borrows = BorrowBookRecords.objects.filter(reservation__isnull=False, returned_date__isnull=True)

    # get only the timeframe for 7 days
    past_week_borrow_books = date.today() - timedelta(days=7)
    penalty_borrow = list(map(lambda x: x, filter(lambda x: x.date_to_return.date() == past_week_borrow_books, book_borrows)))

    return penalty_borrow



def insert_redis_data(data):
    try:
        with redis_client.redis_connection_pipeline() as pipe:
            pipe
            for _d in data:
                pipe.sadd("danielfajardolibrary:penalty", json.dumps(_d))

            pipe.execute()

        return "Done"
    except BaseException as e:
        print(e,"error in insert data redis")

def main():

    borrow_books = check_borrow_status()

    past_day_dates = filter_past_day_date(borrow_books)

    # print(past_day_dates)

    redis_insert = insert_redis_data(past_day_dates)

    print("total inserted data", len(past_day_dates))

if __name__ == "__main__":
    redis_client = RedisConnection()
    main()
