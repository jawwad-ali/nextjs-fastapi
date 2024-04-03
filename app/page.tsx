"use client";
import { addTodos } from "@/app/server/actions";
import DeleteButton, { UpdateCheckBox } from "./components/DeleteButton";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useState, useEffect } from "react";
import Link from "next/link";

interface TodoProps {
  title: string;
  isCompleted: boolean;
  id: number;
}

const URL =
  process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8000/api"
    : `${process.env.NEXT_PUBLIC_DEPLOYED_URL}/api`;
console.log("URL", URL);

export default function Home() {
  const [todos, setTodos] = useState([]);

  const fetchTodos = async () => {
    // const url = await fetch(`${URL}/todos/`, {
    const url = await fetch("/api/todos", {
      cache: "no-store",
      next: {
        tags: ["todos"],
      },
    });
    const res = await url.json();
    setTodos(res);
    console.log(res);
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <main className="flex min-h-screen flex-col space-y-5 max-w-5xl mx-auto ">
      <Link href="/api/todos">Hello API</Link>
      {/* Form */}
      <div className="flex flex-col w-1/2 mx-auto mt-5">
        <form action={addTodos}>
          <Input name="title" placeholder="Add Todos..." />
          <button className="border w-full bg-blue-500 text-white p-2 rounded-md">
            Add
          </button>
        </form>
      </div>

      {/* Listing Todos */}
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Todos</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Delete</TableHead>
            <TableHead>Update</TableHead>
          </TableRow>
        </TableHeader>

        <TableBody>
          {todos.map((data: TodoProps) => (
            <TableRow key={data.id}>
              <TableCell className={`${data.isCompleted && "line-through"}`}>
                {data.title}
              </TableCell>
              <TableCell className={`${data.isCompleted && "line-through"}`}>
                {data.isCompleted == true ? "Completed" : "Pending"}
              </TableCell>

              <TableCell>
                <DeleteButton id={data.id} />
              </TableCell>

              <TableCell>
                <UpdateCheckBox id={data.id} isCompleted={data.isCompleted} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>

        {/* If there are no items in the list */}
        {todos.length == 0 && (
          <TableCaption>NO ITEMS TO DISPLAY.. </TableCaption>
        )}
      </Table>
    </main>
  );
}
