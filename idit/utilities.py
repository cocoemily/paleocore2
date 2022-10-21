from .models import Description, CharacterState

descriptions = Description.objects.all()
for d in descriptions:
    d.character_state = CharacterState.objects.get(cid=d.character.cid, char_state__exact=d.char_state)
