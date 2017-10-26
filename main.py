from collections import defaultdict
from functools import partial
import hashlib
import json
import string
import threading
import time

import click
import psycopg2.extras


emails_query = '''
    insert into "Emails" (id, timestamp) values %s
    on conflict do nothing;'''


recipients_query = '''
    insert into "Recipients" (id, address) values %s
    on conflict do nothing;'''


words_query = '''
    insert into "Words" (address, word, count) values %s
    on conflict (address, word) do update
    set count = "Words".count + EXCLUDED.count'''


@click.command()
@click.option('--input-file', '-f', default='uploads.json')
@click.option('--db-host', '-h', default='localhost')
@click.option('--db-user', '-u', default='postgres')
@click.option('--db-password', '-p', default='postgres')
@click.option('--db-name', '-d', default='checkrecipient_test')
def main(**options):
    time_printer = partial(print_time_diff, time.time())

    with open(options['input_file']) as f:
        payload = json.load(f)

    time_printer('Finished decoding json')

    punctuation_translator = str.maketrans('', '', string.punctuation)

    emails = []
    recipients = []
    recipient_word_map = defaultdict(lambda: defaultdict(int))

    for upload in payload.get('uploads', []):
        for email in upload.get('emails', []):
            h = hashlib.md5()
            h.update(str(email).encode())
            _id = h.hexdigest()

            timestamp = email.get('timestamp')
            if timestamp:
                emails.append((_id, timestamp))

            email_recipients = set(email.get('recipients', []))
            for recipient in email_recipients:
                recipients.append((_id, recipient))

            subject = email.get('subject', '').lower().translate(
                punctuation_translator)
            for word in subject.split():
                for recipient in email_recipients:
                    recipient_word_map[recipient][word] += 1

    time_printer('Finished parsing input')

    recipient_words = [
        (address, word, count)
        for address, counts in recipient_word_map.items()
        for word, count in counts.items()
    ]

    threads = [
        threading.Thread(target=flush, args=(q, values, options))
        for q, values in [
            (emails_query, emails), (recipients_query, recipients),
            (words_query, recipient_words)]
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    time_printer('Total time')


def print_time_diff(start_time, prefix='Time elapsed'):
    print('{}: {:.3f}s'.format(prefix, time.time() - start_time))


def flush(q, values, options):
    conn = psycopg2.connect(
        dbname=options['db_name'],
        user=options['db_user'],
        password=options['db_password'],
        host=options['db_host'])

    cur = conn.cursor()
    psycopg2.extras.execute_values(cur, q, values, page_size=500)

    conn.commit()

    cur.close()
    conn.close()


if __name__ == '__main__':
    main()
