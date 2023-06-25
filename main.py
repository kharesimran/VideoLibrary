from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Video(name={self.name}, views={self.views}, likes={self.likes}'


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

video_create_args = reqparse.RequestParser()
video_create_args.add_argument('name', type=str, help='Name of the video', required=True)
video_create_args.add_argument('views', type=int, help='Number of views of the video', required=True)
video_create_args.add_argument('likes', type=int, help='Number of likes on the video', required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument('name', type=str, help='Name of the video')
video_update_args.add_argument('views', type=int, help='Number of views of the video')
video_update_args.add_argument('likes', type=int, help='Number of likes on the video')


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        video = db.session.query(VideoModel).filter_by(id=video_id).first()
        if not video:
            abort(404, message='Could not find a video with that ID.')
        return video, 200

    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_create_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        try:
            db.session.add(video)
            db.session.commit()
            return video, 201
        except IntegrityError:
            abort(409, message='Video ID taken.')

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_update_args.parse_args()
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message='A video with that ID does not exist.')
        if args['name']:
            video.name = args['name']
        if args['views']:
            video.views = args['views']
        if args['likes']:
            video.likes = args['likes']

        db.session.commit()

        return video, 200

    def delete(self, video_id):

        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message='A video with that ID does not exist.')
        db.session.delete(video)
        db.session.commit()
        return '', 204


api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True, port=5000)
