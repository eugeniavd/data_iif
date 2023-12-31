from sqlite3 import connect
import pandas as pd
from json import load
from rdflib import Graph, Literal, RDF, RDFS, URIRef


def upload_to_db(db_path, df, name):
    # auxiliary function for database updates. 
    # it loads data from dataframes, in case of an error, returns a value of False
    try:
        df.to_sql(name, connect(db_path), if_exists='replace', index=False)
        return True
    except Exception as e:
        print(f"Upload failed: {e}")
        return False


def remove_invalid_char(string):
    # auxiliary function, it removes invalid chars found in the imported data
    if '\"' in string:
        return string.replace('\"', '\\\"')
    elif '"' in string:
        return string.replace('"', '\\\"')
    else:
        return string


def create_graph(json_obj, base_url, graph):
    # auxiliary function, it creates URI for a graph database
    collection_id = URIRef(json_obj['id'])

    # defining URIs types
    type_canvas = URIRef(base_url + 'Canvas')
    type_collection = URIRef(base_url + 'Collection')
    type_manifest = URIRef(base_url + 'Manifest')
    type_metadata = URIRef(base_url + 'Metadata')

    # defining  URIs properties
    prop_id = URIRef('https://schema.org/identifier')
    prop_label = URIRef(base_url + 'label')
    prop_items = URIRef(base_url + 'items')

    # labeling json_obj
    label_list = list(json_obj['label'].values())
    label_value = label_list[0][0]
    label_value = remove_invalid_char(str(label_value))

    # creating triples 
    graph.add((collection_id, prop_id, Literal(json_obj['id'])))
    graph.add((collection_id, RDF.type, type_collection))
    graph.add((collection_id, RDFS.label, Literal(str(label_value))))

    # populating manifests
    for manifest in json_obj['items']:
        manifest_id = URIRef(manifest['id'])

        graph.add((collection_id, prop_items, manifest_id))
        graph.add((manifest_id, prop_id, Literal(manifest['id'])))
        graph.add((manifest_id, RDF.type, type_manifest))
        
        manifest_label_list = list(manifest['label'].values())
        manifest_label_value = manifest_label_list[0][0]
        manifest_label_value = remove_invalid_char(str(manifest_label_value))

        graph.add((manifest_id, RDFS.label, Literal(str(manifest_label_value))))

        # populating canvases
        for canvas in manifest['items']:
            canvas_id = URIRef(canvas['id'])

            graph.add((manifest_id, prop_items, canvas_id))
            graph.add((canvas_id, prop_id, Literal(canvas['id'])))
            graph.add((canvas_id, RDF.type, type_canvas))

            canvas_label_list = list(canvas['label'].values())
            canvas_label_value = canvas_label_list[0][0]
            canvas_label_value = remove_invalid_char(str(canvas_label_value))

            graph.add((canvas_id, RDFS.label, Literal(str(canvas_label_value))))