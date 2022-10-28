from flask_restful import Resource, reqparse
from models.hotel_model import HotelModel

hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'cidade': "Rio de Janeiro",
        'estrelas': 4.3,
        'diaria': 420
    },
    {
        'hotel_id': 'beta',
        'nome': 'Beta Hotel',
        'cidade': "São Paulo",
        'estrelas': 4,
        'diaria': 250
    },
    {
        'hotel_id': 'omega',
        'nome': 'Omega Hotel',
        'cidade': "Santos",
        'estrelas': 5,
        'diaria': 1000
    }
]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be blank")
    argumentos.add_argument('cidade', type=str, required=True, help="The field 'cidade' cannot be blank")
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):

        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Internal error'}, 500
        return hotel.json()

    def put(self, hotel_id):

        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'Internal error'}, 500
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An error occurred trying to delete'}, 500
            return {'message': 'Hotel deleted'}
        return {'message': 'Hotel not found.'}, 404
