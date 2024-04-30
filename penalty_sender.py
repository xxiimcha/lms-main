from helpers import EmailHelper, RedisConnection
from django.conf import settings
import json, time, random



def get_redis_penalty(connection):
    return connection.spop("danielfajardolibrary:penalty",1)


def send_email(data_payload:str):

    info_payload =  json.loads(data_payload)

    # print(info_payload)

    message_html = f"""
        <h1>You have not returned the book you borrowed!</h1>

        <p>Hi {info_payload.get("name")}, the return date for the book you borrowed has already passed, so it should be returned promptly. Failure to return the book on the designated date may result in appropriate penalties.</p>


        <h3>Books you borrowed:</h3>
        
        <ul>
            {''.join(f"<li>{book}</li>" for book in info_payload.get("book_borrow"))}
        </ul>

        
        <h3>Book transaction code: {info_payload.get("qr_code")}</h3>

        <h3>Date to return : {info_payload.get("date_to_return")}</h3>
    """

    email = EmailHelper(subject="Book Penalty",body=message_html,recipients=info_payload.get("email"))

    status = email.send_email(use_html=True)

    if status == 1:
        print("done sending. email:",info_payload.get("email"))
        return "Sent"
    
    return "Failed"

def main():


    payload =  get_redis_penalty(connection)

    

    if len(payload) > 0:
        print("total data: ",len(payload))
        test_mail = send_email(payload[0])

    else:
        print("Got nothing from queue...")
        exit(0)



if __name__ == "__main__":
    redis_client =  RedisConnection()
    connection = redis_client.redis_connection()
    print(connection, "Redis Cluster Connection")



    settings.configure(
        EMAIL_HOST='smtp.hostinger.com',
        EMAIL_HOST_USER='no-reply@danielfajardolibrary.online',
        EMAIL_HOST_PASSWORD='153303AaCc!%',
        EMAIL_PORT=465,
        EMAIL_USE_SSL=True,
        EMAIL_USE_TLS=False,
        DEFAULT_FROM_EMAIL='Daniel Fajardo Public Library <no-reply@danielfajardolibrary.online>',
    )

    while True:
        t1 = time.perf_counter()
        main()
        t2 = time.perf_counter()

        print("Finished in", round(t2 - t1, 2))
        print("Idling...")
        time.sleep(random.randint(2, 5))

    













