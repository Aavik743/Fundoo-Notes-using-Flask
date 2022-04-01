from label.apis import Label_API, LabelFunctionalityAPI

label_routes = [
    (Label_API, '/label'),
    (LabelFunctionalityAPI, '/label_functionality/<int:id>')
]
