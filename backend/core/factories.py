from datetime import timedelta
import itertools

from django.utils import timezone
import factory.fuzzy

from core.constants import ITEM_STATUS
from core.models import Item

hours_gen = (timezone.now() + timedelta(hours=i) for i in itertools.count())


class CreatedAtMixin:
    """
    override Item.created_at.auto_now_add
    # https://github.com/FactoryBoy/factory_boy/issues/102

    to get random dates:
        past_datetime = factory.Faker('past_datetime', start_date="-30d", tzinfo=pytz.UTC)
        ...
        instance.created_at = past_datetime.evaluate(None, None, {})

    Will not work with create_batch
    """
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        instance.created_at = next(hours_gen)
        instance.save()
        return instance


class ItemFactory(CreatedAtMixin, factory.django.DjangoModelFactory):
    title = factory.Faker('sentence', nb_words=2)
    desc = factory.Faker('paragraph', nb_sentences=3, variable_nb_sentences=True)
    status = factory.fuzzy.FuzzyChoice(ITEM_STATUS.ALL)

    class Meta:
        model = Item
