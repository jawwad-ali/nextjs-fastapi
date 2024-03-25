import { fetchTodos } from "../server/actions"

import { Table, TableBody, TableCaption, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const Todos = () => {
    // const getTodos = async() => {
    //     try{
    //         const data = await fetchTodos()
    //         console.log("data", data)
    //     }
    //     catch(err){
    //         console.error(err)
    //     }
    // }

    // const res = getTodos()
    // console.log("resfromtodos",res)

    return (
    <Table>
      <TableCaption>A list of your recent invoices.</TableCaption>
      {/* <TableHeader>
        <TableRow>
          <TableHead className="w-[100px]">Invoice</TableHead>
          <TableHead>Todos</TableHead>
          <TableHead>Delete</TableHead>
          <TableHead>Update</TableHead>
          <TableHead className="text-right">Amount</TableHead>
        </TableRow>
      </TableHeader> */}


        <TableBody>
            {/* {
                
            } */}
        </TableBody>

      </Table>
  )
}

export default Todos