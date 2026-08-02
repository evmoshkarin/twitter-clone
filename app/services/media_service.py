from app.models import Media
from app.extensions import db

class MediaService:
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in MediaService.ALLOWED_EXTENSIONS

    @staticmethod
    def save_media(file):
        if not file or file.filename == '':
            raise ValueError("Файл не выбран")
        if not MediaService.allowed_file(file.filename):
            raise ValueError("Недопустимый формат файла")

        file_body = file.read()
        media = Media(file_body=file_body)
        db.session.add(media)
        db.session.commit()
        return media.id
