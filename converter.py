"""converter.py

Takes a JSON ScienceParse file and converts it into LIF.

Usage:

>>> from converter import Converter
>>> converter = Converter(open('data/input.json').read())
>>> if converter.error is None:
...     len(converter.get_container_as_json_string())
14039

If there was an error it is stored in the error variable:

>>> if converter.error is not None:
...     print(repr(converter.error))


"""

import json
from io import StringIO

import jsonschema

from lif import LIF, Container, View, Annotation


LIF_SCHEMA = 'lif.json'


class Converter(object):

    def __init__(self, science_parse_output):
        self.json_obj = json.loads(science_parse_output)
        self.lif_obj = LIF()
        self.error = None
        self.container = None
        self.convert()

    def convert(self):
        self._add_metadata()
        self._add_view()
        self._add_rest()
        try:
            self._validate()
            self.container = Container()
            self.container.discriminator = "http://vocab.lappsgrid.org/ns/media/jsonld#lif"
            self.container.payload = self.lif_obj
        except jsonschema.exceptions.ValidationError as e:
            self.error = e
        
    def _add_metadata(self):
        self.lif_obj.metadata['id'] = self.json_obj.get('id')
        self.lif_obj.metadata['authors'] = self.json_obj['metadata'].get('authors', [])
        self.lif_obj.metadata['title'] = self.json_obj['metadata'].get('title')
        self.lif_obj.metadata['year'] = self.json_obj['metadata'].get('year')
        self.lif_obj.metadata['references'] = self.json_obj['metadata'].get('references', [])

    def _add_view(self):
        view = View()
        view.id = "structure"
        view.metadata['contains'] = { vocab("Title"): {}, vocab("Abstract"): {},
                                      vocab("Section"): {}, vocab("Header"): {} }
        self.lif_obj.views.append(view)

    def _add_rest(self):
        text_value = StringIO()
        offset = 0
        annotations = self.lif_obj.views[0].annotations
        offset = _add_annotation(annotations, text_value, 'Title',
                                 self.json_obj['metadata'].get('title'), offset)
        offset = _add_annotation(annotations, text_value, 'Abstract',
                                 self.json_obj['metadata'].get('abstractText'), offset)
        for section in self.json_obj['metadata']['sections']:
            offset = _add_annotation(annotations, text_value, 'Header',
                                     section.get('heading'), offset)
            offset = _add_annotation(annotations, text_value, 'Section',
                                     section.get('text'), offset)
        self.lif_obj.text.value = text_value.getvalue()

    def _validate(self):
        lif_obj = self.lif_obj.as_json()
        json_schema = json.load(open(LIF_SCHEMA))
        jsonschema.validate(instance=lif_obj, schema=json_schema)

    def get_container_as_json_string(self, indent=2):
        return json.dumps(self.container.as_json(), indent=indent)

    def get_text_value(self):
        return self.container.payload.text.value


def _add_annotation(annotations, text_value, annotation_type, text, offset):
    if text is None:
        return offset
    prefix = None
    if annotation_type in ('Title', 'Abstract'):
        prefix = annotation_type.upper()
    if prefix is not None:
        anno = {
            "id": IdentifierFactory.next_id('Header'),
            "@type": vocab('Header'),
            "start": offset,
            "end": offset + len(prefix) } 
        annotations.append(Annotation(anno))
        text_value.write(prefix + u"\n\n")
        offset += len(prefix) + 2
    anno = {
        "id": IdentifierFactory.next_id(annotation_type),
        "@type": vocab(annotation_type),
        "start": offset,
        "end": offset + len(text) } 
    annotations.append(Annotation(anno))
    text_value.write(text + u"\n\n")
    return offset + len(text) + 2


def vocab(annotation_type):
    return "http://vocab.lappsgrid.org/{}".format(annotation_type)

        
class IdentifierFactory(object):
    
    ids = { 'Title': 0, 'Abstract': 0, 'Header': 0, 'Section': 0 }

    @classmethod
    def next_id(cls, tagname):
        cls.ids[tagname] += 1
        return "{}{:04d}".format(tagname.lower(), cls.ids[tagname])


if __name__ == '__main__':

    import doctest
    doctest.testmod()
