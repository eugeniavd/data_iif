# importing for relational database
from main import AnnotationProcessor, MetadataProcessor, RelationalQueryProcessor

# importing for grath database
from main import CollectionProcessor, TriplestoreQueryProcessor

# importing for generic queries
from main import GenericQueryProcessor

# running Annotation Processor
an = AnnotationProcessor()
r_path = 'relational.db'
an.setDbPathOrUrl(r_path)
# populating relational database
an.uploadData('data/annotations.csv')

# runnung MetadataProcessor
met = MetadataProcessor()
met.setDbPathOrUrl(r_path)
# populating relational database
met.uploadData('data/metadata.csv')

# running Collection Processor
col = CollectionProcessor()
col.setDbPathOrUrl('http://127.0.0.1:9999/blazegraph/sparql')
# populating graph database
col.uploadData('data/collection-1.json')
col.uploadData('data/collection-2.json')

# creating query processors for working with both databases
# running the Relational Query Processor
rel = RelationalQueryProcessor()
rel.setDbPathOrUrl(r_path)

# running Triple Query Processor
trip = TriplestoreQueryProcessor()
trip.setDbPathOrUrl('http://127.0.0.1:9999/blazegraph/sparql')

# creating a generic query processor for simultenious quering in both databases
gen = GenericQueryProcessor()
gen.addQueryProcessor(rel)
gen.addQueryProcessor(trip)

result_1 = gen.getEntityById("https://dl.ficlit.unibo.it/iiif/2/28429/annotation/p0008-image")
result_2 = gen.getEntitiesWithTitle("Il Canzoniere")
result_3 = gen.getAnnotationsWithTarget("https://dl.ficlit.unibo.it/iiif/2/28429/canvas/p13")
result_4 = gen.getManifestsInCollection("https://dl.ficlit.unibo.it/iiif/19428-19425/collection")
# etc...

#print(result_1)
#print(result_2)
#print(result_3)
print(result_4)