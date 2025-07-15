import pytest
from unittest.mock import MagicMock, patch
import os
import json
from ..lambda_funcs.mod_category.modCategory_lambda import modCategory 

@patch(modCategory.lambda_handler)
def Mod_existing_item():
    #Arrange
    dbToMod = {"category_id": 4, "name": "3 for £12", "isActive": True}
    id = 4
    body = {"name": "3 for £12"}
    request = (body, id)
    context = None
    #Act
    response = modCategory.lambda_handler(request, context ) 
    #Assert
    assert response == {"name": "3 for £12"}