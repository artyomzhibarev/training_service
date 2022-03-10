from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Topic, TrainingTest, Question, Answer, TrainingTestTaker, TrainingTestCustomerRelation


class TopicSerializer(serializers.ModelSerializer):
    tests = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Topic
        fields = ('id', 'name', 'content_text', 'tests')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "question", "answer_text")


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = '__all__'


class TrainingTestCustomerRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingTestCustomerRelation
        fields = "__all__"


class PersonalCustomerTestsSerializer(serializers.ModelSerializer):
    questions_count = SerializerMethodField()
    completed = SerializerMethodField()
    score = SerializerMethodField()
    progress = SerializerMethodField()

    class Meta:
        model = TrainingTest
        fields = ('id', 'name', 'topic', 'created_at', 'slug', 'questions_count', 'completed', 'score', 'progress')
        read_only_fields = ('questions_count', 'completed', 'progress')

    def get_completed(self, obj):
        try:
            test = TrainingTestTaker.objects.get(
                customer=self.context['request'].user, training_test=obj)
            return test.completed
        except TrainingTestTaker.DoesNotExist:
            return None

    def get_progress(self, obj):
        try:
            test_taker = TrainingTestTaker.objects.get(customer=self.context['request'].user, training_test=obj)
            if not test_taker.completed:
                questions_answered = TrainingTestCustomerRelation.objects.filter(
                    customer=test_taker, answer__isnull=False).count()
                total_questions = obj.questions.all().count()
                return int(questions_answered / total_questions)
            return None
        except TrainingTestTaker.DoesNotExist:
            return None

    def get_questions_count(self, obj):
        return obj.questions.all().count()

    def get_score(self, obj):
        try:
            quiztaker = TrainingTestTaker.objects.get(customer=self.context['request'].user, training_test=obj)
            if not quiztaker.completed:
                return quiztaker.score
            return None
        except TrainingTestTaker.DoesNotExist:
            return None


class TrainingTestListSerializer(serializers.ModelSerializer):
    questions_count = SerializerMethodField()

    class Meta:
        model = TrainingTest
        fields = ('name', 'topic', 'created_at', 'slug', 'questions_count')

    def get_questions_count(self, obj):
        return obj.questions.all().count()


class TrainingTestTakerSerializer(serializers.ModelSerializer):
    """
    QuizTakerSerializer
    """
    trainingtestcustomerrelation_set = TrainingTestCustomerRelationSerializer(many=True)

    class Meta:
        model = TrainingTestTaker
        fields = '__all__'


class TrainingTestDetailSerializer(serializers.ModelSerializer):
    """
    QuizDetailSerializer
    """
    trainingtesttaker_set = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = TrainingTest
        fields = ('id', 'questions', 'trainingtesttaker_set')

    def get_trainingtesttaker_set(self, obj):
        try:
            training_test_taker = TrainingTestTaker.objects.get(customer=self.context.get('request').user,
                                                                training_test=obj)
            serializer = TrainingTestTakerSerializer(training_test_taker)
            return serializer.data
        except TrainingTestTaker.DoesNotExist:
            return None


class CustomerAnswerSerializer(serializers.ModelSerializer):
    trainingtesttaker_set = serializers.SerializerMethodField()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = TrainingTest
        fields = "__all__"

    def get_trainingtesttaker_set(self, obj):
        try:
            training_test_taker = TrainingTestTaker.objects.get(customer=self.context.get('request').user, training_test=obj)
            serializer = TrainingTestTakerSerializer(training_test_taker)
            return serializer.data

        except TrainingTestTaker.DoesNotExist:
            return None
