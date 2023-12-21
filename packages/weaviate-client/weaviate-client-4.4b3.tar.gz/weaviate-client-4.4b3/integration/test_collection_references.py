from typing import Generator, TypedDict
from typing_extensions import Annotated

import pytest as pytest
import uuid

from weaviate.collections.classes.data import DataObject, DataReference, DataReferenceOneToMany
from weaviate.collections.classes.grpc import FromReference, FromReferenceMultiTarget, MetadataQuery

import weaviate
from weaviate.collections.classes.config import (
    Configure,
    Property,
    DataType,
    ReferenceProperty,
    ReferencePropertyMultiTarget,
)

from weaviate.collections.classes.internal import CrossReference, Reference, ReferenceAnnotation


@pytest.fixture(scope="module")
def client() -> Generator[weaviate.WeaviateClient, None, None]:
    client = weaviate.connect_to_local()
    client.collections.delete_all()
    yield client
    client.collections.delete_all()


def test_reference_add_delete_replace(client: weaviate.WeaviateClient) -> None:
    ref_collection = client.collections.create(
        name="RefClass2", vectorizer_config=Configure.Vectorizer.none()
    )
    uuid_to = ref_collection.data.insert(properties={})
    collection = client.collections.create(
        name="SomethingElse",
        references=[ReferenceProperty(name="ref", target_collection="RefClass2")],
        vectorizer_config=Configure.Vectorizer.none(),
    )

    uuid_from1 = collection.data.insert({}, uuid=uuid.uuid4())
    uuid_from2 = collection.data.insert(
        {}, references={"ref": Reference.to(uuids=uuid_to)}, uuid=uuid.uuid4()
    )
    collection.data.reference_add(
        from_uuid=uuid_from1, from_property="ref", to=Reference.to(uuids=uuid_to)
    )

    collection.data.reference_delete(
        from_uuid=uuid_from1, from_property="ref", to=Reference.to(uuids=uuid_to)
    )
    assert (
        len(
            collection.query.fetch_object_by_id(
                uuid_from1, return_references=FromReference(link_on="ref")
            )
            .references["ref"]
            .objects
        )
        == 0
    )

    collection.data.reference_add(
        from_uuid=uuid_from2, from_property="ref", to=Reference.to(uuids=uuid_to)
    )
    obj = collection.query.fetch_object_by_id(
        uuid_from2, return_references=FromReference(link_on="ref")
    )
    assert obj is not None
    assert len(obj.references["ref"].objects) == 2
    assert uuid_to in [x.uuid for x in obj.references["ref"].objects]

    collection.data.reference_replace(
        from_uuid=uuid_from2, from_property="ref", to=Reference.to(uuids=[])
    )
    assert (
        len(
            collection.query.fetch_object_by_id(
                uuid_from2, return_references=FromReference(link_on="ref")
            )
            .references["ref"]
            .objects
        )
        == 0
    )

    client.collections.delete("SomethingElse")
    client.collections.delete("RefClass2")


def test_mono_references_grpc(client: weaviate.WeaviateClient) -> None:
    A = client.collections.create(
        name="A",
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
        ],
    )
    uuid_A1 = A.data.insert(properties={"Name": "A1"})
    uuid_A2 = A.data.insert(properties={"Name": "A2"})

    a_objs = A.query.bm25(query="A1", return_properties="name").objects
    assert a_objs[0].properties["name"] == "A1"

    B = client.collections.create(
        name="B",
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferenceProperty(name="a", target_collection="A"),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    uuid_B = B.data.insert({"Name": "B"}, references={"a": Reference.to(uuids=uuid_A1)})
    B.data.reference_add(from_uuid=uuid_B, from_property="a", to=Reference.to(uuids=uuid_A2))

    b_objs = B.query.bm25(
        query="B",
        return_references=FromReference(
            link_on="a",
            return_properties=["name"],
        ),
    ).objects
    assert b_objs[0].references["a"].objects[0].properties["name"] == "A1"
    assert b_objs[0].references["a"].objects[0].uuid == uuid_A1
    assert b_objs[0].references["a"].objects[1].properties["name"] == "A2"
    assert b_objs[0].references["a"].objects[1].uuid == uuid_A2

    C = client.collections.create(
        name="C",
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferenceProperty(name="b", target_collection="B"),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    C.data.insert({"Name": "find me"}, references={"b": Reference.to(uuids=uuid_B)})

    c_objs = C.query.bm25(
        query="find",
        return_properties="name",
        return_references=FromReference(
            link_on="b",
            return_properties="name",
            return_metadata=MetadataQuery(last_update_time=True),
            return_references=FromReference(
                link_on="a",
                return_properties="name",
            ),
        ),
    ).objects
    assert c_objs[0].properties["name"] == "find me"
    assert c_objs[0].references["b"].objects[0].properties["name"] == "B"
    assert c_objs[0].references["b"].objects[0].metadata.last_update_time is not None
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[0].properties["name"] == "A1"
    )
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[1].properties["name"] == "A2"
    )


