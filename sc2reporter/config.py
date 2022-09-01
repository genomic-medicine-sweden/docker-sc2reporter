from pymongo import MongoClient
import os
WTF_CSRF_ENABLED = True
SECRET_KEY = 'frusklimuna4satass5h5'

QC_MAX_PCT_N = 10
DB_NAME = 'sarscov2_standalone'

if os.getenv('MONGO_HOST') != "mongodb": 
    os.environ['MONGO_HOST'] = "localhost"
    os.environ['MONGODB_PORT'] = "27017"
CLIENT = MongoClient(os.environ.get('MONGODB_HOST'),int(os.environ.get('MONGODB_PORT')))

DATABASE = CLIENT[DB_NAME]
SAMPLE_COLL = DATABASE.sample
VARIANT_COLL = DATABASE.variant
DEPTH_COLL = DATABASE.depth
USERS_COLL = DATABASE.users

DEBUG = True

PROPAGATE_EXCEPTIONS = False

PANGO_LINEAGES_OF_CONCERN = ["B.1.351","P.1","A.23.1","B.1.525","B.1.1.28.1","B.1.427", "B.1.429", "B.1.617"] # Removed B.1.1.7

POSITIONS_OF_BIOLOGICAL_SIGNIFICANCE = ["S:501", "S:484"]

VARIANTS_OF_BIOLOGICAL_SIGNIFICANCE = ["S:N501Y","S:N501T", "S:N501S", "S:E484K", "S:K417T", "S:F157L", "S:V367F", "S:Q613H", "S:P681R", "S:Q677H", "S:F888L", "S:H69_V70del", "S:N439K", "S:Y453F", "S:S98F", "S:L452R", "S:D80Y", "S:A626S", "S:V1122L", "S:A222V", "S:S477N"]