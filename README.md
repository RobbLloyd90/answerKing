# answerKing

## API Endpoint URL
answerking.ce5zstiyqlhf.eu-west-2.rds.amazonaws.com

---

## Endpoints

### Items

| Method | Endpoint          | Description                                                                                     | Notes 


| GET     | /item             | Retrieve all items.                                                                             | Returns status 200 with active items.                                                                                   |
| GET     | /item/{id}        | Remove an item by its ID.                                                                        |                                                                                                                          |
| PUT     | /item/{id}        | Modify an existing item.                                                                         | Send a JSON body with the fields to update. E.g., [{"price": 3.59}].                                                   |
| POST    | /item             | Create a new item.                                                                               | Send a JSON body with item details.                                                                                     |

---

### Categories

| Method | Endpoint             | Description                                                                                     | Notes   

| GET     | /category            | Retrieve all active categories.                                                                   | Returns status 200 with list of categories.                                                                              |
| DELETE  | /category/{id}       | Remove a category by its ID.                                                                        | Returns status 200 on success; 400 if ID does not exist or is inactive.                                                 |
| POST    | /category            | Create a new category.                                                                             | Send a JSON body; ensure required fields are included.                                                                  |

## What does it do?

This backend application enables users to view, amend, and manage items and categories within the system.

---

## Future Plans

1. Enable customer users to:
    - View items by category
    - Add items to a shopping basket
    - Amend active items within the basket
    - Pay for the total basket value if sufficient funds are available
    - Reject orders and notify customers if funds are insufficient

---

## Personal Goals

- Learn and implement proper testing syntax using pytest to build a robust application.
- Develop comprehensive tests via TDD to ensure each function performs correctly without side effects.

---

## Additional Endpoints & Behavior Details

### Items

| Operation | Expected Status & Behavior | Additional Notes |
|------------|----------------------------|------------------|
| GET all items | 200 OK when valid; returns active items. | |
| Remove item /item/{id} | 200 OK with valid ID; 400 if ID does not exist or isActive is false. | |
| Modify item /item/{id} | 201 Created on successful update; 400 Bad Request if multiple fields, invalid ID, or invalid body keys. | Body should contain only one valid key at a time. |
| Create new item /item | 201 Created when all required fields are provided; 400 Bad Request otherwise. | Spelling and casing of keys must match, but case mismatch will still succeed if keys are correct. |

---

### Categories

| Operation | Expected Status & Behavior | Additional Notes |
|------------|----------------------------|------------------|
| GET all categories | 200 OK when valid; returns list of active categories. | |
| Remove category /category/{id} | 200 OK with valid ID; 400 if ID does not exist or isActive is false. | |
| Create new category /category | 201 Created when all required fields are provided; 400 Bad Request otherwise. | Ensure proper casing and spelling for keys. |