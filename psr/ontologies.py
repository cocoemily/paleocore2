import projects.ontologies as ontologies

# Basis of Record Vocabulary
BASIS_OF_RECORD_VOCABULARY = ontologies.BASIS_OF_RECORD_VOCABULARY

# Numeric Model Fields
NUMERICS = ('id', 'height', 'width', 'depth', 'upper_limit_in_section', 'lower_limit_in_section',
            'loess_mean_thickness', 'loess_max_thickness', 'loess_amount_coarse_components', 'loess_number_sediment_layers',
            'loess_number_soil_horizons', 'loess_number_coarse_layers', 'loess_number_cultural_horizons', 'item_count',
            'length_mm', 'width_mm', 'thick_mm', 'weight', 'smallplatforms', 'smalldebris', 'tinyplatforms', 'tinydebris', 'counts',)

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

PSR_CAVE_RS_VOCABULARY = ("Cave", "Rockshelter", "Cave/Rockshelter", "cave", "rockshelter")

PSR_LOESS_PROF_VOCABULARY = ("Loess Profile", "Loess", "Profile", "loess", "profile", "loess profile")

PSR_ARCHAEOLOGY_VOCABULARY = ( lithics, lithic, ceramic, ceramics, burial, bones, bone , "BONE", "Bone", "C14", "LITHIC",
                               "bead", "dent", "manuport", "woodid", "lithic", "lithics")

PSR_GEOLOGY_VOCABULARY = ( hearth, petroglyphs, geosample , "ERT", "GPR", "GPRGRID", "OSL", "ROCK", "Rock", "TOPO", "geosample",
                           "micromorph", "red_thing", "sediment", )

PSR_BIOLOGY_VOCABULARY = ( microfauna, flora, "Fauna", "fauna" )

PSR_AGGREGATE_VOCABULARY = ("Bucket", "BUCKET", "Aggregate", "Bulk Find", "aggregate", "bulk", "Bulk")

PSR_LITHIC_VOCABULARY = (lithics, lithic, "LITHIC", "manuport", "Lithic", "Lithics", "lithic", "lithics")

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
gani_iskakov = "Gani Iskakov"
tabasa_ozawa = "Tabasa Ozawa"
alice_rodriguez = "Alice Rodriguez"
tiago_attorre = "Tiago Attorre"

COLLECTOR_CHOICES = (
    (radu_iovita, "Radu Iovita"),
    (patrick_cuthbertson, "Patrick Cuthbertson"),
    (abay_namen, "Abay Namen"),
    (aris_varis, "Aris Varis"),
    (emily_coco, "Emily Coco"),
    (zhaken_taimagambetov, "Zhaken Taimagambetov"),
    (talgat_mamirov, "Talgat Mamirov"),
    (gani_iskakov, "Gani Iskakov"),
    (tabasa_ozawa, "Tabasa Ozawa"),
    (alice_rodriguez, "Alice Rodriguez"),
    (tiago_attorre, "Tiago Attorre")
)

PERSON_DICTIONARY = {
    "Radu Iovita": radu_iovita,
    "Patrick Cuthbertson": patrick_cuthbertson,
    "Abay Namen": abay_namen,
    "Aris Varis": aris_varis,
    "Emily Coco": emily_coco,
    "Zhaken Taimagambetov": zhaken_taimagambetov,
    "Talgat Mamirov": talgat_mamirov,
    "Gani Iskakov": gani_iskakov,
    "Tabasa Ozawa": tabasa_ozawa,
    "Alice Rodriguez": alice_rodriguez,
    "Tiago Attorre": tiago_attorre
}

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

locality_names = {
    "Kyzylzhartas": "Qyzyljartas",
    "Tuttybulaq Upper": "Tuttybulaq 2",
    "Zhetiotau": "Jetiotau Cave"
}
