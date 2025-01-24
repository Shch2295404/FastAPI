from fastapi import HTTPException, Request, status

def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token

def get_current_user(token):
    
    return "user"