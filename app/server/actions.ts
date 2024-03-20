"use server"

import { revalidateTag } from "next/cache";

// Add Todos
export const addTodos = async (e:FormData) => {

    let title = e.get("title") as string;
    console.log("serverTodo",title)

    if(!title) return 

    await fetch("http://127.0.0.1:8000/todos/" , {
        method:"POST",
        body: JSON.stringify({
            title:title 
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
    revalidateTag('todos')
}

// Delete Todos
export const deleteTodos = async (todo_id:number) => {
    console.log(todo_id)
    console.log(typeof todo_id)

    await fetch(`http://127.0.0.1:8000/todos/${todo_id}` , {
        method:"DELETE",
        body: JSON.stringify({
            todo_id:todo_id
        }), 
        headers: {
            "Content-Type": "application/json"
        }
    })
    revalidateTag(`todos`)
}


// Update Todos
export const updateTodos = async (todo_id:number) => {
    console.log("Update",todo_id)
    console.log(typeof todo_id)

    await fetch(`http://127.0.0.1:8000/todos/${todo_id}` , {
        method:"PATCH",
        body: JSON.stringify({
            todo_id:todo_id
        }), 
        headers: {
            "Content-Type": "application/json"
        }
    })
    // revalidateTag(`todos`)
}