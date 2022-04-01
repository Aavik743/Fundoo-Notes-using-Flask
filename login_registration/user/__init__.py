from .apis import Register_API, ActivateAccount_API, Login_API, Reset_Password_API, Forgot_Pass_API

user_routes = [
    (Register_API, '/register'),
    (ActivateAccount_API, '/activate'),
    (Login_API, '/login'),
    (Reset_Password_API, '/reset_password'),
    (Forgot_Pass_API, '/forgot_password')
]
