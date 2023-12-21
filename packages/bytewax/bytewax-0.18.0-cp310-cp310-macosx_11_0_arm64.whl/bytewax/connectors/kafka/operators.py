"""Operators for the kafka source and sink."""
from dataclasses import dataclass
from typing import Dict, Generic, List, Optional, Union, cast

from confluent_kafka import OFFSET_BEGINNING
from confluent_kafka import KafkaError as ConfluentKafkaError

import bytewax.operators as op
from bytewax.dataflow import Dataflow
from bytewax.operators import Stream, operator

from ._types import K2, V2, K, MaybeStrBytes, V
from .error import KafkaError
from .message import KafkaSinkMessage, KafkaSourceMessage
from .serde import SchemaDeserializer, SchemaSerializer
from .sink import KafkaSink
from .source import KafkaSource

__all__ = [
    "deserialize",
    "deserialize_key",
    "deserialize_value",
    "serialize",
    "serialize_key",
    "serialize_value",
    "input",
    "output",
]


@dataclass(frozen=True)
class KafkaSourceOut(Generic[K, V, K2, V2]):
    """Contains two streams of KafkaMessages, oks and errors.

    - KafkaStreams.oks:
        A stream of `KafkaMessage`s where `KafkaMessage.error is None`
    - KafkaStreams.errors:
        A stream of `KafkaMessage`s where `KafkaMessage.error is not None`
    """

    oks: Stream[KafkaSourceMessage[K, V]]
    errs: Stream[KafkaError[K2, V2]]


@operator
def _kafka_error_split(
    step_id: str, up: Stream[Union[KafkaSourceMessage[K2, V2], KafkaError[K, V]]]
) -> KafkaSourceOut[K2, V2, K, V]:
    """Split a stream of KafkaMessages in two."""
    branch = op.branch("branch", up, lambda msg: isinstance(msg, KafkaSourceMessage))
    # Cast the streams to the proper expected types.
    oks = cast(Stream[KafkaSourceMessage[K2, V2]], branch.trues)
    errs = cast(Stream[KafkaError[K, V]], branch.falses)
    return KafkaSourceOut(oks, errs)


@operator
def _to_sink(
    step_id: str, up: Stream[Union[KafkaSourceMessage[K, V], KafkaSinkMessage[K, V]]]
) -> Stream[KafkaSinkMessage[K, V]]:
    """Automatically convert a KafkaSourceMessage to KafkaSinkMessage."""

    def shim_mapper(
        msg: Union[KafkaSourceMessage[K, V], KafkaSinkMessage[K, V]],
    ) -> KafkaSinkMessage[K, V]:
        if isinstance(msg, KafkaSourceMessage):
            return msg.to_sink()
        else:
            return msg

    return op.map("map", up, shim_mapper)


@operator
def input(  # noqa A001
    step_id: str,
    flow: Dataflow,
    *,
    brokers: List[str],
    topics: List[str],
    tail: bool = True,
    starting_offset: int = OFFSET_BEGINNING,
    add_config: Optional[Dict[str, str]] = None,
    batch_size: int = 1000,
) -> KafkaSourceOut[MaybeStrBytes, MaybeStrBytes, MaybeStrBytes, MaybeStrBytes]:
    """Use a set of Kafka topics as an input source.

    Partitions are the unit of parallelism.
    Can support exactly-once processing.

    Messages are emitted into the dataflow
    as `bytewax.connectors.kafka.KafkaMessage` objects.

    Args:
        step_id:
            Unique name for this step
        flow:
            A Dataflow
        brokers:
            List of `host:port` strings of Kafka brokers.
        topics:
            List of topics to consume from.
        tail:
            Whether to wait for new data on this topic when the
            end is initially reached.
        starting_offset:
            Can be either `confluent_kafka.OFFSET_BEGINNING` or
            `confluent_kafka.OFFSET_END`. Defaults to beginning of
            topic.
        add_config:
            Any additional configuration properties. See the `rdkafka`
            [docs](https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md)
            for options.
        batch_size:
            How many messages to consume at most at each poll. Defaults to 1000.
    """
    return op.input(
        "kafka_input",
        flow,
        KafkaSource(
            brokers,
            topics,
            tail,
            starting_offset,
            add_config,
            batch_size,
            # Don't raise on errors, since we split
            # the stream and let users handle that
            raise_on_errors=False,
        ),
    ).then(_kafka_error_split, "split_err")


@operator
def output(
    step_id: str,
    up: Stream[Union[KafkaSourceMessage, KafkaSinkMessage]],
    *,
    brokers: List[str],
    topic: str,
    add_config: Optional[Dict[str, str]] = None,
) -> None:
    """Use a single Kafka topic as an output sink.

    Items consumed from the dataflow must look like two-tuples of
    `(key_bytes, value_bytes)`. Default partition routing is used.

    Workers are the unit of parallelism.

    Can support at-least-once processing. Messages from the resume
    epoch will be duplicated right after resume.

    Args:
        step_id:
            Unique name for this step
        up:
            A stream of `(key_bytes, value_bytes)` 2-tuples
        brokers:
            List of `host:port` strings of Kafka brokers.
        topic:
            Topic to produce to.
        add_config:
            Any additional configuration properties. See the `rdkafka`
            [docs](https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md)
            for options.
    """
    return _to_sink("to_sink", up).then(
        op.output, "kafka_output", KafkaSink(brokers, topic, add_config)
    )


