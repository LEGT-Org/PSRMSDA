Use this to debug on Auth Router

print("REFRESH TOKEN CREATED:", refresh_token)
print("SECURE:", settings.allowed_secure)
print("SAMESITE:", settings.allowed_samesite)

print("COOKIE SET")
print(response.headers)
