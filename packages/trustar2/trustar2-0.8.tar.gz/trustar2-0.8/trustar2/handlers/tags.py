from trustar2.query import Query
from trustar2.handlers.base_handler import BaseHandler
from trustar2.base import Methods, fluent
from trustar2.models.trustar_response import TruStarResponse
from trustar2.trustar_enums import TagsEnum, ObservablesEnum, SubmissionEnum

ADDED_TAGS = TagsEnum.ADDED_TAGS.value
REMOVED_TAGS = TagsEnum.REMOVED_TAGS.value
ENCLAVE_ID = TagsEnum.ENCLAVE_ID.value
ENCLAVE_GUID = TagsEnum.ENCLAVE_GUID.value


@fluent
class TagBase(BaseHandler):

    def __init__(self, endpoint, config=None):
        super(TagBase, self).__init__(config)
        self.guid = None
        self._url = endpoint

    @property
    def base_url(self):
        return f"{self.config.request_details.get('api_endpoint')}/{self._url}"

    def _validate_payload(self):
        if self.guid is None:
            raise AttributeError(f"Id value is required for altering tags of {self._url}")

        added_tags = self.payload_params.get(ADDED_TAGS, [])
        removed_tags = self.payload_params.get(REMOVED_TAGS, [])

        if not (len(added_tags) or len(removed_tags)):
            msg = (f"Either 'addedTags' or 'removedTags' \
                   values are required for altering tags of {self._url}"
            )
            raise AttributeError(msg)

        if ENCLAVE_GUID not in self.payload_params and ENCLAVE_ID not in self.payload_params:
            raise AttributeError(f"Enclave id value is required for altering tags on {self._url}")


    @property
    def tag_endpoint(self):
        self._validate_payload()
        return f"{self.base_url}/{self.guid}/alter-tags"

    def _validate_tags(self, tags):
        iterables = (list, tuple, set)
        if type(tags) not in iterables:
            raise AttributeError(f"addedTags {tags} should be a list of string values")

    def set_added_tags(self, added_tags):
        self._validate_tags(added_tags)
        self.set_payload_param(ADDED_TAGS, added_tags)


    def set_removed_tags(self, removed_tags):
        self._validate_tags(removed_tags)
        self.set_payload_param(REMOVED_TAGS, removed_tags)


    def set_enclave_id(self, enclave_guid):
        if self._url == "submissions":
            self.set_payload_param(ENCLAVE_ID, enclave_guid)
        else:
            self.set_payload_param(ENCLAVE_GUID, enclave_guid)

    def alter_tags(self):
        result = (
            Query(self.config, self.tag_endpoint, Methods.POST)
            .set_params(self.payload_params)
            .execute()
        )
        return TruStarResponse(status_code=result.status_code, data=result.json())


@fluent
class TagIndicator(TagBase):

    def __init__(self, config=None):
        super(TagIndicator, self).__init__("indicators", config)


    def set_indicator_id(self, indicator_id):
        self.guid = indicator_id


@fluent
class TagSubmission(TagBase):

    def __init__(self, config=None):
        super(TagSubmission, self).__init__("submissions", config)


    def set_submission_id(self, submission_id):
        self.guid = submission_id


    def set_id_type_as_external(self, external):
        self.set_payload_param(SubmissionEnum.ID_TYPE.value, "EXTERNAL" if external else "INTERNAL")


@fluent
class TagObservable(TagBase):

    def __init__(self, config=None):
        super(TagObservable, self).__init__("observables", config)


    def set_observable_value(self, value):
        self.guid = value
        self.set_payload_param(ObservablesEnum.OBSERVABLE_VALUE.value, value)

    @property
    def tag_endpoint(self):
        self._validate_payload()
        return f"{self.base_url}/alter-tags"
