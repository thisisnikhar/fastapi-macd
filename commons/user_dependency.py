from commons.auth import get_current_user
from fastapi import Depends


current_user_dependency = Depends(get_current_user)