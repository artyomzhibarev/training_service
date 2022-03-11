from .models import TrainingTestTaker

from celery import shared_task


@shared_task
def send_test_result_to_customer(training_test_taker_id: int, test_name: str, score: int):
    try:
        taker = TrainingTestTaker.objects.get(id=training_test_taker_id)
        taker.customer.email_user(subject=f'{test_name} results',
                                  message=f'You completed the test {test_name} with a score of {score}',
                                  from_email='quizzes@test.com')
    except TrainingTestTaker.DoesNotExist:
        return None
