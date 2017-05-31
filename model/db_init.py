from sqlalchemy.orm import sessionmaker,scoped_session

from conf import settings
from handler import utils
from model.db_obj import AccountGroup,User,Base
db_session = scoped_session(sessionmaker(bind=settings.engine))


def db_init():
    Base.metadata.drop_all(settings.engine)
    Base.metadata.create_all(settings.engine)
    accountgroup_item1 = AccountGroup(name='admin')
    accountgroup_item2 = AccountGroup(name='regular')
    db_session.add(accountgroup_item1)
    db_session.add(accountgroup_item2)
    db_session.flush()
    admin_user = User(name='admin',password= utils.encrypt_pass('admin123'),group=accountgroup_item1.id)
    db_session.add(admin_user)
    db_session.commit()
    db_session.remove()

if __name__ == '__main__':
    db_init()