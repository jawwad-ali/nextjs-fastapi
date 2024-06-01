import { addTodos } from "@/app/server/actions";
import DeleteButton from "./components/DeleteButton";
import { Input } from "@/components/ui/input";
import Link from "next/link";

interface TodoProps {
  title: string; 
  isCompleted: boolean;
  id: number;
} 

export default async  function Home() {
  const fetchTodos = async () => {
      const url = await fetch("http://backend:8000/api/todos", {
      cache: "no-store",
      next: { 
        tags: ["todos"],
      },
    }); 
    const res = await url.json();
    console.log(res); 
    return res
  };


  const todos = await fetchTodos();

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
      {todos.map((data: TodoProps) => (
        <div key={data.id} className="w-full flex items-center justify-around">
          {data.title}

          <p className="underline">{data.isCompleted == true ? "Completed" : "Pending"} </p>

          <DeleteButton id={data.id} />

          {/* <UpdateCheckBox id={data.id} isCompleted={data.isCompleted} /> */}
        </div>
      ))}

      {/* If there are no items in the list */}
      {todos.length == 0 && (
        <div>NO ITEMS TO DISPLAY.. </div>
      )}
    </main >
  );
}