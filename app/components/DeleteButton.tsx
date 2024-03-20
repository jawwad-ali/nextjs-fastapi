"use client";

import { deleteTodos } from "../server/actions";
import { useTransition } from "react";

const DeleteButton = ({ id }: { id: number }) => {
  const [isPending, startTransition] = useTransition();

  return (
    <button
      className="bg-red-500 text-white px-3 py-2 rounded-xl text-sm"
      onClick={() => startTransition(() => deleteTodos(id))}
    >
      {isPending ? "Removing..." : "Delete"}
    </button>
  );
};
export default DeleteButton;

// export const FakeInput = () => {
//   const [currentValue, setCurrentValue] = useState("hi..");
//   const [updatedValue, setUpdatedValue] = useState("");

//   // Function to handle the click event
//   const handleShowCurrentValueClick = () => {
//     // Set the updatedValue to the currentValue
//     setUpdatedValue(currentValue);
//   };

//   return (
//     <>
//       {/* Input field */}
//       <input
//         type="text"
//         value={updatedValue} // Bind the input value to the updatedValue state
//         onChange={(e) => setUpdatedValue(e.target.value)} // Handle input change
//       />
//       {/* Button to show current value */}
//       <button onClick={handleShowCurrentValueClick}>Show Current Value</button>
//       <button>{updatedValue.length > 0 && updatedValue}</button>
//     </>
//   );
// };


// export const UpdateButton = ({ id, title }: { id: number; title: string }) => {
//   const [isPending, startTransition] = useTransition();

//   return (
//     <button
//       className="bg-orange-500 text-white px-3 py-2 rounded-xl text-sm"
//       onClick={() => startTransition(() => updateTodos(id))}
//     >
//       {isPending ? "Updating" : "Update"}
//     </button>
//   );
// };