@pytest.mark.parametrize("level", ["col-col", "col-query", "query-col", "query-query"])
def test_mono_references_grpc_typed_dicts(client: weaviate.WeaviateClient, level: str) -> None:
    client.collections.delete("ATypedDicts")
    client.collections.delete("BTypedDicts")
    client.collections.delete("CTypedDicts")

    class AProps(TypedDict):
        name: str

    class BProps(TypedDict):
        name: str

    class BRefs(TypedDict):
        a: Annotated[
            CrossReference[AProps, None],
            ReferenceAnnotation(metadata=MetadataQuery(creation_time=True)),
        ]

    class CProps(TypedDict):
        name: str

    class CRefs(TypedDict):
        b: Annotated[CrossReference[BProps, BRefs], ReferenceAnnotation(include_vector=True)]

    client.collections.create(
        name="ATypedDicts",
        vectorizer_config=Configure.Vectorizer.text2vec_contextionary(
            vectorize_collection_name=False
        ),
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
        ],
    )
    A = client.collections.get("ATypedDicts", AProps)
    uuid_A1 = A.data.insert(AProps(name="A1"))
    uuid_A2 = A.data.insert(AProps(name="A2"))

    client.collections.create(
        name="BTypedDicts",
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferenceProperty(name="a", target_collection="ATypedDicts"),
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_contextionary(
            vectorize_collection_name=False
        ),
    )
    B = client.collections.get("BTypedDicts", BProps)
    uuid_B = B.data.insert(properties={"name": "B"}, references={"a": Reference.to(uuids=uuid_A1)})
    B.data.reference_add(
        from_uuid=uuid_B,
        from_property="a",
        to=Reference.to(uuids=uuid_A2),
    )

    b_objs = B.query.bm25(query="B", return_references=BRefs).objects
    assert b_objs[0].references["a"].objects[0].properties["name"] == "A1"
    assert b_objs[0].references["a"].objects[0].uuid == uuid_A1
    assert b_objs[0].references["a"].objects[0].references is None
    assert b_objs[0].references["a"].objects[1].properties["name"] == "A2"
    assert b_objs[0].references["a"].objects[1].uuid == uuid_A2
    assert b_objs[0].references["a"].objects[1].references is None

    client.collections.create(
        name="CTypedDicts",
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
            Property(name="Age", data_type=DataType.INT),
        ],
        references=[
            ReferenceProperty(name="b", target_collection="BTypedDicts"),
        ],
        vectorizer_config=Configure.Vectorizer.text2vec_contextionary(
            vectorize_collection_name=False
        ),
    )
    C = client.collections.get("CTypedDicts", CProps)
    C.data.insert(properties={"name": "find me"}, references={"b": Reference.to(uuids=uuid_B)})

    if level == "col-col":
        c_objs = (
            client.collections.get("CTypedDicts", CProps, CRefs)
            .query.bm25(query="find", include_vector=True)
            .objects
        )
    elif level == "col-query":
        c_objs = (
            client.collections.get("CTypedDicts", CProps)
            .query.bm25(
                query="find",
                include_vector=True,
                return_references=CRefs,
            )
            .objects
        )
    elif level == "query-col":
        c_objs = (
            client.collections.get("CTypedDicts", data_model_references=CRefs)
            .query.bm25(
                query="find",
                include_vector=True,
                return_properties=CProps,
            )
            .objects
        )
    else:
        c_objs = (
            client.collections.get("CTypedDicts")
            .query.bm25(
                query="find",
                include_vector=True,
                return_properties=CProps,
                return_references=CRefs,
            )
            .objects
        )
    assert (
        c_objs[0].properties["name"] == "find me"
    )  # happy path (in type and in return_properties)
    assert c_objs[0].uuid is not None
    assert c_objs[0].vector is not None
    assert (
        c_objs[0].properties.get("not_specified") is None
    )  # type is str but instance is None (in type but not in return_properties)
    assert c_objs[0].references["b"].objects[0].properties["name"] == "B"
    assert c_objs[0].references["b"].objects[0].uuid == uuid_B
    assert c_objs[0].references["b"].objects[0].vector is not None
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[0].properties["name"] == "A1"
    )
    assert c_objs[0].references["b"].objects[0].references["a"].objects[0].uuid == uuid_A1
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[0].metadata.creation_time
        is not None
    )
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[1].properties["name"] == "A2"
    )
    assert c_objs[0].references["b"].objects[0].references["a"].objects[1].uuid == uuid_A2
    assert (
        c_objs[0].references["b"].objects[0].references["a"].objects[1].metadata.creation_time
        is not None
    )


