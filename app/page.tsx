"use client"
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

interface TodoProps {
  title: string;
  isCompleted: boolean;
  id: number;
}

const URL =
  process.env.NODE_ENV === "development"
    ? "http://127.0.0.1:8000/api"
    : "/api/";
console.log("URL", URL);

export default async function Home() {
  // const url = await fetch(`${URL}/api/todos/`, {
  const url = await fetch("http://127.0.0.1:8000/api/todos/", {
    cache: "no-store",
    next: {
      tags: ["todos"],
    },
  });
  const res = await url.json();
  console.log(res);

  return (
    <main className="flex min-h-screen flex-col space-y-5 max-w-5xl mx-auto ">
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
          {res.map((data: TodoProps) => (
            <TableRow key={data.id}>
              <TableCell className={`${data.isCompleted && 'line-through' }`}>{data.title}</TableCell>
              <TableCell className={`${data.isCompleted && 'line-through' }`}>
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
        {res.length == 0 && <TableCaption>NO ITEMS TO DISPLAY.. </TableCaption>}
      </Table>
    </main>
  );
}
