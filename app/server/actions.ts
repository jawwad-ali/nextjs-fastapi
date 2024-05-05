"use server"

import { revalidateTag } from "next/cache";

// Add Todos
export const addTodos = async (e: FormData) => {

    let title = e.get("title") as string;
    console.log("serverTodo", title)

    if (!title) return

    // await fetch(`${URL}/todos/` , {
        await fetch("http://backend:8000/api/todos/", {
        method: "POST",
        body: JSON.stringify({
            title: title,
        }),

        headers: {
            "Content-Type": "application/json"
        }
    })
    revalidateTag('todos')
}

// Delete Todos
export const deleteTodos = async (todo_id: number) => {
    console.log(todo_id)
    console.log(typeof todo_id)

    // await fetch(`${URL}/todos/${todo_id}`, {
    await fetch(`http://backend:8000/api/todos/${todo_id}`, {
        method: "DELETE",
        body: JSON.stringify({
            todo_id: todo_id 
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    revalidateTag(`todos`)
}

// Update Todos
export const updateTodos = async (todo_id: number, isCompleted: boolean) => {
    console.log("Update", todo_id, isCompleted)
    console.log(typeof todo_id)

    await fetch(`http://backend:8000/api/todos/${todo_id}`, {
        method: "PATCH",
        body: JSON.stringify({
            todo_id: todo_id,
            isCompleted: !isCompleted
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    revalidateTag(`todos`)
}