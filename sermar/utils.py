from sermar.models import *


def update_biology_fk():
    """
    Update collection foreign key in Biology objects
    :return:
    """
    # Get all Biology Occurrences
    bios = Biology.objects.all()

    # Iterate through all bio objects
    counter = 0
    for b in bios:
        # For each bio object...
        # Fetch the corresponding collection object, EAFP idiom
        try:
            b.collection = Collection.objects.get(collection_code=b.collection_code)
            b.save()  # save modified biology object
            counter += 1  # count successes
        except Collection.DoesNotExist:
            # if there's a problem, notfiy me
            print(f'Error fetching Collection {b.collection_id} for Biology {b.id}')
    print(f'Successfully updated {counter} out of {bios.count()} records')


def update_collection_fk():
    """
    Update locality foreign key in Collection objects
    :return:
    """
    # Get all Collction objects
    colls = Collection.objects.all()

    # Iterate through all bio objects
    counter = 0
    for c in colls:
        # For each colleciton object...
        # Fetch the corresponding locality object, EAFP idiom
        try:
            c.locality = Locality.objects.get(roost_id=c.roost_id)
            c.save()  # save modified biology object
            counter += 1  # count successes
        except Locality.DoesNotExist:
            # if there's a problem, notfiy me
            print(f'Error fetching Collection {c.collection_id} for Biology {c.id}')
    print(f'Successfully updated {counter} out of {colls.count()} records')

