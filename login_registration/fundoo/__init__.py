from .apis import NoteAPI, NoteFunctionalityAPI, PinNoteApi, LabelNoteAPI, TrashNoteApi

fundoo_routes = [
    (NoteAPI, '/note'),
    (NoteFunctionalityAPI, '/note_functionality/<int:id>'),
    (PinNoteApi, '/pin_note/<int:id>'),
    (TrashNoteApi, '/trash_note/<int:id>'),
    (LabelNoteAPI, '/label_note/<int:id>')
]
