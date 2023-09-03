from fastapi import APIRouter, Path, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schema import Todo, TodoItem, TodoItems

todo_router = APIRouter()

todo_list = []


@todo_router.post(
    "/todo",
    status_code=201,
    responses={201: {"message": str}}
)
async def add_todo(todo: Todo) -> JSONResponse:
    todo_list.append(todo)
    return JSONResponse(
        status_code=201,
        content={"message": "Todo added successfully."}
    )


@todo_router.get(
    "/todo",
    response_model=TodoItems,
    responses={200: {"todos": list}}
)
async def retrieve_todos() -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content={"todos": jsonable_encoder(todo_list)}
    )


@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
        todo_id: int = Path(..., title="The ID of the doto to retrive.")
) -> JSONResponse:
    for todo in todo_list:
        if todo.id == todo_id:
            return JSONResponse(
                status_code=200,
                content={"todo": jsonable_encoder(todo)}
            )
    raise HTTPException(
        status_code=404,
        detail={"message": "Todo with supplied ID doesn't exist."}
    )


@todo_router.put("/todo/{todo_id}")
async def update_todo(
        todo_data: TodoItem,
        todo_id: int = Path(title="The ID of the todo to be updated.")
) -> JSONResponse:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return JSONResponse(
                status_code=200,
                content={"message": "Todo updated successfully."}
            )
    raise HTTPException(
        status_code=404,
        detail={"message": "Todo with supplied ID doesn't exist."}
    )


@todo_router.delete(
    "/todo/{todo_id}",
    status_code=204,
    responses={204: {"message": str}}
)
async def delete_single_todo(todo_id: int) -> JSONResponse:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return JSONResponse(
                status_code=204,
                content={"message": "Todo deleted successfully."}
            )
    raise HTTPException(
        status_code=404,
        detail={"message": "Todo with supplied ID doesn't exist."}
    )
