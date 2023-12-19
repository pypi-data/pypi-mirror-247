import json

import pytest

from tests.unit.resources import SEARCHED_SUBMISSION
from trustar2.models.searched_submission import SearchedSubmission


TITLE = "Test Submission Title"
GUID = "test-guid"
ENCLAVE_GUID = "test-enclave-guid"
CREATED = 1624980621003
UPDATED = 1624980621003
TAGS = []


@pytest.fixture
def searched_submission_obj():
    return SearchedSubmission(
        guid=GUID,
        enclave_guid=ENCLAVE_GUID,
        title=TITLE,
        created=CREATED,
        updated=UPDATED,
        tags=TAGS
    )


@pytest.fixture
def searched_submission_json():
    return json.loads(SEARCHED_SUBMISSION)


def test_searched_submission_deserialization(searched_submission_json):
    searched_submission = SearchedSubmission.from_dict(searched_submission_json)

    assert searched_submission.title == TITLE
    assert searched_submission.guid == GUID
    assert searched_submission.enclave_guid == ENCLAVE_GUID
    assert searched_submission.created == CREATED
    assert searched_submission.updated == UPDATED
    assert searched_submission.tags == TAGS


def test_searched_submission_serialization(searched_submission_obj, searched_submission_json):
    current_submission = searched_submission_obj.serialize()
    all_required_values_are_equal = all(current_submission.get(k) == searched_submission_json.get(k)
                                            for k in current_submission.keys())

    assert all_required_values_are_equal


def test_searched_submission_repr(searched_submission_obj):
    assert searched_submission_obj.__repr__() == "SearchedSubmission(title={})".format(TITLE)
