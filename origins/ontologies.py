# Origins Project Choice Lists, Vocabularies, Ontologies
# choice lists and vocabularies are defined with the following design template:

# variable_label1 = value   # variable_labels are lowercase, values can be strings or numbers or codes
# variable_label2 = value
# CHOICES = (
#   (variable_label1, 'string_representation')
#   (variable_label2, 'string_representation')

# The design allows use of the variable_labels in code. Changes to the value applies automatically then in code and
# in what is written to database.


# Anatomical Element Region Choices
cranial = "cranial"
appendicular = "appendicular"
axial = "axial"
ANATOMICAL_REGION_CHOICES =(
    (cranial, "cranial"),
    (appendicular, "appendicular"),
    (axial, "axial")
)


# Anatomical Preservation Choices
complete = "complete" # > 95%
nearly_complete = "nearly complete" # > 75%
fragment = "fragment"
ANATOMICAL_PRESERVATION_CHOICES = (
    (complete, "complete"),
    (nearly_complete, "nearly complete"),
    (fragment, "fragment")
)

# Continents of the World
africa = 'Africa'
antarctica = 'Antarctica'
asia = 'Asia'
australia = 'Australia'
europe = 'Europe'
north_america = 'North America'
south_america = 'South America'

CONTINENT_CHOICES = (
    (africa, 'Africa'),
    (antarctica, 'Antarctica'),
    (asia, 'Asia'),
    (australia, 'Australia'),
    (europe, 'Europe'),
    (north_america, 'North America'),
    (south_america, 'South America')
)

# Type Specimens Choices
# Definitions copied from ICZN online http://code.iczn.org
allotype = 'allotype'  # A term, not regulated by the Code, for a designated specimen of opposite sex to the holotype
cotype = 'cotype'  # A term not recognized by the Code, formerly used for either syntype or paratype, but that should
# not now be used in zoological nomenclature
genotype = 'genotype'  # A term not recognized by the Code, formerly used for type species, but that should not
# now be used in zoological nomenclature
hapanotype = 'hapanotype'  # One or more preparations consisting of directly related individuals representing distinct
# stages in the life cycle, which together form the name-bearing type in an extant species of protistan.
holotype = 'holotype'  # The single specimen (except in the case of a hapantotype, q.v.) designated or otherwise fixed
# as the name-bearing type of a nominal species or subspecies when the nominal taxon is established.
isotype = 'isotype'  # A duplicate specimen of the holotype.
isosyntype = 'isosyntype'  # A duplicate of a syntype.
paratype = 'paratype'  # A specimen not formally designated as a type but cited along with the type collection in the
# original description of a taxon.
lectotype = 'lectotype'  # A syntype designated as the single name-bearing type specimen subsequent to the establishment
# of a nominal species or subspecies
neotype = 'neotype'  # The single specimen designated as the name-bearing type of a nominal species or subspecies
# when there is a need to define the nominal taxon objectively and no name-bearing type is believed to be extant.
# If stability and universality are threatened, because an existing name-bearing type is either taxonomically
# inadequate or not in accord with the prevailing usage of a name, the Commission may use its plenary power
# to set aside that type and designate a neotype.
paralectotype = 'paralectotype'  # Each specimen of a former syntype series remaining after the designation
# of a lectotype
syntype = 'syntype'  # Each specimen of a type series (q.v.) from which neither a holotype nor a lectotype has
# been designated. The syntypes collectively constitute the name-bearing type.
topotype = 'topotype'  # A term, not regulated by the Code, for a specimen originating from the type locality of the
# species or subspecies to which it is thought to belong, whether or not the specimen is part of the type series.

# Using a select set of terms recognized by ICZN.
TYPE_CHOICES = (
    (holotype, 'Holotype'),
    (paratype, 'Paratype'),
    (lectotype, 'Lectotype'),
    (neotype, 'Neotype'),
    (syntype, 'Syntype'),
)

# Nomenclatural Code Choices
iczn = 'ICZN'
icbn = 'ICBN'
NOMENCLATURAL_CODE_CHOICES = (
    (iczn, 'ICZN'),
    (icbn, 'ICBN')
)

