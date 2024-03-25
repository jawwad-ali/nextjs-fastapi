"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { deleteTodos, updateTodos } from "../server/actions";
import { useState, useTransition } from "react";

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

export const UpdateCheckBox = ({
  id,
  isCompleted,
}: {
  id: number;
  isCompleted: boolean;
}) => {
  return <Checkbox onClick={() => updateTodos(id, isCompleted)} />;
};
