import dateutil.parser as parser

def create_pc_export_file():
    """
    Create a simple Paleo Core export file. Flat file in CSV format.
    :return:
    """
    @staticmethod
    def get_type():
        return 'PhysicalObject'

    def get_modified():
        return


def get_as_pc(obj):
    rdict = {
        'type': 'PhysicalObject',
        'language': 'en',
        'modified': obj.date_last_modified.date().isoformat(),  # ISO date string e.g. 2019-10-31
        'license': 'https://creativecommons.org/publicdomain/zero/1.0/legalcode',
        'rights_holder': 'National Museums of Tanzania',
        'access_rights': 'public domain',
        'bibliographic_citation': 'Reed, D., Harrison, T., & Kwekason, A. (2019). Eyasi Plateau Paleontological Expedition, Laetoli, Tanzania, fossil specimen database 1998–2005. Scientific Data, 6(1), 304.',
        'references': '',
        'institution_id': '',  # !! Register with GBIF? or Mint in Paleo Core
        'collection_id': '',  # !! Mint in Paleo Core
        'dataset_id': '',  # !! Mint in Paleo Core
        'institution_code': obj.institution_code,
        'collection_code': obj.collection_code(),
        'dataset_name': 'Eyasi Plateau Paleontology Expedition 1998-2005',
        'owner_institution_code': '',
        'basis_of_record': ''


    }

