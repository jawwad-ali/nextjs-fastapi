import { addTodos } from "@/app/server/actions";
import DeleteButton  from "./components/DeleteButton";

interface TodoProps {
  title: string;
  id: number;
}

export default async function Home() {
  const url = await fetch("http://127.0.0.1:8000/todos/", {
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
          <input
            name="title"
            placeholder="Enter Title"
            className="w-full border h-8 border-gray-400 rounded-md "
          />
          {/* <InputField res={res} /> */}

          <button className="border w-full bg-blue-500 text-white p-2 rounded-md">
            Add
          </button>
        </form>
      </div>

      {/* Listing Todos */}
      {res.map((todo: TodoProps) => (
        <div
          key={todo.id}
          className=" space-x-5 p-2 border w-1/2 mx-auto flex-col rounded-lg"
        >
          <div className="flex items-center justify-between">
            <ol className=" px-5 my-2">
              <li className="text-sm">{todo.title}</li>
            </ol>

            <div className="flex flex-end space-x-5">
              <DeleteButton id={todo.id} />
              {/* <UpdateButton id={todo.id} title={todo.title} /> */}
            </div>
          </div>
        </div>
      ))}
    </main>
  );
}
