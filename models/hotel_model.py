from sql_alchemy import db


class HotelModel(db.Model):
    __tablename__ = 'hoteis'

    hotel_id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(80))
    cidade = db.Column(db.String(40))
    estrelas = db.Column(db.Float(precision=1))
    diaria = db.Column(db.Float(precision=2))

    def __init__(self, hotel_id, nome, cidade, estrelas, diaria):
        self.hotel_id = hotel_id
        self.nome = nome
        self.cidade = cidade
        self.estrelas = estrelas
        self.diaria = diaria

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'cidade': self.cidade,
            'estrelas': self.estrelas,
            'diaria': self.diaria
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        db.session.add(self)
        db.session.commit()

    def update_hotel(self, nome, cidade, estrelas, diaria):
        self.nome = nome
        self.cidade = cidade
        self.estrelas = estrelas
        self.diaria = diaria

    def delete_hotel(self):
        db.session.delete(self)
        db.session.commit()
