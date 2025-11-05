import {Link} from 'react-router-dom'



export function Navigation(){
    return (
        <div>
            <Link to="/tasks" >Task app</Link>
            <Link to= "/tasks-create">create task</Link>
        </div>


    )
}

