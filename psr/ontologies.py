import projects.ontologies as ontologies

# Basis of Record Vocabulary
BASIS_OF_RECORD_VOCABULARY = ontologies.BASIS_OF_RECORD_VOCABULARY

# Item Type Vocabulary
ITEM_TYPE_VOCABULARY = ontologies.ITEM_TYPE_VOCABULARY

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
