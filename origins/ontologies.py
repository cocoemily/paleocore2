# Origins Project Choice Lists, Vocabularies, Ontologies
# choice lists and vocabularies are defined with the following design template:

# variable_label1 = value   # variable_labels are lowercase, values can be strings or numbers or codes
# variable_label2 = value
# CHOICES = (
#   (variable_label1, 'string_representation')
#   (variable_label2, 'string_representation')

# The design allows use of the variable_labels in code. Changes to the value applies automatically then in code and
# in what is written to database.


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
allotype = 'allotype' # A term, not regulated by the Code, for a designated specimen of opposite sex to the holotype
cotype = 'cotype' # A term not recognized by the Code, formerly used for either syntype or paratype, but that should
# not now be used in zoological nomenclature
genotype = 'genotype' # A term not recognized by the Code, formerly used for type species, but that should not
# now be used in zoological nomenclature
hapanotype = 'hapanotype' # One or more preparations consisting of directly related individuals representing distinct
# stages in the life cycle, which together form the name-bearing type in an extant species of protistan.
holotype = 'holotype'  # The single specimen (except in the case of a hapantotype, q.v.) designated or otherwise fixed
# as the name-bearing type of a nominal species or subspecies when the nominal taxon is established.
isotype = 'isotype' # A duplicate specimen of the holotype.
isosyntype = 'isosyntype'  # A duplicate of a syntype.
paratype = 'paratype' # A specimen not formally designated as a type but cited along with the type collection in the
# original description of a taxon.
lectotype = 'lectotype' # A syntype designated as the single name-bearing type specimen subsequent to the establishment
# of a nominal species or subspecies
neotype = 'neotype' # The single specimen designated as the name-bearing type of a nominal species or subspecies
# when there is a need to define the nominal taxon objectively and no name-bearing type is believed to be extant.
# If stability and universality are threatened, because an existing name-bearing type is either taxonomically
# inadequate or not in accord with the prevailing usage of a name, the Commission may use its plenary power
# to set aside that type and designate a neotype.
paralectotype = 'paralectotype' # Each specimen of a former syntype series remaining after the designation
# of a lectotype
syntype = 'syntype'  # Each specimen of a type series (q.v.) from which neither a holotype nor a lectotype has
# been designated. The syntypes collectively constitute the name-bearing type.
topotype = 'topotype'  # A term, not regulated by the Code, for a specimen originating from the type locality of the
# species or subspecies to which it is thought to belong, whether or not the specimen is part of the type series.

# Using a select set of terms recognized by ICZN.
TYPE_CHOICES = (
    (holotype, 'holotype'),
    (paratype, 'paratype'),
    (lectotype, 'lectotype'),
    (neotype, 'neotype'),
    (syntype, 'syntype'),
)

# Nomenclatural Code Choices
iczn = 'ICZN'
icbn = 'ICBN'
NOMENCLATURAL_CODE_CHOICES = (
    (iczn, 'ICZN'),
    (icbn, 'ICBN')
)

# Nomenclatural Status Choices
accepted = 'accepted'
junior_synonym = 'junior_synonym'
supressed = 'supressed'
NOMENCLATURAL_STATUS_CHOICES = (
    (accepted, 'accepted'),
    (junior_synonym, 'junior_synonym'),
    (supressed, 'supressed')
)


# helper functions
def choices2list(choices_tuple):
    """
    Helper function that returns a choice list tuple as a simple list of stored values
    :param choices_tuple:
    :return:
    """
    return [c[0] for c in choices_tuple]