def test_multi_references_grpc(client: weaviate.WeaviateClient) -> None:
    client.collections.delete("A")
    client.collections.delete("B")
    client.collections.delete("C")

    A = client.collections.create(
        name="A",
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
        ],
    )
    uuid_A = A.data.insert(properties={"Name": "A"})

    B = client.collections.create(
        name="B",
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    uuid_B = B.data.insert({"Name": "B"})

    C = client.collections.create(
        name="C",
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferencePropertyMultiTarget(name="ref", target_collections=["A", "B"]),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    C.data.insert(
        {
            "Name": "first",
        },
        references={
            "ref": Reference.to_multi_target(uuids=uuid_A, target_collection="A"),
        },
    )
    C.data.insert(
        {
            "Name": "second",
        },
        references={
            "ref": Reference.to_multi_target(uuids=uuid_B, target_collection="B"),
        },
    )

    objects = C.query.bm25(
        query="first",
        return_properties="name",
        return_references=FromReferenceMultiTarget(
            link_on="ref",
            target_collection="A",
            return_properties=["name"],
            return_metadata=MetadataQuery(last_update_time=True),
        ),
    ).objects
    assert objects[0].properties["name"] == "first"
    assert len(objects[0].references["ref"].objects) == 1
    assert objects[0].references["ref"].objects[0].properties["name"] == "A"
    assert objects[0].references["ref"].objects[0].metadata.last_update_time is not None

    objects = C.query.bm25(
        query="second",
        return_properties="name",
        return_references=FromReferenceMultiTarget(
            link_on="ref",
            target_collection="B",
            return_properties=[
                "name",
            ],
            return_metadata=MetadataQuery(last_update_time=True),
        ),
    ).objects
    assert objects[0].properties["name"] == "second"
    assert len(objects[0].references["ref"].objects) == 1
    assert objects[0].references["ref"].objects[0].properties["name"] == "B"
    assert objects[0].references["ref"].objects[0].metadata.last_update_time is not None

    client.collections.delete("A")
    client.collections.delete("B")
    client.collections.delete("C")


def test_references_batch(client: weaviate.WeaviateClient) -> None:
    name_ref_to = "TestBatchRefTo"
    name_ref_from = "TestBatchRefFrom"

    client.collections.delete(name_ref_to)
    client.collections.delete(name_ref_from)

    ref_collection = client.collections.create(
        name=name_ref_to,
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[Property(name="num", data_type=DataType.INT)],
    )
    num_objects = 10

    uuids_to = ref_collection.data.insert_many(
        [DataObject(properties={"num": i}) for i in range(num_objects)]
    ).uuids.values()
    collection = client.collections.create(
        name=name_ref_from,
        properties=[
            Property(name="num", data_type=DataType.INT),
        ],
        references=[ReferenceProperty(name="ref", target_collection=name_ref_to)],
        vectorizer_config=Configure.Vectorizer.none(),
    )
    uuids_from = collection.data.insert_many(
        [DataObject(properties={"num": i}) for i in range(num_objects)]
    ).uuids.values()

    batch_return = collection.data.reference_add_many(
        [
            *[
                DataReferenceOneToMany(
                    from_property="ref",
                    from_uuid=list(uuids_from)[i],
                    to=Reference.to(list(uuids_to)[i]),
                )
                for i in range(num_objects)
            ],
            *[
                DataReference(
                    from_property="ref",
                    from_uuid=list(uuids_from)[i],
                    to_uuid=list(uuids_to)[i],
                )
                for i in range(num_objects)
            ],
        ]
    )

    assert batch_return.has_errors is False

    objects = collection.query.fetch_objects(
        return_properties=[
            "num",
        ],
        return_references=[
            FromReference(link_on="ref"),
        ],
    ).objects

    for obj in objects:
        assert obj.properties["num"] == obj.references["ref"].objects[0].properties["num"]


def test_insert_many_with_refs(client: weaviate.WeaviateClient) -> None:
    name = "TestInsertManyRefs"
    client.collections.delete(name)
    collection = client.collections.create(
        name=name,
        properties=[Property(name="Name", data_type=DataType.TEXT)],
        references=[
            ReferenceProperty(name="self", target_collection=name),
        ],
        vectorizer_config=Configure.Vectorizer.none(),
    )

    uuid1 = collection.data.insert({"name": "A"})
    uuid2 = collection.data.insert({"name": "B"})

    batch_return = collection.data.insert_many(
        [
            DataObject(
                properties={"name": "C"},
                references={"self": Reference.to(uuids=uuid1)},
            ),
            DataObject(
                properties={"name": "D"},
                references={"self": Reference.to(uuids=uuid2)},
            ),
        ]
    )
    assert batch_return.has_errors is False

    for obj in collection.query.fetch_objects(
        return_properties=["name"], return_references=FromReference(link_on="self")
    ).objects:
        if obj.properties["name"] in ["A", "B"]:
            assert obj.references is None
        else:
            assert obj.references is not None


def test_references_batch_with_errors(client: weaviate.WeaviateClient) -> None:
    name_ref_to = "TestBatchRefErrorTo"
    name_ref_from = "TestBatchRefErrorFrom"

    client.collections.delete(name_ref_to)
    client.collections.delete(name_ref_from)

    _ = client.collections.create(
        name=name_ref_to,
        vectorizer_config=Configure.Vectorizer.none(),
    )

    collection = client.collections.create(
        name=name_ref_from,
        properties=[
            Property(name="num", data_type=DataType.INT),
        ],
        references=[ReferenceProperty(name="ref", target_collection=name_ref_to)],
        vectorizer_config=Configure.Vectorizer.none(),
    )

    batch_return = collection.data.reference_add_many(
        [DataReference(from_property="doesNotExist", from_uuid=uuid.uuid4(), to_uuid=uuid.uuid4())],
    )
    assert batch_return.has_errors is True
    assert 0 in batch_return.errors


# commented out due to mypy failures since it is stale code
# @pytest.mark.skip(reason="string syntax has been temporarily removed from the API")
# def test_references_with_string_syntax(client: weaviate.WeaviateClient):
#     name1 = "TestReferencesWithStringSyntaxA"
#     name2 = "TestReferencesWithStringSyntaxB"
#     client.collections.delete(name1)
#     client.collections.delete(name2)

#     client.collections.create(
#         name=name1,
#         vectorizer_config=Configure.Vectorizer.none(),
#         properties=[
#             Property(name="Name", data_type=DataType.TEXT),
#             Property(name="Age", data_type=DataType.INT),
#             Property(name="Weird__Name", data_type=DataType.INT),
#         ],
#     )

#     uuid_A = client.collections.get(name1).data.insert(
#         properties={"Name": "A", "Age": 1, "Weird__Name": 2}
#     )

#     client.collections.get(name1).query.fetch_object_by_id(uuid_A)

#     client.collections.create(
#         name=name2,
#         properties=[
#             Property(name="Name", data_type=DataType.TEXT),
#         ],
#         references=[ReferenceProperty(name="ref", target_collection=name1)],
#         vectorizer_config=Configure.Vectorizer.none(),
#     )

#     client.collections.get(name2).data.insert(
#         {"Name": "B"}, references={"ref": Reference.to(uuids=uuid_A)}
#     )

#     objects = (
#         client.collections.get(name2)
#         .query.bm25(
#             query="B",
#             return_properties=[
#                 "name",
#                 "__ref__properties__Name",
#                 "__ref__properties__Age",
#                 "__ref__properties__Weird__Name",
#                 "__ref__metadata__last_update_time_unix",
#             ],
#         )
#         .objects
#     )

#     assert objects[0].properties["name"] == "B"
#     assert objects[0].references["ref"].objects[0].properties["name"] == "A"
#     assert objects[0].references["ref"].objects[0].properties["age"] == 1
#     assert objects[0].references["ref"].objects[0].properties["weird__Name"] == 2
#     assert objects[0].references["ref"].objects[0].uuid == uuid_A
#     assert objects[0].references["ref"].objects[0].metadata.last_update_time_unix is not None


def test_warning_refs_as_props(
    client: weaviate.WeaviateClient, recwarn: pytest.WarningsRecorder
) -> None:
    name = "TestRefsAsProps"
    client.collections.delete(name)

    client.collections.create(
        name=name,
        vectorizer_config=Configure.Vectorizer.none(),
        properties=[
            Property(name="Name", data_type=DataType.TEXT),
            ReferenceProperty(name="ref", target_collection=name),
        ],
    )

    assert len(recwarn) == 1
    w = recwarn.pop()
    assert issubclass(w.category, DeprecationWarning)
    assert str(w.message).startswith("Dep007")
