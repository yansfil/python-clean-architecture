from time import sleep

from app.domains.events import DeleteUserPosts, SendEmail, SendSlack
from app.services.message_queue import message_queue
from app.services.uow import PostUnitOfWork


def send_email(event: SendEmail):
    sleep(5)
    print(f"COMPLETE SEND EMAIL ({event.msg})")


def send_slack(event: SendSlack):
    sleep(5)
    print(f"COMPLETE SEND EMAIL ({event.msg})")


def delete_post(event: DeleteUserPosts, uow: PostUnitOfWork = PostUnitOfWork()):
    with uow:
        try:
            uow.repo.delete_by_user_id(event.user_id)
            uow.commit()
        except Exception as e:
            print("erorr 발생!")
            message_queue.put_nowait(SendSlack(msg=str(e)))
