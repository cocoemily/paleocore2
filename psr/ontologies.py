import projects.ontologies as ontologies

# Basis of Record Vocabulary
BASIS_OF_RECORD_VOCABULARY = ontologies.BASIS_OF_RECORD_VOCABULARY

# Item Type Vocabulary
ITEM_TYPE_VOCABULARY = ontologies.ITEM_TYPE_VOCABULARY

geosample = "Geosample" #geology
lithics = "Lithics" #archaeology
lithic = "Lithic" #archaeology
burial = "Burial" #archaeology?
bones = "Bones" #archaeology/biology
bone = "Bone" #archaeology/biology
enclosure = "Enclosure" #geology
hearth = "Hearth" #geology
petroglyphs = "Petroglyphs" #geology
trench = "Trench" #excavation unit?
ceramic = "Ceramic" #archaeology
ceramics = "Ceramics" #archaeology
fauna = "Fauna" #biology/archaeology
flora = "Flora" #biology
microfauna = "Microfauna" #biology



PSR_ARCHAEOLOGY_VOCABULARY = ( lithics, lithic, ceramic, ceramics, burial, bones, bone , "BONE", "Bone", "C14", "LITHIC",
                               "bead", "dent", "manuport", "woodid")

PSR_GEOLOGY_VOCABULARY = ( hearth, petroglyphs, geosample , "ERT", "GPR", "GPRGRID", "OSL", "ROCK", "Rock", "TOPO", "geosample",
                           "micromorph", "red_thing", "sediment", )

PSR_BIOLOGY_VOCABULARY = ( microfauna, flora )

PSR_AGGREGATE_VOCABULARY = ("Bucket", "BUCKET")

PSR_LITHIC_VOCABULARY = (lithics, lithic, "LITHIC", "manuport")

PSR_BONE_VOCABULARY = (bone, bones, "BONE", "dent", fauna, microfauna)

PSR_CERAMIC_VOCABULARY = (ceramic, ceramics, "CERAMIC")



# Collection Method Vocabulary
COLLECTING_METHOD_VOCABULARY = ontologies.COLLECTING_METHOD_VOCABULARY

# Anatomical Side Vocabulary
SIDE_VOCABULARY = ontologies.SIDE_VOCABULARY

# Collector Vocabulary
radu_iovita = 'Radu Iovita'
patrick_cuthbertson = 'Patrick Cuthbertson'
abay_namen = 'Abay Namen'
aris_varis = 'Aris Varis'
emily_coco = "Emily Coco"
zhaken_taimagambetov = "Zhaken Taimagambetov"
talgat_mamirov = "Talgat Mamirov"
COLLECTOR_CHOICES = (
    (radu_iovita, "Radu Iovita"),
    (patrick_cuthbertson, "Patrick Cuthbertson"),
    (abay_namen, "Abay Namen"),
    (aris_varis, "Aris Varis"),
    (emily_coco, "Emily Coco"),
    (zhaken_taimagambetov, "Zhaken Taimagambetov"),
    (talgat_mamirov, "Talgat Mamirov")
)

# Field Season Vocabulary
jun2017 = 'Jun 2017'
aug2017 = 'Aug 2017'
may2018 = 'May 2018'
jun2018 = 'Jun 2018'
aug2018 = 'Aug 2018'
may2019 = 'May 2019'
jun2019 = 'Jun 2019'
aug2019 = 'Aug 2019'
FIELD_SEASON_CHOICES = (
    (jun2017, 'Jun 2017'),
    (aug2017, 'Aug 2017'),
    (may2018, 'May 2018'),
    (jun2018, 'Jun 2018'),
    (aug2018, 'Aug 2018'),
    (may2019, 'May 2019'),
    (jun2019, 'Jun 2019'),
    (aug2019, 'Aug 2019')
)
