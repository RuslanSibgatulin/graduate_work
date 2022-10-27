# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='service.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\rservice.proto\" \n\x0cMovieRequest\x12\x10\n\x08movie_id\x18\x01 \x01(\t\"7\n\x05Movie\x12\x10\n\x08movie_id\x18\x01 \x01(\t\x12\r\n\x05title\x18\x02 \x01(\t\x12\r\n\x05score\x18\x03 \x01(\r26\n\rMoviesService\x12%\n\x0cGetMovieInfo\x12\r.MovieRequest\x1a\x06.Movieb\x06proto3'
)




_MOVIEREQUEST = _descriptor.Descriptor(
  name='MovieRequest',
  full_name='MovieRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='movie_id', full_name='MovieRequest.movie_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=17,
  serialized_end=49,
)


_MOVIE = _descriptor.Descriptor(
  name='Movie',
  full_name='Movie',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='movie_id', full_name='Movie.movie_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='title', full_name='Movie.title', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='score', full_name='Movie.score', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=51,
  serialized_end=106,
)

DESCRIPTOR.message_types_by_name['MovieRequest'] = _MOVIEREQUEST
DESCRIPTOR.message_types_by_name['Movie'] = _MOVIE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MovieRequest = _reflection.GeneratedProtocolMessageType('MovieRequest', (_message.Message,), {
  'DESCRIPTOR' : _MOVIEREQUEST,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:MovieRequest)
  })
_sym_db.RegisterMessage(MovieRequest)

Movie = _reflection.GeneratedProtocolMessageType('Movie', (_message.Message,), {
  'DESCRIPTOR' : _MOVIE,
  '__module__' : 'service_pb2'
  # @@protoc_insertion_point(class_scope:Movie)
  })
_sym_db.RegisterMessage(Movie)



_MOVIESSERVICE = _descriptor.ServiceDescriptor(
  name='MoviesService',
  full_name='MoviesService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=108,
  serialized_end=162,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetMovieInfo',
    full_name='MoviesService.GetMovieInfo',
    index=0,
    containing_service=None,
    input_type=_MOVIEREQUEST,
    output_type=_MOVIE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MOVIESSERVICE)

DESCRIPTOR.services_by_name['MoviesService'] = _MOVIESSERVICE

# @@protoc_insertion_point(module_scope)