@operator
def deserialize_key(
    step_id: str,
    up: Stream[KafkaSourceMessage[K, V]],
    deserializer: SchemaDeserializer[K, K2],
) -> KafkaSourceOut[K2, V, K, V]:
    """Deserialize the key of a KafkaMessage using the provided SchemaDeserializer.

    Returns an object with two attributes:
        - .oks: A stream of `KafkaMessage`s where `KafkaMessage.error is None`
        - .errors: A stream of `KafkaMessage`s where `KafkaMessage.error is not None`
    """

    # Make sure the first KafkaMessage in the return type's Union represents
    # the `oks` stream and the second one the `errs` stream for the
    # `_kafka_error_split` operator.
    def shim_mapper(
        msg: KafkaSourceMessage[K, V],
    ) -> Union[KafkaSourceMessage[K2, V], KafkaError[K, V]]:
        try:
            key = deserializer.de(msg.key)
            return msg._with_key(key)
        except Exception as e:
            err = ConfluentKafkaError(ConfluentKafkaError._KEY_DESERIALIZATION, f"{e}")
            return KafkaError(err, msg)

    return op.map("map", up, shim_mapper).then(_kafka_error_split, "split")


@operator
def deserialize_value(
    step_id: str,
    up: Stream[KafkaSourceMessage[K, V]],
    deserializer: SchemaDeserializer[V, V2],
) -> KafkaSourceOut[K, V2, K, V]:
    """Deserialize the value of a KafkaMessage using the provided SchemaDeserializer.

    Returns an object with two attributes:
        - .oks: A stream of `KafkaMessage`s where `KafkaMessage.error is None`
        - .errors: A stream of `KafkaMessage`s where `KafkaMessage.error is not None`
    """

    def shim_mapper(
        msg: KafkaSourceMessage[K, V],
    ) -> Union[KafkaSourceMessage[K, V2], KafkaError[K, V]]:
        try:
            value = deserializer.de(msg.value)
            return msg._with_value(value)
        except Exception as e:
            err = ConfluentKafkaError(
                ConfluentKafkaError._VALUE_DESERIALIZATION, f"{e}"
            )
            return KafkaError(err, msg)

    return op.map("map", up, shim_mapper).then(_kafka_error_split, "split_err")


@operator
def deserialize(
    step_id: str,
    up: Stream[KafkaSourceMessage[K, V]],
    *,
    key_deserializer: SchemaDeserializer[K, K2],
    val_deserializer: SchemaDeserializer[V, V2],
) -> KafkaSourceOut[K2, V2, K, V]:
    """Serialize both keys and values with the given serializers.

    Returns an object with two attributes:
        - .oks: A stream of `KafkaMessage`s where `KafkaMessage.error is None`
        - .errors: A stream of `KafkaMessage`s where `KafkaMessage.error is not None`
    A message will be put in .errors even if only one of the deserializers fail.
    """

    # Use a single map step rather than concatenating
    # deserialize_key and deserialize_value so we can
    # return the original message if any of the 2 fail.
    def shim_mapper(
        msg: KafkaSourceMessage[K, V],
    ) -> Union[KafkaSourceMessage[K2, V2], KafkaError[K, V]]:
        try:
            key = key_deserializer.de(msg.key)
        except Exception as e:
            err = ConfluentKafkaError(ConfluentKafkaError._KEY_DESERIALIZATION, f"{e}")
            return KafkaError(err, msg)

        try:
            value = val_deserializer.de(msg.value)
        except Exception as e:
            err = ConfluentKafkaError(
                ConfluentKafkaError._VALUE_DESERIALIZATION, f"{e}"
            )
            return KafkaError(err, msg)

        return msg._with_key_and_value(key, value)

    return op.map("map", up, shim_mapper).then(_kafka_error_split, "split_err")


@operator
def serialize_key(
    step_id: str,
    up: Stream[Union[KafkaSourceMessage[K, V], KafkaSinkMessage[K, V]]],
    serializer: SchemaSerializer[K, K2],
) -> Stream[KafkaSinkMessage[K2, V]]:
    """Serialize the key of a KafkaMessage using the provided SchemaSerializer.

    Crash if any error occurs.
    """

    def shim_mapper(msg: KafkaSinkMessage[K, V]) -> KafkaSinkMessage[K2, V]:
        key = serializer.ser(msg.key)
        return msg._with_key(key)

    return _to_sink("to_sink", up).then(op.map, "map", shim_mapper)


@operator
def serialize_value(
    step_id: str,
    up: Stream[Union[KafkaSourceMessage[K, V], KafkaSinkMessage[K, V]]],
    serializer: SchemaSerializer[V, V2],
) -> Stream[KafkaSinkMessage[K, V2]]:
    """Serialize the value of a KafkaMessage using the provided SchemaSerializer.

    Crash if any error occurs.
    """

    def shim_mapper(msg: KafkaSinkMessage[K, V]) -> KafkaSinkMessage[K, V2]:
        value = serializer.ser(msg.value)
        return msg._with_value(value)

    return _to_sink("to_sink", up).then(op.map, "map", shim_mapper)


@operator
def serialize(
    step_id: str,
    up: Stream[Union[KafkaSourceMessage[K, V], KafkaSinkMessage[K, V]]],
    *,
    key_serializer: SchemaSerializer[K, K2],
    val_serializer: SchemaSerializer[V, V2],
) -> Stream[KafkaSinkMessage[K2, V2]]:
    """Serialize both keys and values with the given serializers.

    Crash if any error occurs.
    """

    def shim_mapper(msg: KafkaSinkMessage[K, V]) -> KafkaSinkMessage[K2, V2]:
        key = key_serializer.ser(msg.key)
        value = val_serializer.ser(msg.value)
        return msg._with_key_and_value(key, value)

    return _to_sink("to_sink", up).then(op.map, "map", shim_mapper)
