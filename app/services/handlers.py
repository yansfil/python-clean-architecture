from time import sleep

from app.domains.events import DeleteUserPosts, SendEmail
from app.services.uow import PostUnitOfWork


def send_email(event: SendEmail):
    sleep(5)
    print(f"COMPLETE SEND EMAIL ({event.msg})")


def delete_post(event: DeleteUserPosts, uow: PostUnitOfWork = PostUnitOfWork()):
    with uow:
        uow.repo.delete_by_user_id(event.user_id)
        uow.commit()
