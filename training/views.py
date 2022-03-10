from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.status import HTTP_412_PRECONDITION_FAILED

from .models import Topic, TrainingTest, Question, TrainingTestTaker, TrainingTestCustomerRelation, Answer
from .serializers import (TrainingTestListSerializer, TrainingTestDetailSerializer, TopicSerializer,
                          PersonalCustomerTestsSerializer, CustomerAnswerSerializer, TrainingTestTakerSerializer,
                          TrainingTestCustomerRelationSerializer)


class TopicList(ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TopicDetail(RetrieveAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PersonalCustomerTests(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PersonalCustomerTestsSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = TrainingTest.objects.filter(trainingtesttaker__customer=self.request.user)
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query).distinct()

        return queryset


class TrainingTestList(ListAPIView):
    serializer_class = TrainingTestListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        queryset = TrainingTest.objects.exclude(trainingtesttaker__customer=self.request.user)
        query = self.request.query_params.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query).distinct()

        return queryset


class TrainingTestDetail(RetrieveAPIView):
    serializer_class = TrainingTestDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get('slug')
        test = get_object_or_404(TrainingTest, slug=slug)
        last_question = None
        customer, created = TrainingTestTaker.objects.get_or_create(customer=self.request.user, training_test=test)
        if created:
            for question in Question.objects.filter(training_test=test):
                TrainingTestCustomerRelation.objects.create(customer=customer, question=question)
        else:
            last_question = TrainingTestCustomerRelation.objects.filter(customer=customer, answer__isnull=False)
            if last_question.count() > 0:
                last_question = last_question.last().id
            else:
                last_question = None
        return Response(
            {
                'test': self.get_serializer(test, context={
                    'request': self.request
                }).data,
                'last_question_id': last_question
            })


class SaveCustomerAnswers(UpdateAPIView):
    serializer_class = TrainingTestCustomerRelationSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        trainingtesttaker_id = request.data.get('trainingtesttaker')
        question_id = request.data.get('question')
        answer_id = request.data.get('answer')
        customer = self.request.user
        slug = self.kwargs.get('slug')
        training_test = get_object_or_404(TrainingTest, slug=slug)

        # training_test_taker = get_object_or_404(TrainingTestTaker, id=trainingtesttaker_id)
        training_test_taker = get_object_or_404(TrainingTestTaker, customer=customer, training_test=training_test)

        if training_test_taker.completed:
            return Response({
                "message": "This quiz is already complete. you can't answer any more questions"},
                status=HTTP_412_PRECONDITION_FAILED
            )

        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)

        if answer.is_correct:
            comment = answer.comment_correct
        else:
            comment = answer.comment_incorrect

        obj = get_object_or_404(TrainingTestCustomerRelation, customer=training_test_taker, question=question)
        obj.answer = answer
        obj.save()

        return Response({'data': self.get_serializer(obj, context={'request': self.request}).data,
                         'comment': comment})


class SubmitTest(GenericAPIView):
    serializer_class = CustomerAnswerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        trainingtesttaker_id = request.data.get('trainingtesttaker')
        question_id = request.data.get('question')
        answer_id = request.data.get('answer')
        slug = self.kwargs.get('slug')
        test = TrainingTest.objects.get(slug=slug)

        training_test_taker = get_object_or_404(TrainingTestTaker, id=trainingtesttaker_id)
        if training_test_taker.completed:
            return Response({
                "message": "This quiz is already complete. you can't submit again"},
                status=HTTP_412_PRECONDITION_FAILED
            )

        question = get_object_or_404(Question, id=question_id)
        if answer_id is not None:
            answer = get_object_or_404(Answer, id=answer_id)
            obj = get_object_or_404(TrainingTestCustomerRelation, customer=training_test_taker, question=question)
            obj.answer = answer
            obj.save()
        training_test_taker.completed = True

        correct_answers = 0
        for users_answer in TrainingTestCustomerRelation.objects.filter(customer=training_test_taker,
                                                                        question=question):
            answer = Answer.objects.get(question=users_answer.question, is_correct=True)
            if users_answer.answer == answer:
                correct_answers += 1
        score = int(correct_answers / training_test_taker.training_test.questions.count() * 100)
        training_test_taker.score = score
        training_test_taker.save()
        print('preparing')
        training_test_taker.customer.email_user(subject=test.name,
                                                message=f'You completed the test with a score of {score}',
                                                from_email='quizzes@test.com')  # celery need
        print('sending')
        return Response(self.get_serializer(test).data)