# Nomenclatural CODE taxon rank group choices
species_group = 'species-group'
genus_group = 'genus-group'
family_group = 'family-group'
TAXON_RANK_GROUP_CHOICES = (
    (species_group, 'species-group'),
    (genus_group, 'genus-group'),
    (family_group, 'family-group')
)

# Bernard Campbell Nomenclatural Status Choices
valid = 'valid'
invalid_gh = 'invalid_gh'  # Generic homonym
invalid_ga = 'invalid_ga'  # Genus nomen nudum before 1931
invalid_gb = 'invalid_gb'  # Genus nomen nudum after 1930
invalid_sh = 'invalid_sh'  # Specific homonym
invalid_sm = 'invalid_sm'  # Specific nomen nudum before 1931
invalid_sn = 'invalid_sn'  # Specific nomen nudum after 1930
invalid_so = 'invalid_so'  # Specific nomen nudum - proposed conditionally
suppressed = 'suppressed'  # Name suppressed by ICZN decision.
BC_STATUS_CHOICES = (
    (valid, 'Valid'),
    (invalid_gh, 'Invalid GH'),
    (invalid_ga, 'Invalid GA'),
    (invalid_gb, 'Invalid GB'),
    (invalid_sh, 'Inavlid SH'),
    (invalid_sm, 'Invalid SM'),
    (invalid_sn, 'Invalid SN'),
    (invalid_so, 'Inavlid SO'),
    (suppressed, 'Suppressed')
)

# Origins Nomenclatural Status Choices
unavailable = 'unavailable'
invalid = 'invalid'
suppressed = 'suppressed'
potentially_valid = 'potentially_valid'
NOMENCLATURAL_STATUS_CHOICES = (
    (unavailable, 'unavailable'),
    (invalid, 'invalid'),
    (suppressed, 'suppressed'),
    (potentially_valid, 'potentially valid'),
)

# Origins Nomenclatural Status Remark Choices
conditional = 'conditionally proposed'
fictional = 'fictional'
nomen_nudum = 'nomen nudum'
improperly_formed = 'improperly formed'
improperly_published = 'improperly published'
lacks_type = 'lacks type specimen or species'
homonym = 'homonym'
objective_synonym = 'objective synonym'
STATUS_REMARK_CHOICES=(
    (conditional, 'Conditionally proposed'),
    (fictional, 'Fictional'),
    (nomen_nudum, 'Nomen nudum'),
    (improperly_formed, 'Improperly formed'),
    (improperly_published, 'Improperly published'),
    (lacks_type, 'Lacks type specimen/species'),
    (homonym, 'Homonym'),
    (objective_synonym, 'Objective synonym')
)

# Classification Status Choices
accepted = 'accepted'
junior_synonym = 'junior_synonym'
deprecated = 'deprecated'
# supressed defined above for Nomenclatural status choices
CLASSIFICATION_STATUS_CHOICES = (
    (accepted, 'Accepted'),
    (junior_synonym, 'Junior Synonym'),
    (deprecated, 'Deprecated')
)

# Verifiers
denne = 'Denne Reed'
emily = 'Emily Raney'
jyhreh = 'Jyhreh Johnson'
harper = 'Harper Jackson'
nida = 'Nida Virabalin'
kennedy = 'Kennedy Knowlton'
ashlynn = 'Ashlynn Arzola'
nick = 'Nicholas Hartman'
jorge = 'Jorge Ramirez Salinas'
hayden = 'Hayden Post'
mackenzie = 'Mackenzie Murray'

VERIFIER_CHOICES = (
    (denne, 'DR'),
    (emily, 'ER'),
    (jyhreh, 'JJ'),
    (harper, 'HJ'),
    (kennedy, 'KK'),
    (nida, 'NV'),
    (ashlynn, 'AA'),
    (nick, 'NH'),
    (jorge, 'JRS'),
    (hayden, 'HP'),
    (mackenzie, 'MM')
)


# helper functions
def choices2list(choices_tuple):
    """
    Helper function that returns a choice list tuple as a simple list of stored values
    :param choices_tuple:
    :return:
    """
    return [c[0] for c in choices_tuple]
