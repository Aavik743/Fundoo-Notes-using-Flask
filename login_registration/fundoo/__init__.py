from .apis import CreateNoteAPI, GetNotesAPI, UpdateNoteAPI, DeleteNoteAPI

fundoo_routes = [
    (CreateNoteAPI, '/create_note'),
    (GetNotesAPI, '/get_note'),
    (UpdateNoteAPI, '/update_note'),
    (DeleteNoteAPI, '/delete_note')
]
