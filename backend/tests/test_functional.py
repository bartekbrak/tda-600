from django.urls import reverse
import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from core.constants import ITEM_STATUS
from core.factories import ItemFactory
from core.models import Item


@pytest.mark.django_db
def test_standard_scenario(api_client):
    """
    User:
    - opens the app,
    - receives some items of various statuses,
    - decides to complete two items,
    - delete one
    - edit just title of one
    - and add one
    """
    batch = ItemFactory.create_batch(8)
    the_pending = ItemFactory.create_batch(2, status=ITEM_STATUS.PENDING)
    some_items = api_client.get(reverse('items-list'))
    assert some_items.status_code == HTTP_200_OK
    assert some_items.json()
    assert 'items' in some_items.json()
    assert len(some_items.json()['items']) == 10

    first, second = the_pending
    first_complete = api_client.patch(
        reverse('items-detail', kwargs={'pk': first.id}),
        data={'status': ITEM_STATUS.DONE},
    )
    second_complete = api_client.patch(
        reverse('items-detail', kwargs={'pk': second.id}),
        data={'status': ITEM_STATUS.DONE},
    )
    first.refresh_from_db()
    second.refresh_from_db()
    assert first_complete.status_code == second_complete.status_code == HTTP_200_OK
    assert first.status == ITEM_STATUS.DONE
    assert second.status == ITEM_STATUS.DONE

    to_be_deleted = batch[0]
    delete_one = api_client.delete(reverse('items-detail', kwargs={'pk': to_be_deleted.id}))
    assert delete_one.status_code == HTTP_204_NO_CONTENT
    with pytest.raises(Item.DoesNotExist):
        to_be_deleted.refresh_from_db()

    just_title = batch[1]
    new_title = 'new_title'
    patch_the_title = api_client.patch(
        reverse('items-detail', kwargs={'pk': just_title.id}),
        data={'title': new_title}
    )
    assert patch_the_title.status_code == HTTP_200_OK
    just_title.refresh_from_db()
    assert just_title.title == new_title

    add_one = api_client.post(
        reverse('items-list'),
        data={
            'title': 'title',
            'desc': 'desc',
        }
    )
    assert add_one.status_code == HTTP_201_CREATED
    assert Item.objects.filter(pk=add_one.json()['item']['id']).exists()
