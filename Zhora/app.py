import sqlite3
import contextlib
import json
from flask import Flask, Response, request


app = Flask(__name__)


@contextlib.contextmanager
def create_cursor():
    connection = sqlite3.connect('chinook.db')
    try:
        yield connection.cursor()  #
    finally:
        connection.close()


@app.route('/names')
def get_names():
    with create_cursor() as cursor:
        query = cursor.execute('SELECT FirstName, count(*) FROM customers GROUP BY FirstName')
        data = query.fetchall()

    return Response(
        response=json.dumps(data),
        content_type='application/json'
    )


@app.route('/customers/')
def get_customers():
    with create_cursor() as cursor:

        conditions = []

        try:
            customer_id = int(request.args['id'])  # get id values
            conditions.append(f'CustomerId = {customer_id}')  # >> []
        except (ValueError, KeyError):  # id = poop
            pass

        country = request.args.getlist('country')  # get country value
        if country:
            n = ", ".join(repr(e) for e in country)
            conditions.append(f'Country IN ({n})')  # >> []

        fax_parameters = {
            'is_null': 'Fax IS NULL',
            'is_not_null': 'Fax IS NOT NULL',
        }
        fax = fax_parameters.get(request.args.get('fax'))  # get fax values
        if fax:
            conditions.append(fax)  # >> []

        query = 'SELECT * FROM customers'  # main
        if conditions:
            where = ' OR '.join(conditions)  # OR
            query = f'SELECT * FROM customers WHERE {where};'
        customers = cursor.execute(query)

        results = customers.fetchall()

    return Response(
        response=json.dumps(results),
        content_type='application/json'
    )


@app.route('/tracks')
def gef_tracks():
    with create_cursor() as cursor:
        query = cursor.execute('SELECT Count(*)  FROM tracks')
        data = query.fetchall()

    return Response(
        response=json.dumps(data),
        content_type='application/json'
    )


@app.route('/tracks-sec')
def gef_tracks_sec():
    with create_cursor() as cursor:
        query = cursor.execute('SELECT Name,Milliseconds /1000 FROM tracks')
        data = query.fetchall()

    return Response(
        response=json.dumps(data),
        content_type='application/json'
    )


if __name__ == '__main__':
    app.run()
