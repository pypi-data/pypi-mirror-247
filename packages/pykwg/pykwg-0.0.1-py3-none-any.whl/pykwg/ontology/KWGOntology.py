from rdflib import Namespace, RDFS, RDF, TIME, OWL, XSD
from rdflib.namespace import DefinedNamespace
from ..config import Config


class KWGOntology(DefinedNamespace):
    def __init__(self):
        super().__init__()
        config = Config()
        self.prefix = {
            "kwgr": Namespace(f"{config.base_address}lod/resource"),
            "kwg-ont": Namespace(f"{config.base_address}lod/ontology"),
            "geo": Namespace("http://www.opengis.net/ont/geosparql#"),
            "geof": Namespace("http://www.opengis.net/def/function/geosparql/"),
            "sf": Namespace("http://www.opengis.net/ont/sf#"),
            "wd": Namespace("http://www.wikidata.org/entity/"),
            "wdt": Namespace("http://www.wikidata.org/prop/direct/"),
            "rdf": RDF,
            "rdfs": RDFS,
            "xsd": XSD,
            "owl": OWL,
            "time": TIME,
            "dbo": Namespace("http://dbpedia.org/ontology/"),
            "ssn": Namespace("http://www.w3.org/ns/ssn/"),
            "sosa": Namespace("http://www.w3.org/ns/sosa/"),
        }
